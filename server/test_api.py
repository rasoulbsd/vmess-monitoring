#!/usr/bin/env python3
"""
Test script for VMess Monitoring API
"""

import requests
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.config import Config


def test_api_key_auth():
    """Test API key authentication"""
    print("Testing API Key Authentication...")
    
    url = f"http://{Config.SERVER_HOST}:{Config.SERVER_PORT}/api/test-vmess"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": Config.API_KEY
    }
    data = {
        "vmess_link": "vmess://example-link",
        "dest_url": "https://www.gstatic.com/generate_204"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


def test_basic_auth():
    """Test basic authentication"""
    print("\nTesting Basic Authentication...")
    
    url = f"http://{Config.SERVER_HOST}:{Config.SERVER_PORT}/api/test-vmess-basic"
    auth = (Config.USERNAME, Config.PASSWORD)
    data = {
        "vmess_link": "vmess://example-link",
        "dest_url": "https://www.gstatic.com/generate_204"
    }
    
    try:
        response = requests.post(url, auth=auth, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


def test_health_endpoints():
    """Test health check endpoints"""
    print("\nTesting Health Endpoints...")
    
    base_url = f"http://{Config.SERVER_HOST}:{Config.SERVER_PORT}"
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"Root endpoint - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health endpoint - Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("VMess Monitoring API Test Script")
    print("=" * 40)
    
    test_health_endpoints()
    test_api_key_auth()
    test_basic_auth()
    
    print("\nTest completed!") 