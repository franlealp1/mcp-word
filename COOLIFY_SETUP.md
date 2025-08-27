# Coolify Environment Variables Setup

## 🔧 Required Environment Variables for Public Download URLs

To fix the unreachable URLs (like `http://0.0.0.0:8000/files/{id}`), you need to add these environment variables in your Coolify deployment:

### Environment Variables to Add:

| Variable | Value | Description |
|----------|--------|-------------|
| `PUBLIC_DOMAIN` | `your-mcp-domain.coolify.app` | Your public domain (without protocol) |
| `USE_HTTPS` | `true` | Use HTTPS for download URLs (recommended) |

### Example Configuration:

```env
PUBLIC_DOMAIN=your-mcp-server.coolify-domain.com
USE_HTTPS=true
```

**Result**: URLs will be generated as `https://your-mcp-server.coolify-domain.com/files/{id}` ✅

## 🚀 How to Add Variables in Coolify:

1. **Go to your Coolify dashboard**
2. **Select your MCP application**  
3. **Navigate to "Environment Variables" tab**
4. **Add the variables:**
   - Variable: `PUBLIC_DOMAIN`
   - Value: `your-actual-domain.coolify.app` (replace with your real domain)
   - Variable: `USE_HTTPS`  
   - Value: `true`
5. **Save and redeploy the application**

## 🎯 Finding Your Public Domain:

Your public domain is shown in Coolify under:
- Application → **"Domains"** section
- Usually looks like: `https://random-words-123.coolify-domain.com`
- **Use only the domain part** (without `https://`)

**Example**:
- Full URL: `https://mcp-word-server-abc123.coolify.example.com`
- PUBLIC_DOMAIN value: `mcp-word-server-abc123.coolify.example.com`

## ✅ After Setup:

Your download URLs will change from:
- ❌ **Before**: `http://0.0.0.0:8000/files/abc123` (unreachable)
- ✅ **After**: `https://your-domain.coolify.app/files/abc123` (working!)

## 🧪 Testing:

1. **Redeploy** your application after adding variables
2. **Test** the `create_document_with_download_link` tool
3. **Check** that URLs now use your public domain
4. **Verify** the link works in a browser

## 🔧 Fallback Behavior:

If you don't set these variables:
- URLs will fall back to `http://0.0.0.0:8000/files/{id}` (for backwards compatibility)
- This is useful for local development but won't work in production

## ⚠️ Important Notes:

- **Don't include protocol** in PUBLIC_DOMAIN (no `https://`)
- **USE_HTTPS defaults to true** - only set to `false` for local testing
- **Redeploy required** - changes take effect on next deployment
- **Test in browser** - make sure the generated URLs actually work