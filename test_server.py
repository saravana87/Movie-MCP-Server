#!/usr/bin/env python3
"""
Basic test script for Movie MCP Server functionality.
Run this to verify the server components work correctly.
"""

import os
import sys
import pandas as pd
from pathlib import Path

# Add the current directory to sys.path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_csv_loading():
    """Test if the CSV file can be loaded."""
    print("Testing CSV file loading...")
    
    csv_path = Path("movies.csv")
    if not csv_path.exists():
        print("❌ movies.csv not found")
        return False
    
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Successfully loaded {len(df)} movies")
        print(f"   Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

def test_movie_search():
    """Test the movie search functionality."""
    print("\nTesting movie search...")
    
    try:
        # Import the search function
        from mcp_moviedb_server import fuzzy_search_movies, load_movie_data
        
        # Load data
        if not load_movie_data():
            print("❌ Failed to load movie data")
            return False
        
        # Test search
        results = fuzzy_search_movies("Avatar", limit=3)
        if results:
            print(f"✅ Found {len(results)} results for 'Avatar'")
            for i, movie in enumerate(results[:2], 1):
                title = movie.get('title', 'Unknown')
                year = movie.get('release_date', 'Unknown')[:4] if movie.get('release_date') else 'Unknown'
                print(f"   {i}. {title} ({year})")
            return True
        else:
            print("❌ No results found for 'Avatar'")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_environment():
    """Test environment configuration."""
    print("\nTesting environment configuration...")
    
    # Check for .env file
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if env_path.exists():
        print("✅ .env file found")
    elif env_example_path.exists():
        print("ℹ️  .env.example found (copy to .env and configure)")
    else:
        print("ℹ️  No .env file found (optional)")
    
    # Check Python version
    import sys
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"⚠️  Python version: {version.major}.{version.minor}.{version.micro} (3.8+ recommended)")
    
    return True

def test_dependencies():
    """Test if required dependencies are available."""
    print("\nTesting dependencies...")
    
    required_modules = [
        'pandas',
        'httpx', 
        'bs4',
        'pydantic',
        'dotenv'
    ]
    
    all_available = True
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - not installed")
            all_available = False
    
    # Test MCP (optional but recommended)
    try:
        import mcp
        print("✅ mcp")
    except ImportError:
        print("⚠️  mcp - not installed (required for server functionality)")
        all_available = False
    
    return all_available

def main():
    """Run all tests."""
    print("🎬 Movie MCP Server - Basic Tests")
    print("=" * 40)
    
    tests = [
        test_environment,
        test_dependencies,
        test_csv_loading,
        test_movie_search
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 40)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! The server should work correctly.")
    elif passed >= total - 1:
        print("✅ Most tests passed. Minor issues detected.")
    else:
        print("⚠️  Several issues detected. Please resolve them before running the server.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)