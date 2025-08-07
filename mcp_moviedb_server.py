import argparse
import os
import json
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path

import pandas as pd
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
import dotenv

# Try to import FastMCP, fall back to standard MCP if not available
try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    print("FastMCP not available. Please install mcp package.")
    MCP_AVAILABLE = False
    exit(1)

# Load environment variables
dotenv.load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    SERPER_URL = "https://google.serper.dev/search"
    MOVIES_CSV_PATH = os.getenv("MOVIES_CSV_PATH", "movies.csv")
    SERPER_API_KEY = os.getenv("SERPER_API_KEY")
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Validate configuration
if not Config.SERPER_API_KEY:
    logger.warning("SERPER_API_KEY not found in environment variables. Web search will not work.")

# Create MCP server
mcp = FastMCP("MovieServer")

# Global variables for data
movies_df: Optional[pd.DataFrame] = None

def load_movie_data() -> bool:
    """Load and preprocess movie data."""
    global movies_df
    
    try:
        csv_path = Path(Config.MOVIES_CSV_PATH)
        if not csv_path.exists():
            logger.error(f"Movie CSV file not found: {Config.MOVIES_CSV_PATH}")
            return False
        
        logger.info(f"Loading movie data from {Config.MOVIES_CSV_PATH}")
        movies_df = pd.read_csv(Config.MOVIES_CSV_PATH)
        
        # Normalize and preprocess data
        movies_df['title_lower'] = movies_df['title'].str.lower()
        movies_df['title_normalized'] = movies_df['title'].str.lower().str.strip()
        
        # Fill NaN values for better search results
        movies_df['overview'] = movies_df['overview'].fillna('')
        movies_df['genres'] = movies_df['genres'].fillna('')
        
        logger.info(f"Loaded {len(movies_df)} movies successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load movie data: {e}")
        return False

# Load data on startup
if not load_movie_data():
    logger.error("Failed to load movie data. Exiting.")
    exit(1)

def fuzzy_search_movies(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Perform fuzzy search on movie titles and return results."""
    if movies_df is None:
        return []
    
    query_lower = query.lower().strip()
    
    # First try exact matches
    exact_matches = movies_df[movies_df['title_normalized'] == query_lower]
    
    # Then try contains matches
    contains_matches = movies_df[
        movies_df['title_lower'].str.contains(query_lower, na=False, regex=False)
    ]
    
    # Combine results, prioritizing exact matches
    all_matches = pd.concat([exact_matches, contains_matches]).drop_duplicates()
    
    # Sort by popularity (descending) and vote_average for better results
    if 'popularity' in all_matches.columns:
        all_matches = all_matches.sort_values(['popularity'], ascending=False)
    
    # Limit results
    results = all_matches.head(limit)
    
    # Convert to list of dictionaries
    movie_list = []
    for _, row in results.iterrows():
        movie_dict = row.to_dict()
        # Clean up NaN values
        movie_dict = {k: v for k, v in movie_dict.items() if pd.notna(v)}
        movie_list.append(movie_dict)
    
    return movie_list

def format_movie_info(movie_data: Dict[str, Any]) -> str:
    """Format movie information for display."""
    if not movie_data:
        return "No movie data available"
    
    # Essential fields to display
    essential_fields = ['title', 'release_date', 'overview', 'genres', 'vote_average', 
                       'vote_count', 'runtime', 'budget', 'revenue', 'director']
    
    formatted_lines = []
    
    for field in essential_fields:
        if field in movie_data and movie_data[field]:
            value = movie_data[field]
            # Format field names nicely
            display_name = field.replace('_', ' ').title()
            
            # Special formatting for certain fields
            if field == 'budget' or field == 'revenue':
                if isinstance(value, (int, float)) and value > 0:
                    formatted_lines.append(f"{display_name}: ${value:,.0f}")
            elif field == 'runtime':
                if isinstance(value, (int, float)) and value > 0:
                    formatted_lines.append(f"{display_name}: {value:.0f} minutes")
            elif field == 'vote_average':
                if isinstance(value, (int, float)):
                    formatted_lines.append(f"{display_name}: {value:.1f}/10")
            else:
                formatted_lines.append(f"{display_name}: {value}")
    
    return "\n".join(formatted_lines) if formatted_lines else "Movie information unavailable"

# --- Tool: Get info about a movie ---
@mcp.tool()
def get_movie_info(title: str, limit: int = 5) -> str:
    """
    Search and return movie information from the dataset.
    
    Args:
        title: Movie title to search for
        limit: Maximum number of results to return (default: 5)
    
    Returns:
        Formatted movie information or error message
    """
    try:
        if not title or not title.strip():
            return "Please provide a movie title to search for."
        
        logger.info(f"Searching for movie: {title}")
        
        # Perform fuzzy search
        results = fuzzy_search_movies(title.strip(), limit)
        
        if not results:
            return f"No movies found matching '{title}'. Try a different title or check spelling."
        
        # Format results
        if len(results) == 1:
            return format_movie_info(results[0])
        else:
            # Multiple results - show summary
            formatted_results = []
            for i, movie in enumerate(results, 1):
                basic_info = f"{i}. {movie.get('title', 'Unknown')} ({movie.get('release_date', 'Unknown year')[:4] if movie.get('release_date') else 'Unknown year'})"
                if movie.get('vote_average'):
                    basic_info += f" - Rating: {movie['vote_average']:.1f}/10"
                formatted_results.append(basic_info)
            
            result_text = f"Found {len(results)} movies matching '{title}':\n\n"
            result_text += "\n".join(formatted_results)
            result_text += f"\n\nUse a more specific title to get detailed information about a particular movie."
            
            return result_text
            
    except Exception as e:
        logger.error(f"Error searching for movie '{title}': {e}")
        return f"An error occurred while searching for the movie: {str(e)}"

@mcp.tool()
async def search_web(query: str, num_results: int = 2) -> str:
    """
    Search the web for movie-related information using Serper API.
    
    Args:
        query: Search query for movies
        num_results: Number of search results to return (default: 2, max: 10)
    
    Returns:
        Formatted search results or error message
    """
    try:
        if not Config.SERPER_API_KEY:
            return "Web search is not available. SERPER_API_KEY environment variable is not set."
        
        if not query or not query.strip():
            return "Please provide a search query."
        
        # Validate and limit num_results
        num_results = max(1, min(num_results, 10))
        
        logger.info(f"Performing web search for: {query}")
        
        payload = json.dumps({
            "q": query.strip(),
            "num": num_results
        })

        headers = {
            "X-API-KEY": Config.SERPER_API_KEY,
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=Config.REQUEST_TIMEOUT) as client:
            try:
                response = await client.post(
                    Config.SERPER_URL, 
                    headers=headers, 
                    data=payload
                )
                response.raise_for_status()
                data = response.json()
                
                # Format search results
                if 'organic' in data and data['organic']:
                    results = []
                    for i, item in enumerate(data['organic'][:num_results], 1):
                        title = item.get('title', 'No title')
                        snippet = item.get('snippet', 'No description available')
                        link = item.get('link', 'No link')
                        
                        result_text = f"{i}. **{title}**\n"
                        result_text += f"   {snippet}\n"
                        result_text += f"   Source: {link}\n"
                        results.append(result_text)
                    
                    return f"Web search results for '{query}':\n\n" + "\n".join(results)
                else:
                    return f"No web search results found for '{query}'"
                    
            except httpx.TimeoutException:
                logger.error(f"Web search timed out for query: {query}")
                return f"Web search timed out. Please try again later."
            except httpx.HTTPStatusError as e:
                logger.error(f"Web search HTTP error: {e}")
                return f"Web search failed with error: {e.response.status_code}"
                
    except Exception as e:
        logger.error(f"Error in web search for '{query}': {e}")
        return f"An error occurred during web search: {str(e)}"

@mcp.tool()
def get_movie_stats() -> str:
    """Get statistics about the movie database."""
    try:
        if movies_df is None:
            return "Movie database is not loaded."
        
        total_movies = len(movies_df)
        
        # Calculate various statistics
        stats = []
        stats.append(f"Total movies in database: {total_movies:,}")
        
        if 'release_date' in movies_df.columns:
            # Year range
            movies_with_dates = movies_df[movies_df['release_date'].notna()]
            if not movies_with_dates.empty:
                years = pd.to_datetime(movies_with_dates['release_date'], errors='coerce').dt.year
                years = years.dropna()
                if not years.empty:
                    stats.append(f"Year range: {int(years.min())} - {int(years.max())}")
        
        if 'genres' in movies_df.columns:
            # Most common genres (basic count)
            genre_counts = movies_df['genres'].value_counts().head(5)
            if not genre_counts.empty:
                stats.append("Top 5 genre combinations:")
                for genre, count in genre_counts.items():
                    if pd.notna(genre):
                        stats.append(f"  - {genre}: {count} movies")
        
        if 'vote_average' in movies_df.columns:
            # Rating statistics
            ratings = movies_df['vote_average'].dropna()
            if not ratings.empty:
                stats.append(f"Average rating: {ratings.mean():.1f}/10")
                stats.append(f"Highest rated: {ratings.max():.1f}/10")
        
        return "\n".join(stats)
        
    except Exception as e:
        logger.error(f"Error getting movie stats: {e}")
        return f"Error retrieving movie statistics: {str(e)}"

if __name__ == "__main__":
    if not MCP_AVAILABLE:
        print("MCP library is not available. Please install the required dependencies.")
        exit(1)
    
    parser = argparse.ArgumentParser(description="Movie MCP Server")
    parser.add_argument(
        "--server_type", 
        type=str, 
        default="sse", 
        choices=["sse", "stdio"],
        help="Server transport type (default: sse)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE server (default: 8000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host for SSE server (default: localhost)"
    )
    
    args = parser.parse_args()
    
    logger.info(f"Starting Movie MCP Server with {args.server_type} transport")
    logger.info(f"Movie database contains {len(movies_df) if movies_df is not None else 0} movies")
    
    try:
        if args.server_type == "sse":
            mcp.run(args.server_type, host=args.host, port=args.port)
        else:
            mcp.run(args.server_type)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        exit(1)
    
