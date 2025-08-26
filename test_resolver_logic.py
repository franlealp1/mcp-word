#!/usr/bin/env python3
"""
Test the core resolver logic without MCP dependencies.
"""

import os
import sys
import uuid
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

# Copy the core functions we need to test (without MCP dependencies)
TEMP_FILES_DIR = Path("/tmp/mcp_files")
DB_FILE = TEMP_FILES_DIR / "file_registry.db"

def init_temp_storage():
    """Initialize temporary file storage and database."""
    TEMP_FILES_DIR.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    
    # Create table with user_filename for mapping
    conn.execute("""
        CREATE TABLE IF NOT EXISTS temp_files (
            file_id TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            user_filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            expires_at DATETIME NOT NULL,
            download_count INTEGER DEFAULT 0
        )
    """)
    
    # Check if user_filename column exists (for existing databases)
    cursor = conn.execute("PRAGMA table_info(temp_files)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'user_filename' not in columns:
        conn.execute("ALTER TABLE temp_files ADD COLUMN user_filename TEXT")
        conn.execute("UPDATE temp_files SET user_filename = original_filename WHERE user_filename IS NULL")
        conn.execute("UPDATE temp_files SET user_filename = original_filename WHERE user_filename = ''")
    
    conn.execute("CREATE INDEX IF NOT EXISTS idx_user_filename ON temp_files(user_filename)")
    conn.commit()
    conn.close()

def register_temp_file(file_path: str, original_filename: str, user_filename: str, cleanup_hours: int = 24) -> str:
    """Register a temporary file for cleanup and return its public ID."""
    file_id = str(uuid.uuid4())
    created_at = datetime.now()
    expires_at = created_at + timedelta(hours=cleanup_hours)
    
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        INSERT INTO temp_files (file_id, original_filename, user_filename, file_path, created_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (file_id, original_filename, user_filename, file_path, created_at.isoformat(), expires_at.isoformat()))
    conn.commit()
    conn.close()
    
    return file_id

def get_temp_file_by_user_filename(user_filename: str):
    """Get temporary file info by user filename."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("""
        SELECT file_id, original_filename, user_filename, file_path, created_at, expires_at, download_count
        FROM temp_files WHERE user_filename = ? ORDER BY created_at DESC LIMIT 1
    """, (user_filename,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        "file_id": row[0],
        "original_filename": row[1],
        "user_filename": row[2],
        "file_path": row[3],
        "created_at": row[4],
        "expires_at": row[5],
        "download_count": row[6]
    }

def cleanup_expired_files():
    """Remove expired files from filesystem and database."""
    now = datetime.now().isoformat()
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.execute("SELECT file_path FROM temp_files WHERE expires_at < ?", (now,))
    
    expired_files = cursor.fetchall()
    for (file_path,) in expired_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing expired file {file_path}: {e}")
    
    conn.execute("DELETE FROM temp_files WHERE expires_at < ?", (now,))
    conn.commit()
    conn.close()

def resolve_document_path(filename: str):
    """Resolve a filename to actual file path, checking temp files first."""
    # Add .docx if not present
    if not filename.endswith('.docx'):
        filename = filename + '.docx'
    
    # First, check if it's a temp file by user filename
    cleanup_expired_files()  # Clean up first
    temp_file_info = get_temp_file_by_user_filename(filename)
    
    if temp_file_info:
        # Check if file still exists on disk
        if os.path.exists(temp_file_info["file_path"]):
            # Check if not expired
            expires_at = datetime.fromisoformat(temp_file_info["expires_at"])
            if datetime.now() <= expires_at:
                return temp_file_info["file_path"], True
    
    # Fall back to current directory
    current_path = os.path.abspath(filename)
    if os.path.exists(current_path):
        return current_path, False
    
    # File not found anywhere
    raise FileNotFoundError(f"Document '{filename}' not found in temp storage or current directory")

def test_resolver_workflow():
    """Test the resolver workflow simulation."""
    print("🧪 Testing Resolver Workflow")
    print("=" * 50)
    
    try:
        # Step 1: Initialize
        init_temp_storage()
        print("✓ Temp storage initialized")
        
        # Step 2: Create a "document" (simulate create_document_with_download_link)
        filename = "products.docx"
        unique_filename = f"{uuid.uuid4()}_{filename}"
        temp_file_path = TEMP_FILES_DIR / unique_filename
        
        # Create a dummy file
        temp_file_path.write_text("Initial content: Sevilla products")
        print(f"✓ Created temp file: {temp_file_path}")
        
        # Register the file  
        file_id = register_temp_file(str(temp_file_path), filename, filename, 24)
        print(f"✓ Registered file with ID: {file_id}")
        
        # Step 3: Test resolver - should find temp file when we ask for "products.docx"
        print("\\n🔍 Testing resolver...")
        resolved_path, is_temp = resolve_document_path("products.docx")
        print(f"✓ Resolved 'products.docx' to: {resolved_path}")
        print(f"✓ Is temp file: {is_temp}")
        
        # Verify it found the right file
        if str(resolved_path) == str(temp_file_path) and is_temp:
            print("✓ Resolver correctly found temp file!")
        else:
            print("✗ Resolver found wrong file")
            return False
        
        # Step 4: Test file modification (simulate editing tools)
        print("\\n✏️ Testing file modification...")
        content = Path(resolved_path).read_text()
        new_content = content + "\\nAdded: More products"
        Path(resolved_path).write_text(new_content)
        print("✓ File content modified")
        
        # Step 5: Test resolver again - should still find the same file
        resolved_path2, is_temp2 = resolve_document_path("products.docx")
        if str(resolved_path2) == str(resolved_path):
            print("✓ Resolver consistently finds same file")
        else:
            print("✗ Resolver inconsistent")
            return False
        
        # Step 6: Verify modified content
        final_content = Path(resolved_path2).read_text()
        if "More products" in final_content:
            print("✓ File modifications persisted")
        else:
            print("✗ File modifications lost")
            return False
        
        # Step 7: Test download link retrieval
        print("\\n🔗 Testing download link retrieval...")
        temp_file_info = get_temp_file_by_user_filename("products.docx")
        if temp_file_info:
            download_url = f"http://localhost:8000/files/{temp_file_info['file_id']}"
            print(f"✓ Download URL generated: {download_url}")
        else:
            print("✗ Could not retrieve file info for download link")
            return False
        
        # Cleanup test file
        temp_file_path.unlink()
        
        print("\\n" + "=" * 50)
        print("🎉 RESOLVER WORKFLOW TEST SUCCESSFUL!")
        print("\\n✅ Key functionality verified:")
        print("   1. ✓ Temp file creation and registration")
        print("   2. ✓ Smart filename resolution (temp files first)")
        print("   3. ✓ File modification through resolved paths")
        print("   4. ✓ Consistent file resolution across operations")
        print("   5. ✓ Download link generation from user filename")
        
        return True
        
    except Exception as e:
        print(f"\\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the resolver test."""
    success = test_resolver_workflow()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())