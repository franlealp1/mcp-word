# Coolify Deployment Guide for Word MCP Server

## Quick Start

1. **Clone to your Coolify server**:
   ```bash
   git clone https://github.com/franlealp1/mcp-word
   cd Office-Word-MCP-Server
   ```

2. **Deploy with Coolify**:
   - Create new service in Coolify
   - Select "Nixpacks" build pack
   - Point to this repository
   - Coolify will use the `nixpacks.toml` configuration

## Service Configuration

### Coolify Settings
- **Build Pack**: Nixpacks
- **Port**: 8000
- **Health Check Path**: `/mcp`
- **Domain**: `word-mcp.yourdomain.com` (optional)

### Environment Variables
Environment variables are pre-configured in `nixpacks.toml`. No additional configuration needed in Coolify.

```bash
# Automatically set by nixpacks.toml:
MCP_TRANSPORT=streamable-http
MCP_HOST=0.0.0.0
MCP_PORT=8000
MCP_PATH=/mcp
FASTMCP_LOG_LEVEL=INFO
```

### Resource Requirements
- **Memory**: 512MB limit, 256MB reserved
- **CPU**: 0.5 cores limit, 0.25 cores reserved
- **Storage**: Persistent volumes for document storage

## n8n Integration

### MCP Client Node Configuration

1. **Add MCP Client Tool Node** to your n8n workflow

2. **Configure Connection**:
   - **Transport Type**: HTTP Streamable
   - **URL**: `http://word-mcp-server:8000/mcp` (internal) or `https://word-mcp.yourdomain.com/mcp` (external)
   - **Authentication**: None (internal network)

3. **Available Tools**:
   ```json
   {
     "document_tools": [
       "create_document",
       "copy_document", 
       "get_document_info",
       "get_document_text",
       "list_available_documents"
     ],
     "content_tools": [
       "add_paragraph",
       "add_heading",
       "add_table",
       "add_picture",
       "search_and_replace"
     ],
     "format_tools": [
       "format_text",
       "create_custom_style",
       "format_table"
     ],
     "protection_tools": [
       "protect_document",
       "unprotect_document"
     ]
   }
   ```

### Example n8n Workflow

```json
{
  "nodes": [
    {
      "name": "Create Document",
      "type": "@n8n/n8n-nodes-langchain.toolMcp",
      "parameters": {
        "tool": "create_document",
        "toolInput": {
          "filename": "report.docx",
          "title": "Monthly Report",
          "author": "n8n Workflow"
        }
      }
    },
    {
      "name": "Add Content",
      "type": "@n8n/n8n-nodes-langchain.toolMcp", 
      "parameters": {
        "tool": "add_heading",
        "toolInput": {
          "filename": "report.docx",
          "text": "Executive Summary",
          "level": 1
        }
      }
    }
  ]
}
```


curl -X POST http://localhost:8000/mcp -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream"  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

## Networking

### Internal Network (Recommended)
If n8n and Word MCP server are on the same Coolify instance:
- **URL**: `http://word-mcp-server:8000/mcp`
- **No external domain needed**
- **Better security and performance**

### External Access
If accessing from external n8n:
- **Configure domain in Coolify**
- **URL**: `https://word-mcp.yourdomain.com/mcp`
- **Consider adding authentication if public**

## Monitoring

### Health Checks
- **Endpoint**: `GET /mcp`
- **Expected**: 200 OK response
- **Coolify**: Auto-configured health checks

### Logs
```bash
# View logs in Coolify dashboard or CLI
coolify logs word-mcp-server
```

### Metrics
- **Memory usage**: Monitor for document processing spikes
- **CPU usage**: Usually low except during document operations
- **Disk usage**: Monitor document storage volume

## Troubleshooting

### Common Issues

1. **Connection Refused**:
   - Check if service is running: `docker ps`
   - Verify port 8000 is exposed
   - Check health check endpoint

2. **n8n Can't Connect**:
   - Verify MCP Client node configuration
   - Test with curl: `curl http://word-mcp-server:8000/mcp`
   - Check network connectivity between services

3. **Document Operations Fail**:
   - Verify volume permissions
   - Check LibreOffice installation in container
   - Review server logs for errors

### Debug Mode
Enable detailed logging:
```bash
# In Coolify environment variables
FASTMCP_LOG_LEVEL=DEBUG
```

## Security Considerations

1. **Internal Network**: Keep MCP server on internal network when possible
2. **File Access**: Server runs as non-root user (`mcp`)
3. **Document Storage**: Persistent volumes with proper permissions
4. **No Authentication**: Add reverse proxy with auth if external access needed

## Scaling

- **Horizontal**: Deploy multiple instances behind load balancer
- **Vertical**: Increase memory/CPU limits for heavy document processing
- **Storage**: Use external storage for document persistence across instances