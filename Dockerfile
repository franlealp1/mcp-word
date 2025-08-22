# Multi-stage build for optimized production deployment
# syntax=docker/dockerfile:1

FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Install runtime dependencies (LibreOffice for document conversion)
RUN apt-get update && apt-get install -y \
    libreoffice \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r mcp && useradd -r -g mcp mcp

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and package files
COPY word_document_server/ ./word_document_server/
COPY office_word_mcp_server/ ./office_word_mcp_server/
COPY word_mcp_server.py ./
COPY requirements.txt ./
COPY pyproject.toml ./
COPY __init__.py ./
COPY LICENSE ./
COPY README.md ./

# Install the local package properly (must be done as root)
RUN pip install --no-cache-dir . && \
    pip list | grep office-word-mcp-server

# Create directories for document storage with proper permissions
RUN mkdir -p /app/documents /app/temp && \
    chown -R mcp:mcp /app

# Switch to non-root user
USER mcp

# Set environment variables for HTTP transport
ENV MCP_TRANSPORT=streamable-http
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=8000
ENV MCP_PATH=/mcp
ENV FASTMCP_LOG_LEVEL=INFO
ENV PYTHONPATH=/app

# Health check for Coolify - check if Python process is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ps aux | grep python | grep word_m || exit 1

# Expose port
EXPOSE 8000

# Run the MCP server with HTTP transport
# Support both module and direct script execution
CMD ["sh", "-c", "python -m office_word_mcp_server || python word_mcp_server.py"]
