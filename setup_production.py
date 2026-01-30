#!/usr/bin/env python3
"""
Production Setup Script for eBay/Vinted Scraping API
"""

import os
import sys
import requests
import base64

def test_current_setup():
    """Test current configuration"""
    print("🔍 Testing Current Setup...")
    
    # Load environment variables
    try:
        with open('.env', 'r') as env_file:
            for line in env_file:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    if key.startswith('export '):
                        key = key[7:]
                    os.environ[key] = value.strip('"')
    except FileNotFoundError:
        print("❌ .env file not found")
        return False
    
    app_id = os.environ.get('EBAY_APP_ID')
    cert_id = os.environ.get('EBAY_CERT_ID')
    
    if not app_id or not cert_id:
        print("❌ Missing eBay credentials in .env file")
        return False
    
    print(f"✅ Credentials loaded: {app_id[:10]}...")
    
    # Determine environment
    if 'SBX' in app_id:
        env_type = "SANDBOX"
        token_url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    else:
        env_type = "PRODUCTION"
        token_url = "https://api.ebay.com/identity/v1/oauth2/token"
    
    print(f"🌐 Environment: {env_type}")
    
    # Test authentication
    try:
        credentials = f"{app_id}:{cert_id}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'scope': 'https://api.ebay.com/oauth/api_scope'
        }
        
        response = requests.post(token_url, headers=headers, data=data, timeout=10)
        
        if response.status_code == 200:
            print("✅ Authentication successful!")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def setup_production_credentials():
    """Guide user through production setup"""
    print("\n🚀 Production Setup Guide")
    print("=" * 50)
    
    print("\n1. Get Production Credentials:")
    print("   Visit: https://developer.ebay.com")
    print("   → Create Account → Application Keys → Add New Application")
    print("   → Choose PRODUCTION environment")
    
    print("\n2. Update Your .env File:")
    print("   Replace SBX with PRD in your credentials:")
    print("   EBAY_APP_ID=\"your-production-app-id\"")
    print("   EBAY_CERT_ID=\"your-production-cert-id\"")
    
    print("\n3. Deploy Options:")
    print("   a) Vercel: vercel --prod")
    print("   b) Docker: docker build -t scraping-api .")
    print("   c) Cloud: Set env vars in your cloud platform")
    
    print("\n4. Test Production:")
    print("   python3 setup_production.py")

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🧪 Testing API Endpoints...")
    
    try:
        # Test Vinted
        response = requests.get("http://localhost:8099/?search=shoes&items_per_page=2", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Vinted API: {data['count']} items found")
        else:
            print(f"❌ Vinted API: {response.status_code}")
    except:
        print("⚠️  Vinted API: Server not running")
    
    try:
        # Test eBay
        response = requests.get("http://localhost:8099/ebay?search=laptop&items_per_page=2", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ eBay API: {data['count']} items found")
        else:
            print(f"❌ eBay API: {response.status_code}")
    except:
        print("⚠️  eBay API: Server not running")

def main():
    print("🎯 eBay/Vinted API Production Setup")
    print("=" * 50)
    
    # Test current setup
    if test_current_setup():
        print("\n✅ Current setup is working!")
        test_api_endpoints()
        
        # Check if using sandbox
        app_id = os.environ.get('EBAY_APP_ID', '')
        if 'SBX' in app_id:
            print("\n⚠️  Currently using SANDBOX credentials")
            setup_production_credentials()
        else:
            print("\n🎉 Using PRODUCTION credentials!")
            print("🚀 Ready for production deployment!")
    else:
        print("\n❌ Setup issues found")
        setup_production_credentials()

if __name__ == "__main__":
    main()
