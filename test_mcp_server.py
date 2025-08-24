#!/usr/bin/env python3
"""
Test script to verify MCP server functionality and debug schema issues.
"""

import asyncio
import json
import aiohttp
import sys

async def test_mcp_server():
    """Test the MCP server endpoints and tool schemas."""
    
    # Your MCP server URL from n8n
    base_url = "http://31992d3c0a5f:8000"
    mcp_path = "/mcp"
    
    print(f"Testing MCP server at: {base_url}{mcp_path}")
    
    try:
        async with aiohttp.ClientSession() as session:
            
            # Test 1: Check if server is running
            print("\n1. Testing server connectivity...")
            try:
                async with session.get(f"{base_url}/health", timeout=5) as response:
                    print(f"   Health check status: {response.status}")
            except Exception as e:
                print(f"   Health check failed: {e}")
            
            # Test 2: Get tools list (if available)
            print("\n2. Testing tools endpoint...")
            try:
                async with session.post(f"{base_url}{mcp_path}", 
                                       json={"jsonrpc": "2.0", "method": "tools/list", "id": 1},
                                       timeout=10) as response:
                    if response.status == 200:
                        tools_data = await response.json()
                        print(f"   Tools response: {json.dumps(tools_data, indent=2)}")
                    else:
                        print(f"   Tools endpoint failed: {response.status}")
            except Exception as e:
                print(f"   Tools test failed: {e}")
            
            # Test 3: Test create_document tool call
            print("\n3. Testing create_document tool...")
            test_payload = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": "create_document",
                    "arguments": {
                        "filename": "test_hola.docx"
                    }
                },
                "id": 2
            }
            
            try:
                async with session.post(f"{base_url}{mcp_path}", 
                                       json=test_payload,
                                       timeout=10) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"   Create document response: {json.dumps(result, indent=2)}")
                    else:
                        print(f"   Create document failed: {response.status}")
                        error_text = await response.text()
                        print(f"   Error details: {error_text}")
            except Exception as e:
                print(f"   Create document test failed: {e}")
                
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
    
    return True

def main():
    """Main function to run the test."""
    print("MCP Server Test Script")
    print("=" * 50)
    
    # Run the async test
    success = asyncio.run(test_mcp_server())
    
    if success:
        print("\n✅ Test completed successfully")
    else:
        print("\n❌ Test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
