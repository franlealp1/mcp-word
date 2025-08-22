# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a Model Context Protocol (MCP) server for Microsoft Word document manipulation. The codebase follows a modular architecture with clear separation of concerns:

### Core Structure
- **`word_document_server/`**: Main package containing the MCP server implementation
  - **`main.py`**: Central entry point with transport configuration and tool registration
  - **`core/`**: Core business logic modules (styles, tables, footnotes, protection)
  - **`tools/`**: MCP tool implementations organized by functionality
  - **`utils/`**: Shared utilities for document and file operations

### Key Components
- **Transport Support**: Supports stdio, streamable-http, and SSE transports via FastMCP
- **Tool Categories**: 
  - Document tools (create, copy, info, text extraction)
  - Content tools (paragraphs, headings, tables, images)
  - Format tools (styling, text formatting)
  - Protection tools (password protection, restricted editing)
  - Footnote tools (footnotes and endnotes)
  - Extended tools (advanced content manipulation)

### Dependencies
- `python-docx`: Core Word document manipulation
- `fastmcp`: MCP server framework (2.8.1+)
- `msoffcrypto-tool`: Document protection/unprotection
- `docx2pdf`: PDF conversion

## Development Commands

### Setup and Installation
```bash
# Setup with virtual environment (recommended for development)
python setup_mcp.py

# Manual setup
pip install -r requirements.txt

# Install from PyPI (for end users)
pip install office-word-mcp-server
```

### Running the Server
```bash
# Default stdio transport
python word_mcp_server.py

# With specific transport (set environment variables)
export MCP_TRANSPORT=streamable-http
export MCP_HOST=127.0.0.1
export MCP_PORT=8000
python word_mcp_server.py
```

### Testing
No formal test framework is currently configured. Test by:
1. Running the server with Claude Desktop
2. Manual testing with MCP tools
3. Enabling debug logging: `export MCP_DEBUG=1`

### Linting and Type Checking
No specific lint/typecheck commands are configured in this codebase.

## Key Implementation Details

### Tool Registration Pattern
All MCP tools are registered in `word_document_server/main.py:register_tools()` using FastMCP decorators. Each tool function wraps the corresponding implementation from the tools modules.

### Document Loading Pattern
Most tools follow this pattern:
1. Load document using `python-docx`
2. Perform operations
3. Save document
4. Return success/error message

### Error Handling
- Tools return descriptive error messages for common issues
- Missing styles are handled gracefully (created or direct formatting applied)
- File permission issues are caught and reported

### Transport Configuration
The server supports multiple transports configured via environment variables:
- `MCP_TRANSPORT`: stdio (default), streamable-http, sse
- `MCP_HOST`, `MCP_PORT`: For HTTP/SSE transports
- `MCP_PATH`, `MCP_SSE_PATH`: Transport-specific paths

### Style System
The codebase extensively uses Word's style system:
- Automatic style detection and creation
- Fallback to direct formatting when styles unavailable
- Custom style creation support

## Working with This Codebase

### Adding New Tools
1. Implement core functionality in appropriate `core/` module
2. Create tool wrapper in relevant `tools/` module
3. Register tool in `main.py:register_tools()`
4. Follow existing parameter and return value patterns

### Modifying Document Operations
- Core document logic lives in `core/` modules
- Utility functions are in `utils/` modules  
- Always save documents after modifications
- Handle edge cases (missing styles, protected documents)

### Testing Changes
- Use `setup_mcp.py` to configure test environment
- Test with Claude Desktop integration
- Verify both stdio and HTTP transports work
- Test with various document types and styles