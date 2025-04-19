# Movie-MCP-Server
This MCP server uses Movie server tools and Web search tools.

🚀 Features
Search movie titles by keyword (using Dataframe)
Search latest movies thru web

📦 Requirements
Python 3.8+
httpx
beautifulsoup4
pandas
mcp (FastMCP protocol library)

# Clone the repo
https://github.com/saravana87/Movie-MCP-Server.git

# Create virtual environment
python -m venv venv

.\venv\Scripts\activate  # On Windows

source venv/bin/activate  # On macOS/Linux

Running the MCP Server
python python .\mcp_moviedb_server.py --server_type=sse
