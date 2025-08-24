# n8n Integration Guide for Office Word MCP Server

This guide explains how to connect and use the Office Word MCP Server with n8n for automated document processing workflows.

## Quick Start

### 1. Deploy the MCP Server

#### Option A: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/franlealp1/mcp-word
cd Office-Word-MCP-Server

# Create directories for document storage
mkdir documents output

# Start the server
docker-compose up -d
```

#### Option B: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MCP_TRANSPORT=streamable-http
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
export MCP_PATH=/mcp

# Start the server
python -m word_document_server.main
```

### 2. Test the Connection

The server will be available at: `http://your-server-ip:8000/mcp`

## n8n Workflow Examples

### Example 1: Create a Document from Form Data

```json
{
  "workflow": {
    "nodes": [
      {
        "id": "form-trigger",
        "type": "n8n-nodes-base.webhook",
        "position": [240, 300],
        "parameters": {
          "httpMethod": "POST",
          "path": "create-document"
        }
      },
      {
        "id": "create-document",
        "type": "n8n-nodes-base.httpRequest",
        "position": [460, 300],
        "parameters": {
          "method": "POST",
          "url": "http://your-server-ip:8000/mcp",
          "sendHeaders": true,
          "headerParameters": {
            "parameters": [
              {
                "name": "Content-Type",
                "value": "application/json"
              }
            ]
          },
          "sendBody": true,
          "bodyParameters": {
            "parameters": [
              {
                "name": "jsonrpc",
                "value": "2.0"
              },
              {
                "name": "id",
                "value": "1"
              },
              {
                "name": "method",
                "value": "tools/call"
              },
              {
                "name": "params",
                "value": "={{ { \"name\": \"create_document\", \"arguments\": { \"filename\": $json.filename, \"title\": $json.title, \"author\": $json.author } } }}"
              }
            ]
          }
        }
      }
    ]
  }
}
```

### Example 2: Add Content to Existing Document

```json
{
  "workflow": {
    "nodes": [
      {
        "id": "add-content",
        "type": "n8n-nodes-base.httpRequest",
        "parameters": {
          "method": "POST",
          "url": "http://your-server-ip:8000/mcp",
          "sendHeaders": true,
          "headerParameters": {
            "parameters": [
              {
                "name": "Content-Type",
                "value": "application/json"
              }
            ]
          },
          "sendBody": true,
          "bodyParameters": {
            "parameters": [
              {
                "name": "jsonrpc",
                "value": "2.0"
              },
              {
                "name": "id",
                "value": "1"
              },
              {
                "name": "method",
                "value": "tools/call"
              },
              {
                "name": "params",
                "value": "={{ { \"name\": \"add_heading\", \"arguments\": { \"filename\": $json.filename, \"text\": $json.heading, \"level\": $json.level } } }}"
              }
            ]
          }
        }
      }
    ]
  }
}
```

### Example 3: Process Document and Extract Information

```json
{
  "workflow": {
    "nodes": [
      {
        "id": "get-document-info",
        "type": "n8n-nodes-base.httpRequest",
        "parameters": {
          "method": "POST",
          "url": "http://your-server-ip:8000/mcp",
          "sendHeaders": true,
          "headerParameters": {
            "parameters": [
              {
                "name": "Content-Type",
                "value": "application/json"
              }
            ]
          },
          "sendBody": true,
          "bodyParameters": {
            "parameters": [
              {
                "name": "jsonrpc",
                "value": "2.0"
              },
              {
                "name": "id",
                "value": "1"
              },
              {
                "name": "method",
                "value": "tools/call"
              },
              {
                "name": "params",
                "value": "={{ { \"name\": \"get_document_info\", \"arguments\": { \"filename\": $json.filename } } }}"
              }
            ]
          }
        }
      }
    ]
  }
}
```

## Available MCP Tools for n8n

### Document Management
- `create_document(filename, title, author)` - Create new Word document
- `copy_document(source_filename, destination_filename)` - Copy existing document
- `get_document_info(filename)` - Get document metadata
- `get_document_text(filename)` - Extract all text from document
- `list_available_documents(directory)` - List documents in directory
- `convert_to_pdf(filename, output_filename)` - Convert to PDF

### Content Addition
- `add_heading(filename, text, level)` - Add heading with specified level
- `add_paragraph(filename, text, style)` - Add paragraph with optional styling
- `add_table(filename, rows, cols, data)` - Create table with data
- `add_picture(filename, image_path, width)` - Insert image
- `add_page_break(filename)` - Add page break
- `add_footnote(filename, text)` - Add footnote

### Text Formatting
- `format_text(filename, paragraph_index, start_pos, end_pos, bold, italic, underline, color, font_size, font_name)` - Format specific text
- `search_and_replace(filename, find_text, replace_text)` - Find and replace text
- `create_custom_style(filename, style_name, bold, italic, font_size, font_name, color, base_style)` - Create custom style

### Table Operations
- `format_table(filename, table_index, has_header_row, border_style, shading)` - Format table appearance
- `modify_table_cell(filename, table_index, row, column, content)` - Modify specific table cell

### Document Protection
- `add_password_protection(filename, password)` - Add password protection
- `add_restricted_editing(filename, allowed_editing_level)` - Restrict editing
- `add_digital_signature(filename, certificate_path)` - Add digital signature

## Error Handling in n8n

### Handle MCP Server Errors

```json
{
  "workflow": {
    "nodes": [
      {
        "id": "mcp-request",
        "type": "n8n-nodes-base.httpRequest",
        "parameters": {
          "method": "POST",
          "url": "http://your-server-ip:8000/mcp",
          "options": {
            "timeout": 30000
          }
        }
      },
      {
        "id": "error-handler",
        "type": "n8n-nodes-base.if",
        "parameters": {
          "conditions": {
            "options": {
              "caseSensitive": true,
              "leftValue": "",
              "typeValidation": "strict"
            },
            "conditions": [
              {
                "id": "error-check",
                "leftValue": "={{ $json.error }}",
                "rightValue": "",
                "operator": {
                  "type": "exists"
                }
              }
            ],
            "combinator": "and"
          }
        }
      }
    ]
  }
}
```

## Best Practices

### 1. Document Storage
- Use consistent file naming conventions
- Store documents in organized directory structure
- Implement backup strategies for important documents

### 2. Error Handling
- Always check for MCP server response errors
- Implement retry logic for network issues
- Log all document operations for audit trails

### 3. Performance
- Use batch operations when possible
- Implement caching for frequently accessed documents
- Monitor server resource usage

### 4. Security
- Use HTTPS in production environments
- Implement proper authentication if needed
- Validate all input data before processing

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if MCP server is running
   - Verify port 8000 is accessible
   - Check firewall settings

2. **Document Not Found**
   - Verify file paths are correct
   - Check file permissions
   - Ensure documents directory is mounted (Docker)

3. **Timeout Errors**
   - Increase timeout settings in n8n
   - Check server performance
   - Monitor resource usage

### Debug Mode

Enable debug logging on the MCP server:

```bash
export MCP_DEBUG=1
python -m word_document_server.main
```

## Advanced Usage

### Batch Document Processing

Create workflows that process multiple documents:

```json
{
  "workflow": {
    "nodes": [
      {
        "id": "list-documents",
        "type": "n8n-nodes-base.httpRequest",
        "parameters": {
          "method": "POST",
          "url": "http://your-server-ip:8000/mcp",
          "sendBody": true,
          "bodyParameters": {
            "parameters": [
              {
                "name": "jsonrpc",
                "value": "2.0"
              },
              {
                "name": "id",
                "value": "1"
              },
              {
                "name": "method",
                "value": "tools/call"
              },
              {
                "name": "params",
                "value": "={{ { \"name\": \"list_available_documents\", \"arguments\": { \"directory\": \"./documents\" } } }}"
              }
            ]
          }
        }
      },
      {
        "id": "process-each",
        "type": "n8n-nodes-base.splitInBatches",
        "parameters": {
          "batchSize": 1
        }
      }
    ]
  }
}
```

This integration allows you to automate complex document workflows in n8n, from simple document creation to advanced batch processing and formatting operations.
