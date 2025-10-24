#!/usr/bin/env python3
"""Load documents into LlamaIndex RAG for Q&A."""

import sys
from pathlib import Path
from ai_brain.config import Config
from ai_brain.llamaindex_rag import LlamaIndexRAG
import chromadb

def main():
    """Load documents from command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python load_documents.py <file1> <file2> ... <fileN>")
        print("\nSupported formats: .txt, .md, .pdf, .docx")
        print("\nExample:")
        print("  python load_documents.py research_paper.pdf notes.txt")
        print("  python load_documents.py documents/  # Load all files in directory")
        sys.exit(1)
    
    # Validate config
    if not Config.validate():
        print("❌ Configuration error. Please check your .env file.")
        sys.exit(1)
    
    # Get file paths from arguments
    file_paths = sys.argv[1:]
    
    print(f"📁 Loading {len(file_paths)} file(s) into LlamaIndex RAG...")
    print()
    
    # Initialize ChromaDB
    print("🧠 Initializing ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=Config.CHROMA_PERSIST_DIR)
    
    # Initialize RAG
    rag = LlamaIndexRAG(
        chroma_client=chroma_client,
        collection_name=Config.CHROMA_COLLECTION_NAME
    )
    print()
    
    # Load documents
    print("📄 Loading documents...")
    count = rag.load_documents_from_files(file_paths)
    
    print()
    print(f"✅ Successfully loaded {count} document(s)")
    print()
    print("💡 Now you can run:")
    print("   python main_enhanced.py --llamaindex")
    print()
    print("And ask questions about your documents!")

if __name__ == "__main__":
    main()
