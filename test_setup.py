#!/usr/bin/env python3
"""
Test script to verify Marketing Copy Generator setup
Run this after setup to ensure everything is working correctly
"""

import sys
import os

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (need 3.8+)")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking Python dependencies...")
    required = ['flask', 'flask_cors', 'bs4', 'requests', 'anthropic', 'dotenv']
    missing = []

    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)

    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\n🔍 Checking environment configuration...")

    backend_env = os.path.join('backend', '.env')
    root_env = '.env'

    env_file = None
    if os.path.exists(backend_env):
        env_file = backend_env
    elif os.path.exists(root_env):
        env_file = root_env

    if not env_file:
        print(f"   ❌ No .env file found")
        print(f"      Create one with: cp .env.example .env")
        return False

    print(f"   ✅ .env file exists")

    # Check if API key is set
    with open(env_file, 'r') as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY=' in content and 'your_api_key_here' not in content:
            # Check if there's an actual key (starts with sk-ant-)
            for line in content.split('\n'):
                if line.startswith('ANTHROPIC_API_KEY='):
                    key = line.split('=', 1)[1].strip()
                    if key and key != 'your_api_key_here':
                        print(f"   ✅ ANTHROPIC_API_KEY configured")
                        return True

    print(f"   ⚠️  ANTHROPIC_API_KEY not set or invalid")
    print(f"      Edit {env_file} and add your API key")
    return False

def check_scraper():
    """Test the scraper module"""
    print("\n🔍 Testing scraper module...")

    try:
        sys.path.insert(0, 'backend')
        from scraper import VigoShopScraper

        scraper = VigoShopScraper()
        print(f"   ✅ Scraper imported successfully")
        return True
    except Exception as e:
        print(f"   ❌ Scraper import failed: {e}")
        return False

def check_copy_generator():
    """Test the copy generator module"""
    print("\n🔍 Testing copy generator module...")

    try:
        sys.path.insert(0, 'backend')
        from copy_generator import CopyGenerator

        # Try to initialize (will fail if no API key, but that's expected)
        try:
            generator = CopyGenerator()
            print(f"   ✅ Copy generator initialized")
            return True
        except ValueError as e:
            if "ANTHROPIC_API_KEY" in str(e):
                print(f"   ⚠️  Copy generator ready (API key needed to generate)")
                return True
            else:
                raise
    except Exception as e:
        print(f"   ❌ Copy generator import failed: {e}")
        return False

def check_flask_app():
    """Test Flask app can be imported"""
    print("\n🔍 Testing Flask app...")

    try:
        sys.path.insert(0, 'backend')
        from app import app

        print(f"   ✅ Flask app imported successfully")

        # Check routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected = ['/health', '/scrape', '/generate', '/examples']

        for route in expected:
            if route in routes:
                print(f"   ✅ Route: {route}")
            else:
                print(f"   ❌ Missing route: {route}")
                return False

        return True
    except Exception as e:
        print(f"   ❌ Flask app import failed: {e}")
        return False

def check_frontend():
    """Check if frontend files exist"""
    print("\n🔍 Checking frontend files...")

    files_to_check = [
        'frontend/package.json',
        'frontend/index.html',
        'frontend/src/App.jsx',
        'frontend/src/components/InputForm.jsx',
        'frontend/src/components/CopyPreview.jsx',
    ]

    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_exist = False

    return all_exist

def main():
    """Run all checks"""
    print("=" * 60)
    print("Marketing Copy Generator - Setup Verification")
    print("=" * 60)

    results = []

    results.append(("Python version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Environment", check_env_file()))
    results.append(("Scraper", check_scraper()))
    results.append(("Copy Generator", check_copy_generator()))
    results.append(("Flask App", check_flask_app()))
    results.append(("Frontend", check_frontend()))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED!")
        print("\nYou can now start the application:")
        print("  1. Terminal 1: cd backend && python app.py")
        print("  2. Terminal 2: cd frontend && npm run dev")
        print("  3. Open: http://localhost:3000")
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above and run this script again.")
        print("\nCommon fixes:")
        print("  - Run: pip install -r backend/requirements.txt")
        print("  - Create .env: cp .env.example .env")
        print("  - Add API key to .env file")
        print("  - Run: cd frontend && npm install")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
