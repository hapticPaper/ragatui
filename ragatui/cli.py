"""CLI entry point for ragatui."""

import argparse
import sys
import os
import runpy
from ragatui.config import get_config

def main():
    """Main entry point for ragatui CLI."""
    parser = argparse.ArgumentParser(description="ragatui: TUI for Python scripts with LLM monitoring")
    parser.add_argument("script", help="Python script to run")
    parser.add_argument("--local-rag", action="store_true", help="Use local FAISS-based RAG storage")
    parser.add_argument("--rag-provider", default="faiss", help="RAG provider (default: faiss)")
    parser.add_argument("--embedding-provider", default="local", help="Embedding provider (default: local)")
    parser.add_argument("--embedding-model", default="embeddinggemma", help="Embedding model (default: embeddinggemma)")
    parser.add_argument("--embedding-endpoint", default=None, help="Embedding endpoint (default: http://localhost:11434)")
    
    # Parse known args to allow script args to pass through if needed
    # But for now, we assume simple usage
    args, script_args = parser.parse_known_args()
    
    # Configure RAG based on CLI args
    config = get_config()
    
    if args.local_rag:
        config.enable_rag(
            provider="faiss",
            storage_type="local",
            persist_directory="./faiss_db"
        )
    elif args.rag_provider != "faiss":
         config.enable_rag(
            provider=args.rag_provider
        )
    
    # Configure Embeddings
    config.set_embedding_config(
        provider=args.embedding_provider,
        model=args.embedding_model,
        endpoint=args.embedding_endpoint
    )
    
    # Set script args so the script sees them
    sys.argv = [args.script] + script_args
    
    # Run the script
    print(f"[ragatui] Running {args.script}...")
    if args.local_rag:
        print(f"[ragatui] RAG enabled with Local FAISS storage")
        print(f"[ragatui] Embedding: {args.embedding_provider}/{args.embedding_model}")
    
    try:
        # Get absolute path
        script_path = os.path.abspath(args.script)
        # Add script directory to path so imports work
        sys.path.insert(0, os.path.dirname(script_path))
        
        runpy.run_path(script_path, run_name="__main__")
    except Exception as e:
        print(f"[ragatui] Error running script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
