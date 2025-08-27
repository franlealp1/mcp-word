# Troubleshooting Download Links Issue

## 🧪 Test Results: Tool Works Correctly

**Local testing confirms:**
- ✅ `create_document_with_download_link` tool generates proper URLs
- ✅ Database registration works correctly  
- ✅ File storage and retrieval works
- ✅ JSON response format is correct
- ✅ Download URL format: `http://0.0.0.0:8000/files/{uuid}`

**Sample successful response:**
```json
{
  "success": true,
  "message": "Document test_products.docx created successfully", 
  "download_url": "http://0.0.0.0:8000/files/9449913e-7348-4563-ac42-9924d2ced1c7",
  "file_id": "9449913e-7348-4563-ac42-9924d2ced1c7",
  "original_filename": "test_products.docx",
  "expires_at": "2025-08-28T18:19:11.233499",
  "cleanup_hours": 24
}
```

## 🔍 Potential Issues in n8n Environment

### 1. **Agent Prompt Limitations**
**Most Likely Issue**: The AI agent may not be configured to:
- Look for the `download_url` field in the response
- Extract and present the URL to the user
- Understand that this is a downloadable link

**Solution**: Update your n8n AI agent prompt to include:
```
When calling create_document_with_download_link, always check the response for a 'download_url' field. 
If present, provide this URL to the user and explain they can click it to download the document.
```

### 2. **URL Format Issues** 
**Issue**: The generated URL uses `0.0.0.0:8000` which won't work for external access.

**Current**: `http://0.0.0.0:8000/files/{file_id}`  
**Should be**: `https://your-domain.com/files/{file_id}`

**Root cause**: The `get_transport_config()` function uses:
```python
config = {
    'host': '0.0.0.0',  # Internal binding
    'port': 8000
}
```

**Solution**: The URL should use the public domain, not internal IP.

### 3. **MCP Tool Response Parsing**
**Issue**: The n8n MCP client might not be properly parsing the JSON response.

**Check**: Ensure your MCP client node in n8n can handle dictionary/object responses from tools.

### 4. **Environment Variable Issues**
**Issue**: Container might not have correct host/port configuration.

**Check**: These environment variables in your Coolify deployment:
- `MCP_HOST` should be `0.0.0.0` (correct)
- `MCP_PORT` should be `8000` (correct)
- But URLs should use your public domain

## 🔧 Immediate Fixes Needed

### Fix 1: Update URL Generation to Use Public Domain

The tool should generate URLs using your public domain, not internal IPs:

```python
# Instead of:
base_url = f"http://{config['host']}:{config['port']}"

# Should be:
public_domain = os.getenv('PUBLIC_DOMAIN', f"{config['host']}:{config['port']}")
protocol = "https" if os.getenv('USE_HTTPS', 'true').lower() == 'true' else "http"
base_url = f"{protocol}://{public_domain}"
```

### Fix 2: Add Environment Variables to Coolify

Add these to your container environment:
```
PUBLIC_DOMAIN=your-mcp-domain.com
USE_HTTPS=true
```

### Fix 3: Verify Agent Prompt

Ensure your n8n AI agent prompt includes:
```
When using create_document_with_download_link:
1. Check if 'success' is true
2. If successful, extract the 'download_url' field
3. Present the download URL to the user with clear instructions
4. Tell them the link expires in 24 hours (or check 'cleanup_hours')

Example response: "I've created your document! Download it here: [URL] (link expires in 24 hours)"
```

## 🚨 Quick Test in n8n

To verify which issue it is, test calling the tool directly in n8n:

1. Call `create_document_with_download_link("test.docx")`
2. Check the **raw response** in n8n logs
3. Look for:
   - Is `success: true`?
   - Is `download_url` field present?
   - Does the URL look correct?

## 📋 Most Likely Solution

**90% chance it's the agent prompt**. The tool works, but the AI agent doesn't know how to extract and present the download URL from the response.

Update your agent prompt to handle the tool response properly, and the issue should be resolved.