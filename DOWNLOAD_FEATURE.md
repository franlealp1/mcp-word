# Document Download Feature

This feature allows the MCP server to create Word documents in temporary storage and return public download links, perfect for n8n workflows where users need to access generated documents through chat interfaces.

## Overview

The system creates Word documents in a temporary folder (`/tmp/mcp_files/`), tracks them in a SQLite database, and provides HTTP endpoints for downloading. Files are automatically cleaned up after a configurable period (default: 24 hours).

## New MCP Tool

### `create_document_with_download_link`

Creates a Word document in temporary storage and returns a public download link.

**Parameters:**
- `filename` (str): Name of the document to create
- `cleanup_hours` (int, optional): Hours after which file is auto-deleted (default: 24)
- `title` (str, optional): Document title metadata
- `author` (str, optional): Document author metadata

**Returns:**
```json
{
  "success": true,
  "message": "Document test.docx created successfully",
  "download_url": "http://your-domain.com/files/abc123-def456-789",
  "file_id": "abc123-def456-789",
  "original_filename": "test.docx",
  "expires_at": "2024-08-27T18:00:00",
  "cleanup_hours": 24
}
```

## HTTP Endpoints

### `GET /files/{file_id}`
Downloads the document file.
- Returns: Word document with proper headers
- Status: 404 if not found, 410 if expired

### `GET /files/{file_id}/info`
Gets file metadata without downloading.
- Returns: JSON with file info and status

### `POST /cleanup`
Manually triggers cleanup of expired files.
- Returns: Success/error message

## Usage in n8n Workflows

1. **MCP Node**: Call `create_document_with_download_link`
2. **Extract URL**: Get `download_url` from response
3. **Chat Response**: Send URL to user for direct download

The URL works directly in browsers and chat clients, allowing end users to download documents without additional authentication.

## Technical Details

### Storage Structure
```
/tmp/mcp_files/
├── file_registry.db          # SQLite database
├── uuid1_document1.docx      # Temporary files
└── uuid2_document2.docx
```

### Database Schema
```sql
CREATE TABLE temp_files (
    file_id TEXT PRIMARY KEY,           -- Public UUID
    original_filename TEXT NOT NULL,    -- Original filename
    file_path TEXT NOT NULL,            -- Full path to file
    created_at DATETIME NOT NULL,       -- Creation timestamp
    expires_at DATETIME NOT NULL,       -- Expiration timestamp
    download_count INTEGER DEFAULT 0    -- Download counter
);
```

### Cleanup Process
- **Automatic**: Background thread runs every hour
- **On-demand**: Cleanup runs before serving each file
- **Manual**: POST to `/cleanup` endpoint
- **On-exit**: Cleanup thread stops gracefully

### Security Features
- UUID-based file IDs (not guessable)
- File expiration enforcement
- Path traversal protection
- No directory listing

## Configuration

The feature uses existing MCP server configuration:
- Uses the same host/port as the MCP server
- Works with all transport types (streamable-http recommended)
- No additional dependencies required

## Deployment Notes

### Coolify/Docker
- Files stored in container's `/tmp/mcp_files/`
- URLs automatically work through Coolify's reverse proxy
- No additional port configuration needed

### URLs Format
- Internal: `http://container:8000/files/{file_id}`
- Public: `https://your-domain.com/files/{file_id}`

## Error Handling

The system gracefully handles:
- File creation failures
- Database errors  
- Expired file access
- Missing files
- Permission issues

All errors return appropriate HTTP status codes and JSON error messages.

## Testing

Run the test suite:
```bash
python simple_test.py
```

This verifies:
- Temp storage initialization
- File registration
- Database operations
- File access permissions