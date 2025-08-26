# Posibilidades de Storage para Servir Documentos Word desde MCP Server

## 🏗️ **Arquitectura Propuesta**

### **Opción 1: Almacenamiento en Cloud + CDN (Recomendada)**

**Flujo:**
1. **MCP Server** genera el documento Word
2. **n8n** sube el archivo a almacenamiento cloud (S3, Google Cloud Storage, etc.)
3. **n8n** genera un enlace temporal firmado (expiración configurable)
4. **Usuario** recibe el enlace directo para descarga

**Ventajas:**
- ✅ Escalable (sin límites de almacenamiento)
- ✅ Alta disponibilidad
- ✅ CDN para descargas rápidas globales
- ✅ Enlaces temporales seguros
- ✅ Backup automático
- ✅ Costos predecibles

### **Opción 2: Sistema de Archivos Local + Proxy**

**Flujo:**
1. **MCP Server** guarda en volumen persistente
2. **n8n** genera enlace interno
3. **Nginx/Proxy** sirve archivos estáticos
4. **Usuario** descarga vía proxy

**Ventajas:**
- ✅ Control total del sistema
- ✅ Sin dependencias externas
- ✅ Costos mínimos

## 🔧 **Modificaciones en el Servidor MCP**

### **Nueva Herramienta: `serve_document`**
```python
@mcp.tool()
async def serve_document(filename: str, expiration_minutes: int = 60) -> str:
    """Generate a temporary download link for a Word document.
    
    Args:
        filename: Name of the document to serve
        expiration_minutes: How long the link should be valid (default 60)
    
    Returns:
        JSON with download URL and expiration info
    """
```

### **Funcionalidades del MCP Server:**

1. **Gestión de Archivos Temporales**
   - Guardar en directorio específico (`/tmp/documents/`)
   - Generar nombres únicos con timestamps
   - Limpiar archivos expirados automáticamente

2. **Servidor HTTP Interno**
   - Endpoint `/download/{file_id}` 
   - Validación de expiración
   - Headers correctos para descarga

3. **Base de Datos Simple**
   - SQLite para tracking de archivos
   - Campos: `file_id`, `filename`, `created_at`, `expires_at`, `download_count`

## 📋 **Modificaciones en n8n**

### **Nuevos Nodos Necesarios:**

1. **HTTP Request Node** (para servir archivos)
   - Endpoint: `/download/{file_id}`
   - Método: GET
   - Headers: `Content-Disposition: attachment`

2. **Function Node** (para gestión de enlaces)
   - Generar URLs únicas
   - Validar expiración
   - Formatear respuesta al usuario

3. **Webhook Node** (para recibir peticiones de descarga)
   - Endpoint público para descargas
   - Rate limiting
   - Logging de accesos

### **Flujo Completo en n8n:**

```
Chat Trigger → AI Agent → MCP Server → 
create_document → serve_document → 
HTTP Response con enlace → Usuario descarga
```

## 🗂️ **Políticas de Gestión de Archivos**

### **Opción 1: Eliminación Inmediata (Recomendada)**
```python
# Después de cada descarga exitosa
if download_count >= 1:
    delete_file(file_path)
    remove_from_database(file_id)
```

**Ventajas:**
- ✅ Máximo ahorro de espacio
- ✅ Seguridad (archivos no persisten)
- ✅ Simplicidad

**Desventajas:**
- ❌ No permite re-descargas
- ❌ Usuario debe guardar inmediatamente

### **Opción 2: TTL Configurable**
```python
# Eliminar archivos después de X minutos
CLEANUP_INTERVAL = 30  # minutos
MAX_FILE_AGE = 60      # minutos
```

**Ventajas:**
- ✅ Permite re-descargas en ventana de tiempo
- ✅ Control de costos de almacenamiento
- ✅ Flexibilidad para el usuario

### **Opción 3: Límite de Descargas**
```python
MAX_DOWNLOADS = 3  # máximo 3 descargas por archivo
```

## 🏗️ **Implementación Técnica**

### **En el MCP Server (Docker):**

1. **Nuevo endpoint HTTP**
```python
@app.route('/download/<file_id>')
async def download_file(file_id):
    # Validar expiración
    # Incrementar contador
    # Servir archivo
    # Eliminar si es última descarga
```

2. **Sistema de limpieza**
```python
# Cron job cada 5 minutos
async def cleanup_expired_files():
    # Eliminar archivos expirados
    # Limpiar base de datos
```

3. **Gestión de directorios**
```bash
# En Dockerfile
VOLUME /app/temp_documents
RUN mkdir -p /app/temp_documents
```

### **En n8n:**

1. **Configuración del webhook**
```javascript
// En Function node
const fileId = $input.first().json.file_id;
const downloadUrl = `http://mcp-server:8000/download/${fileId}`;
return { downloadUrl, expiresAt: $input.first().json.expires_at };
```

2. **Respuesta al usuario**
```javascript
// En HTTP Response node
return {
  message: "Documento creado exitosamente",
  downloadUrl: downloadUrl,
  expiresIn: "60 minutos"
};
```

## 🔒 **Consideraciones de Seguridad**

### **Validación de Enlaces:**
- Tokens JWT en URLs
- Validación de IP (opcional)
- Rate limiting por usuario

### **Limpieza Automática:**
- Archivos huérfanos (sin descargas)
- Archivos muy antiguos (>24h)
- Espacio en disco crítico

## 📊 **Métricas y Monitoreo**

### **Tracking en MCP:**
- Archivos generados por día
- Tasa de descarga exitosa
- Espacio en disco utilizado
- Tiempo promedio de vida de archivos

### **Alertas:**
- Espacio en disco >80%
- Tasa de error en descargas >5%
- Archivos no descargados >100

## 🛠️ **Tecnologías Recomendadas**

### **Para Almacenamiento:**
- **AWS S3** o **MinIO** (self-hosted)
- **Google Cloud Storage**
- **Azure Blob Storage**

### **Para Gestión de Archivos:**
- **Redis** para cache de URLs
- **PostgreSQL** para tracking de archivos
- **Cron jobs** para limpieza

### **Para Seguridad:**
- **JWT tokens** para URLs temporales
- **Rate limiting** por usuario/IP
- **Validación de tipos MIME**

## 📊 **Consideraciones de Escalabilidad**

### **Almacenamiento:**
- Implementar lifecycle policies
- Compresión automática de archivos
- Backup incremental

### **Rendimiento:**
- CDN para distribución global
- Cache de archivos frecuentes
- Load balancing para múltiples instancias

### **Monitoreo:**
- Métricas de generación/descarga
- Alertas de espacio en disco
- Logs centralizados

## 🔒 **Seguridad y Compliance**

### **Protección de Datos:**
- Encriptación en reposo
- Enlaces de un solo uso (opcional)
- Auditoría de accesos

### **Cumplimiento:**
- GDPR compliance (eliminación automática)
- Logs de auditoría
- Políticas de retención

## 💰 **Análisis de Costos**

### **Opción Cloud:**
- Storage: ~$0.023/GB/mes
- Transferencia: ~$0.09/GB
- CDN: ~$0.085/GB

### **Opción Self-hosted:**
- Storage local: Costo de hardware
- Mantenimiento: Tiempo de administración
- Backup: Costo de infraestructura

## 🎯 **Recomendación de Política**

**Implementar Opción 2 (TTL Configurable)** porque:

1. **Balance entre usabilidad y eficiencia**
2. **Permite re-descargas accidentales**
3. **Control de costos predecible**
4. **Experiencia de usuario mejor**

**Configuración sugerida:**
- TTL: 60 minutos
- Limpieza: cada 15 minutos
- Máximo: 3 descargas por archivo

## 🚀 **Plan de Implementación**

### **Fase 1: MCP Server Modifications**
1. Agregar herramienta `serve_document`
2. Implementar endpoint HTTP para descargas
3. Configurar base de datos SQLite
4. Implementar sistema de limpieza automática

### **Fase 2: n8n Integration**
1. Modificar flujo para usar nueva herramienta
2. Configurar webhook para descargas
3. Implementar Function node para gestión de URLs
4. Testing end-to-end

### **Fase 3: Production Deployment**
1. Configurar monitoreo y alertas
2. Implementar rate limiting
3. Configurar backup y recovery
4. Documentación y training

## 📝 **Próximos Pasos**

1. **Decidir política de almacenamiento** (TTL vs eliminación inmediata)
2. **Implementar herramienta `serve_document`** en MCP server
3. **Modificar flujo n8n** para integrar nueva funcionalidad
4. **Testing exhaustivo** de descargas y limpieza
5. **Deployment en producción** con monitoreo
