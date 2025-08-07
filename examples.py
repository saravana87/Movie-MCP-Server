#!/usr/bin/env python3
"""
Example usage script for the Movie MCP Server.
This demonstrates how the server tools can be used.
"""

import asyncio
import json

# This is a conceptual example showing how the tools work
# In practice, these would be called through the MCP protocol

def example_movie_search():
    """Example of movie database search."""
    print("🎬 Example: Movie Database Search")
    print("-" * 40)
    
    # Simulated tool calls and expected responses
    examples = [
        {
            "query": "Avatar",
            "limit": 3,
            "description": "Search for Avatar movies"
        },
        {
            "query": "Lord of the Rings",
            "limit": 2, 
            "description": "Search for LOTR movies"
        },
        {
            "query": "Inception",
            "limit": 1,
            "description": "Find Inception"
        }
    ]
    
    for example in examples:
        print(f"\n🔍 Query: {example['description']}")
        print(f"   Tool: get_movie_info('{example['query']}', {example['limit']})")
        print(f"   Expected: Movie details with title, year, rating, overview...")

def example_web_search():
    """Example of web search functionality."""
    print("\n\n🌐 Example: Web Search")
    print("-" * 40)
    
    examples = [
        {
            "query": "latest Marvel movies 2024",
            "num_results": 3,
            "description": "Find current Marvel releases"
        },
        {
            "query": "Oscar winners 2024 best picture",
            "num_results": 5,
            "description": "Find recent Oscar information"
        }
    ]
    
    for example in examples:
        print(f"\n🔍 Query: {example['description']}")
        print(f"   Tool: search_web('{example['query']}', {example['num_results']})")
        print(f"   Expected: Web search results with titles, snippets, and sources...")

def example_database_stats():
    """Example of database statistics."""
    print("\n\n📊 Example: Database Statistics")
    print("-" * 40)
    
    print(f"\n🔍 Query: Get database information")
    print(f"   Tool: get_movie_stats()")
    print(f"   Expected: Total movies, year range, top genres, average ratings...")

def example_mcp_integration():
    """Example of MCP integration."""
    print("\n\n🔌 MCP Integration Example")
    print("-" * 40)
    
    mcp_config = {
        "mcpServers": {
            "movie-server": {
                "command": "python",
                "args": ["mcp_moviedb_server.py"],
                "env": {
                    "SERPER_API_KEY": "your_api_key_here"
                }
            }
        }
    }
    
    print("\n📝 Claude Desktop MCP Configuration:")
    print("Add this to your Claude Desktop config:")
    print(json.dumps(mcp_config, indent=2))
    
    print("\n🎯 Available Tools:")
    tools = [
        "get_movie_info - Search movie database",
        "search_web - Search web for movie info", 
        "get_movie_stats - Get database statistics"
    ]
    
    for tool in tools:
        print(f"   • {tool}")

def main():
    """Run all examples."""
    print("🎬 Movie MCP Server - Usage Examples")
    print("=" * 50)
    
    example_movie_search()
    example_web_search() 
    example_database_stats()
    example_mcp_integration()
    
    print("\n" + "=" * 50)
    print("🚀 Getting Started:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Get Serper API key: https://serper.dev")
    print("3. Configure .env file with your API key") 
    print("4. Run server: python mcp_moviedb_server.py")
    print("5. Connect via MCP protocol or test directly")
    
    print("\n📚 For more information:")
    print("• README.md - Complete setup guide")
    print("• validate.py - Check your setup")
    print("• test_server.py - Test functionality")

if __name__ == "__main__":
    main()