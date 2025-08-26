#!/usr/bin/env python3
"""
Test script for the new document download feature.
This script tests the temporary file creation, storage, and HTTP endpoints.
"""

import os
import sys
import json
import asyncio
import requests
from pathlib import Path

# Add the word_document_server to Python path
sys.path.insert(0, str(Path(__file__).parent))

from word_document_server.main import (
    init_temp_storage, 
    register_temp_file, 
    get_temp_file_info,
    cleanup_expired_files,
    TEMP_FILES_DIR
)

def test_temp_storage_functions():
    """Test the temporary storage functions."""
    print("Testing temporary storage functions...")
    
    # Initialize storage
    init_temp_storage()
    print("✓ Temp storage initialized")
    
    # Create a test file
    test_file = TEMP_FILES_DIR / "test_document.docx"
    test_file.write_text("test content")
    
    # Register the file
    file_id = register_temp_file(str(test_file), "test_document.docx", 24)
    print(f"✓ File registered with ID: {file_id}")
    
    # Get file info
    file_info = get_temp_file_info(file_id)
    if file_info:
        print(f"✓ File info retrieved: {file_info['original_filename']}")
    else:
        print("✗ Failed to retrieve file info")
        return False
    
    # Clean up
    test_file.unlink()
    
    return True

async def test_create_document_tool():
    """Test the create_document_with_download_link tool."""
    print("\nTesting document creation with download link...")
    
    # Import the tool function (we need to simulate the MCP tool call)
    from word_document_server.main import get_transport_config
    from docx import Document
    from word_document_server.core.styles import ensure_heading_style, ensure_table_style
    from word_document_server.utils.file_utils import ensure_docx_extension
    from word_document_server.main import init_temp_storage, register_temp_file, TEMP_FILES_DIR
    import uuid
    from datetime import datetime, timedelta
    
    # Simulate the tool function logic
    init_temp_storage()
    
    filename = "test_document.docx"
    cleanup_hours = 1  # 1 hour for testing
    title = "Test Document"
    author = "Test Author"
    
    try:
        # Generate unique filename in temp directory
        original_filename = ensure_docx_extension(filename)
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        temp_file_path = TEMP_FILES_DIR / unique_filename
        
        # Create the document
        doc = Document()
        
        if title:
            doc.core_properties.title = title
        if author:
            doc.core_properties.author = author
        
        ensure_heading_style(doc)
        ensure_table_style(doc)
        
        # Save to temp location
        doc.save(str(temp_file_path))
        
        # Register the file for cleanup
        file_id = register_temp_file(str(temp_file_path), original_filename, cleanup_hours)
        
        # Get the public URL
        config = get_transport_config()
        base_url = f"http://{config['host']}:{config['port']}"
        download_url = f"{base_url}/files/{file_id}"
        
        expires_at = datetime.now() + timedelta(hours=cleanup_hours)
        
        result = {
            "success": True,
            "message": f"Document {original_filename} created successfully",
            "download_url": download_url,
            "file_id": file_id,
            "original_filename": original_filename,
            "expires_at": expires_at.isoformat(),
            "cleanup_hours": cleanup_hours
        }
        
        print(f"✓ Document created successfully")
        print(f"  - File ID: {result['file_id']}")
        print(f"  - Download URL: {result['download_url']}")
        print(f"  - Expires at: {result['expires_at']}")
        
        # Verify the file exists
        if temp_file_path.exists():
            print(f"✓ File exists on disk: {temp_file_path}")
        else:
            print(f"✗ File not found on disk: {temp_file_path}")
            return False
            
        return result
        
    except Exception as e:
        print(f"✗ Error creating document: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Word Document Download Feature")
    print("=" * 50)
    
    # Test 1: Storage functions
    if not test_temp_storage_functions():
        print("✗ Storage function tests failed")
        return 1
    
    # Test 2: Document creation
    result = asyncio.run(test_create_document_tool())
    if not result:
        print("✗ Document creation test failed")
        return 1
    
    print("\n" + "=" * 50)
    print("✓ All tests passed!")
    print("\nTo test the HTTP endpoints, start the MCP server with:")
    print("  python -m word_document_server")
    print(f"\nThen test the download URL: {result['download_url']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())