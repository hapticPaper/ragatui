"""RAG setup utilities for ragatui."""

import os
from typing import Dict, Any, Optional
from pathlib import Path


def setup_rag_environment(
    provider: str = "chromadb",
    docker: bool = False,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, str]:
    """
    Setup RAG environment for ragatui.
    
    This function helps users configure their RAG database, either by:
    1. Writing environment variables for an existing setup
    2. Guiding through Docker-based setup
    
    Args:
        provider: RAG provider to use (chromadb, pgvector, etc.)
        docker: Whether to use Docker for setup
        config: Configuration dictionary
        
    Returns:
        Dictionary of environment variables to set
    """
    config = config or {}
    env_vars = {}
    
    if provider == "chromadb":
        # ChromaDB setup
        persist_directory = config.get("persist_directory", "./chroma_db")
        env_vars["CHROMA_PERSIST_DIRECTORY"] = persist_directory
        
        if docker:
            env_vars["CHROMA_HOST"] = config.get("host", "localhost")
            env_vars["CHROMA_PORT"] = str(config.get("port", 8000))
    
    elif provider == "pgvector":
        # PostgreSQL with pgvector setup
        env_vars["PGVECTOR_HOST"] = config.get("host", "localhost")
        env_vars["PGVECTOR_PORT"] = str(config.get("port", 5432))
        env_vars["PGVECTOR_DATABASE"] = config.get("database", "ragatui")
        env_vars["PGVECTOR_USER"] = config.get("user", "ragatui")
        env_vars["PGVECTOR_PASSWORD"] = config.get("password", "")
    
    # Write to .env file
    env_file = Path(".env")
    with open(env_file, "a") as f:
        f.write("\n# RAG Configuration\n")
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    return env_vars


def generate_docker_compose(
    provider: str = "chromadb",
    output_path: str = "docker-compose.yml"
) -> str:
    """
    Generate a docker-compose.yml file for RAG setup.
    
    Args:
        provider: RAG provider to use
        output_path: Path to write docker-compose.yml
        
    Returns:
        Path to the generated file
    """
    compose_content = ""
    
    if provider == "chromadb":
        compose_content = """version: '3.8'

services:
  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - ./chroma_data:/chroma/chroma
    environment:
      - IS_PERSISTENT=TRUE
      - ANONYMIZED_TELEMETRY=FALSE
"""
    
    elif provider == "pgvector":
        compose_content = """version: '3.8'

services:
  postgres:
    image: ankane/pgvector:latest
    ports:
      - "5432:5432"
    volumes:
      - ./pg_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=ragatui
      - POSTGRES_USER=ragatui
      - POSTGRES_PASSWORD=ragatui_password
"""
    
    if compose_content:
        with open(output_path, "w") as f:
            f.write(compose_content)
    
    return output_path


def check_rag_dependencies() -> Dict[str, bool]:
    """
    Check if RAG dependencies are available.
    
    Returns:
        Dictionary indicating which dependencies are available
    """
    dependencies = {}
    
    try:
        import chromadb
        dependencies["chromadb"] = True
    except ImportError:
        dependencies["chromadb"] = False
    
    try:
        import pgvector
        dependencies["pgvector"] = True
    except ImportError:
        dependencies["pgvector"] = False
    
    try:
        import langchain
        dependencies["langchain"] = True
    except ImportError:
        dependencies["langchain"] = False
    
    return dependencies


def print_setup_instructions(provider: str = "chromadb") -> None:
    """
    Print setup instructions for RAG.
    
    Args:
        provider: RAG provider to setup
    """
    print(f"\n=== RAG Setup Instructions for {provider} ===\n")
    
    if provider == "chromadb":
        print("1. Install ChromaDB: pip install chromadb")
        print("2. Run setup_rag_environment() to configure")
        print("3. Or use Docker: docker-compose up -d")
    
    elif provider == "pgvector":
        print("1. Install pgvector: pip install pgvector psycopg2-binary")
        print("2. Setup PostgreSQL with pgvector extension")
        print("3. Run setup_rag_environment() to configure")
        print("4. Or use Docker: docker-compose up -d")
    
    print("\nFor more information, visit: https://github.com/hapticPaper/ragatui")
