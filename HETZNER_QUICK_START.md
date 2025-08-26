# 🚀 **Quick Start: Hetzner Storage Integration**

## ⚡ **Setup Rápido (1.5 horas)**

### **Step 1: Verificar Hetzner Storage (10 min)**
```bash
# Obtener la información de tu bucket de Hetzner:
# - Access Key ID
# - Secret Access Key  
# - Endpoint URL (ej: https://fsn1.your-objectstorage.com)
# - Bucket Name
# - Region (ej: fsn1)
```

### **Step 2: Variables de Entorno en Coolify (5 min)**
```bash
# Agregar en tu MCP server container:
HETZNER_ACCESS_KEY_ID=tu-access-key-aqui
HETZNER_SECRET_ACCESS_KEY=tu-secret-key-aqui  
HETZNER_ENDPOINT_URL=https://fsn1.your-objectstorage.com
HETZNER_REGION=fsn1
HETZNER_BUCKET_NAME=tu-bucket-name
```

### **Step 3: Actualizar MCP Server (1 hora)**

**3.1 Agregar boto3 a requirements.txt:**
```bash
boto3>=1.34.0
```

**3.2 Agregar tools al main.py:**
```python
# Agregar después de las importaciones existentes
import boto3
from botocore.exceptions import ClientError
import uuid
import json
from datetime import datetime, timedelta

# Agregar estos dos nuevos tools dentro de register_tools():

@mcp.tool()
async def upload_document_to_cloud(filename: str, expiration_hours: int = 24) -> str:
    """Upload an existing document to Hetzner cloud storage and return download URL."""
    filename = ensure_docx_extension(filename)
    
    if not os.path.exists(filename):
        return json.dumps({"status": "error", "message": f"Document {filename} does not exist"})
    
    try:
        # Initialize S3-compatible client for Hetzner
        s3_client = boto3.client('s3',
            aws_access_key_id=os.getenv('HETZNER_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('HETZNER_SECRET_ACCESS_KEY'),
            endpoint_url=os.getenv('HETZNER_ENDPOINT_URL'),
            region_name=os.getenv('HETZNER_REGION', 'fsn1')
        )
        
        # Generate unique key
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        file_key = f"documents/{timestamp}_{unique_id}_{filename}"
        bucket_name = os.getenv('HETZNER_BUCKET_NAME')
        
        # Upload file
        with open(filename, 'rb') as f:
            s3_client.upload_fileobj(f, bucket_name, file_key,
                ExtraArgs={
                    'ContentType': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'ContentDisposition': f'attachment; filename="{filename}"'
                }
            )
        
        # Generate pre-signed URL
        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': file_key},
            ExpiresIn=expiration_hours * 3600
        )
        
        return json.dumps({
            "status": "success",
            "filename": filename,
            "downloadUrl": download_url,
            "expiresAt": (datetime.now() + timedelta(hours=expiration_hours)).isoformat(),
            "message": f"Document {filename} uploaded successfully to Hetzner Storage"
        })
        
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Failed to upload: {str(e)}"})

@mcp.tool() 
async def create_and_upload_document(filename: str, title: Optional[str] = None, 
                                   author: Optional[str] = None, 
                                   expiration_hours: int = 24) -> str:
    """Create a new Word document and automatically upload to Hetzner cloud storage."""
    try:
        # Create document first
        create_result = await document_tools.create_document(filename, title, author)
        
        if "successfully" not in create_result:
            return json.dumps({"status": "error", "message": f"Document creation failed: {create_result}"})
        
        # Upload to Hetzner cloud storage
        upload_result_str = await upload_document_to_cloud(filename, expiration_hours)
        upload_result = json.loads(upload_result_str)
        
        if upload_result["status"] == "success":
            upload_result["title"] = title
            upload_result["author"] = author
            upload_result["message"] = f"Document '{filename}' created and uploaded to Hetzner Storage!"
            
            # Clean up local file
            try:
                os.remove(filename)
            except:
                pass
                
        return json.dumps(upload_result)
        
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Failed to create and upload: {str(e)}"})
```

### **Step 4: Actualizar n8n System Message (10 min)**
```text
Use `create_and_upload_document` tool for creating new Word documents with automatic cloud upload:
- **filename** (REQUIRED): Document name with .docx extension
- **title** (optional): Document title for metadata
- **author** (optional): Document author for metadata  
- **expiration_hours** (optional): Hours until download expires (default: 24, max: 168)

Example response format:
"✅ Document created successfully!

**📄 report.docx** (36.5 KB)
📝 Title: Monthly Report
👤 Author: Team Lead

🔗 [📥 **Download Document**](https://download-url-here...)

⏰ **Download link expires in 24 hours**

The document has been securely uploaded to Hetzner cloud storage."
```

### **Step 5: Deploy y Test (10 min)**
```bash
# 1. Deploy MCP server en Coolify
# 2. Test desde n8n: "create a document called test.docx"  
# 3. Verificar que devuelve download URL
# 4. Testear descarga del documento
```

---

## 🔧 **Test de Conexión Rápido**

```bash
# Test manual desde container del MCP server:
python3 -c "
import boto3
import os

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('HETZNER_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('HETZNER_SECRET_ACCESS_KEY'),
    endpoint_url=os.getenv('HETZNER_ENDPOINT_URL'),
    region_name=os.getenv('HETZNER_REGION')
)

try:
    response = s3.list_objects_v2(Bucket=os.getenv('HETZNER_BUCKET_NAME'), MaxKeys=1)
    print('✅ Conexión a Hetzner Storage exitosa!')
except Exception as e:
    print(f'❌ Error: {e}')
"
```

---

## 📋 **Checklist de Verificación**

- [ ] Variables de entorno configuradas en Coolify
- [ ] boto3 agregado a requirements.txt  
- [ ] Nuevos tools agregados a main.py
- [ ] System message actualizado en n8n
- [ ] MCP server redesplegado
- [ ] Test de conexión exitoso
- [ ] Test end-to-end desde n8n funciona
- [ ] Download URL funciona correctamente

---

## 🎯 **Resultado Esperado**

Cuando un usuario pida "create a document called report.docx", el AI debería responder algo como:

```
✅ Document created successfully!

**📄 report.docx** (36.5 KB)

🔗 [📥 **Download Document**](https://fsn1.your-objectstorage.com/bucket/documents/20240824_143022_a1b2c3d4_report.docx?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=...&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=...)

⏰ **Download link expires in 24 hours**

The document has been securely uploaded to Hetzner cloud storage and will be automatically cleaned up after 7 days.
```

**Total time: ~1.5 horas vs 2-3 semanas del plan original!** 🚀