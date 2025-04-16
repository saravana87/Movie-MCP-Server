import argparse
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, IPvAnyAddress
import os
import dotenv
import pandas as pd
import httpx
from bs4 import BeautifulSoup
import json

dotenv.load_dotenv()

# Create MCP server
mcp = FastMCP("MovieServer")
SERPER_URL="https://google.serper.dev/search"

# Load the CSV data once
MOVIES_CSV_PATH = "movies.csv"  # <- Update path if needed
movies_df = pd.read_csv(MOVIES_CSV_PATH)

# Normalize title column
movies_df['title'] = movies_df['title'].str.lower()

# --- Tool: Get info about a movie ---
@mcp.tool()
def get_movie_info(title: str) -> str:
    """Search and return movie info from the dataset."""
    title = title.lower()
    result = movies_df[movies_df['title'].str.contains(title, na=False)]

    if result.empty:
        return f"No results found for movie: {title}"

    row = result.iloc[0].to_dict()
    return "\n".join(f"{k.capitalize()}: {v}" for k, v in row.items())

@mcp.tool()
async def search_web(query: str) -> dict | None:
    payload = json.dumps({"q": query, "num": 2})

    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                SERPER_URL, headers=headers, data=payload, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException:
            return {"organic": []}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default="sse", choices=["sse", "stdio"]
    )
    args = parser.parse_args()
    mcp.run(args.server_type)
    
