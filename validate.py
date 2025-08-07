#!/usr/bin/env python3
"""
Simple validation script that checks the server structure without dependencies.
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check if required files exist."""
    print("🔍 Checking required files...")
    
    required_files = [
        "mcp_moviedb_server.py",
        "movies.csv", 
        "README.md",
        ".env.example"
    ]
    
    all_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - missing")
            all_exist = False
    
    return all_exist

def check_server_structure():
    """Check if the server file has proper structure."""
    print("\n🔍 Checking server structure...")
    
    try:
        with open("mcp_moviedb_server.py", "r") as f:
            content = f.read()
        
        required_elements = [
            "import logging",
            "class Config:",
            "def load_movie_data():",
            "def fuzzy_search_movies(",
            "@mcp.tool()",
            "def get_movie_info(",
            "def search_web(",
            "def get_movie_stats(",
            "if __name__ == \"__main__\":"
        ]
        
        all_present = True
        for element in required_elements:
            if element in content:
                print(f"✅ {element}")
            else:
                print(f"❌ {element} - missing")
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error reading server file: {e}")
        return False

def check_requirements():
    """Check requirements files."""
    print("\n🔍 Checking requirements...")
    
    req_files = ["requirements-clean.txt", "requirements-minimal.txt"]
    found_any = False
    
    for req_file in req_files:
        if Path(req_file).exists():
            print(f"✅ {req_file}")
            found_any = True
        else:
            print(f"ℹ️  {req_file} - not found")
    
    # Check old requirements file
    if Path("requirements.txt").exists():
        print("ℹ️  requirements.txt - exists (consider using requirements-clean.txt)")
    
    return found_any

def check_csv_structure():
    """Basic check of CSV file structure."""
    print("\n🔍 Checking movie database...")
    
    try:
        csv_path = Path("movies.csv")
        if not csv_path.exists():
            print("❌ movies.csv not found")
            return False
        
        # Read first few lines to check structure
        with open(csv_path, "r", encoding="utf-8") as f:
            header = f.readline().strip()
            first_row = f.readline().strip()
        
        if "title" in header.lower() and "," in header:
            print("✅ CSV structure looks valid")
            print(f"   Columns found: {len(header.split(','))}")
            return True
        else:
            print("❌ CSV structure may be invalid")
            return False
            
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

def main():
    """Run validation checks."""
    print("🎬 Movie MCP Server - Validation Checks")
    print("=" * 45)
    
    checks = [
        ("File Structure", check_files),
        ("Server Code", check_server_structure), 
        ("Requirements", check_requirements),
        ("Database", check_csv_structure)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 {name}:")
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Check failed: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 45)
    print(f"Validation Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All validations passed!")
        print("The server structure looks good. Install dependencies and run the server.")
    elif passed >= total - 1:
        print("✅ Most validations passed. Minor issues detected.")
    else:
        print("⚠️  Several issues detected. Please review the problems above.")
    
    print("\n📋 Next Steps:")
    print("1. Install dependencies: pip install -r requirements-clean.txt")
    print("2. Copy .env.example to .env and configure")
    print("3. Run: python mcp_moviedb_server.py")
    
    return passed >= total - 1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)