"""
Entry point for running office-word-mcp-server as a Python module.
This allows running: python -m office-word-mcp-server
"""

from word_document_server.main import run_server

if __name__ == "__main__":
    run_server()