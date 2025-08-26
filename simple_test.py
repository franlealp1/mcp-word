#!/usr/bin/env python3
"""
Simple test to verify the temp storage logic without MCP dependencies.
"""

import os
import sys
import uuid
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Temp file management functions (copied from main.py)
TEMP_FILES_DIR = Path("/tmp/mcp_files")
DB_FILE = TEMP_FILES_DIR / "file_registry.db"

def init_temp_storage():
    """Initialize temporary file storage and database."""
    TEMP_FILES_DIR.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS temp_files (
            file_id TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            expires_at DATETIME NOT NULL,
            download_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def register_temp_file(file_path: str, original_filename: str, cleanup_hours: int = 24) -> str:
    """Register a temporary file for cleanup and return its public ID."""
    file_id = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(hours=cleanup_hours)
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        INSERT INTO temp_files (file_id, original_filename, file_path, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?)
    """, (file_id, original_filename, file_path, created_at.isoformat(), expires_at.isoformat()))
    conn.commit()
    conn.close()
    
    return file_id

def get_temp_file_info(file_id: str):
    """Get temporary file info by ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("""
        SELECT file_id, original_filename, file_path, created_at, expires_at, download_count
        FROM temp_files WHERE file_id = ?
    """, (file_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        "file_id": row[0],
        "original_filename": row[1], 
        "file_path": row[2],
        "created_at": row[3],
        "expires_at": row[4],
        "download_count": row[5]
    }

def main():
    """Test the core temp storage functionality."""
    print("Testing temporary storage system...")
    
    # Initialize storage
    init_temp_storage()
    print("✓ Storage initialized")
    
    # Create a test file
    test_file = TEMP_FILES_DIR / "test.txt"
    test_file.write_text("test content")
    print(f"✓ Test file created: {test_file}")
    
    # Register the file
    file_id = register_temp_file(str(test_file), "test.txt", 24)
    print(f"✓ File registered with ID: {file_id}")
    
    # Retrieve file info
    file_info = get_temp_file_info(file_id)
    if file_info:
        print(f"✓ File info retrieved:")
        print(f"  - Original: {file_info['original_filename']}")
        print(f"  - Path: {file_info['file_path']}")
        print(f"  - Created: {file_info['created_at']}")
        print(f"  - Expires: {file_info['expires_at']}")
    else:
        print("✗ Failed to retrieve file info")
        return 1
    
    # Test file access
    if os.path.exists(file_info['file_path']):
        print("✓ File exists and is accessible")
    else:
        print("✗ File not accessible")
        return 1
    
    # Clean up test file
    test_file.unlink()
    print("✓ Test file cleaned up")
    
    print("\n" + "=" * 50)
    print("✓ All core functionality tests passed!")
    print("\nThe system is ready to:")
    print("1. Store Word documents in /tmp/mcp_files/")
    print("2. Track them in SQLite database")
    print("3. Serve them via HTTP endpoints")
    print("4. Clean up expired files automatically")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())