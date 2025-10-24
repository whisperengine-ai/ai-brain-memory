#!/usr/bin/env python3
"""Test configuration and backends."""

import os
from ai_brain.config import Config
from ai_brain.device_utils import print_device_info

def test_config():
    """Test configuration loading."""
    print("🧪 Testing Configuration")
    print("=" * 50)
    
    print("\n📋 Current Configuration:")
    print(f"   LLM Backend: {Config.LLM_BACKEND}")
    
    if Config.LLM_BACKEND.lower() == "ollama":
        print(f"   Ollama URL: {Config.OLLAMA_BASE_URL}")
        print(f"   Ollama Model: {Config.OLLAMA_MODEL}")
    else:
        print(f"   OpenRouter Model: {Config.OPENROUTER_MODEL}")
        has_key = bool(Config.OPENROUTER_API_KEY)
        print(f"   OpenRouter API Key: {'✅ Set' if has_key else '❌ Not set'}")
    
    print(f"\n🔮 Embedding Model: {Config.EMBEDDING_MODEL}")
    print(f"😊 Sentiment Model: {Config.SENTIMENT_MODEL}")
    print(f"🔬 spaCy Model: {Config.SPACY_MODEL}")
    
    print(f"\n💾 ChromaDB:")
    print(f"   Directory: {Config.CHROMA_PERSIST_DIR}")
    print(f"   Collection: {Config.CHROMA_COLLECTION_NAME}")
    
    print(f"\n⚙️  Memory Settings:")
    print(f"   Max items: {Config.MAX_MEMORY_ITEMS}")
    print(f"   Relevance threshold: {Config.MEMORY_RELEVANCE_THRESHOLD}")
    
    print("\n🖥️  Device Information:")
    print_device_info()
    
    print("\n✅ Configuration test complete!")
    
    # Validate
    is_valid = Config.validate()
    if is_valid:
        print("✅ Configuration is valid")
    else:
        print("⚠️  Configuration has issues (see warnings above)")

if __name__ == "__main__":
    test_config()
