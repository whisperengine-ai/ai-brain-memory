"""Configuration management for AI Brain."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration."""
    
    # LLM Backend Selection
    # Options: "openrouter", "ollama"
    LLM_BACKEND = os.getenv("LLM_BACKEND", "openrouter")
    
    # OpenRouter API (Remote)
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
    
    # Ollama (Local)
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
    
    # ChromaDB
    CHROMA_PERSIST_DIR = Path(os.getenv("CHROMA_PERSIST_DIR", "./chroma_db"))
    CHROMA_COLLECTION_NAME = "ai_brain_memory"
    
    # Embeddings (GPU-accelerated: MPS on Mac, CUDA on Windows/Linux)
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # NLP Models
    # Emotion detection model (RoBERTa) - Detects 11 emotions
    SENTIMENT_MODEL = os.getenv(
        "SENTIMENT_MODEL", 
        "cardiffnlp/twitter-roberta-base-emotion-multilabel-latest"
    )
    # spaCy model for NER and linguistic analysis
    SPACY_MODEL = os.getenv("SPACY_MODEL", "en_core_web_sm")
    
    # Memory settings
    MAX_MEMORY_ITEMS = int(os.getenv("MAX_MEMORY_ITEMS", "1000"))
    MEMORY_RELEVANCE_THRESHOLD = float(os.getenv("MEMORY_RELEVANCE_THRESHOLD", "0.3"))
    MEMORY_CONTEXT_SIZE = 5  # Number of relevant memories to retrieve
    
    # System prompt
    SYSTEM_PROMPT = """You are an AI assistant with persistent memory. You can remember past conversations and context.
When relevant memories are provided, use them to give more personalized and contextual responses.
Be helpful, thoughtful, and maintain continuity across conversations.

IMPORTANT CONVERSATIONAL GUIDELINES:
- When the user shares NEW information (projects, activities, feelings), show genuine curiosity and ask follow-up questions
- If the user says "I've been working on X", ask specifically about X rather than just recapping old topics
- Balance acknowledging past context with exploring new topics the user introduces
- Be engaged and forward-looking, not just a recap machine
- Prioritize what the user JUST said over older memories"""

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration."""
        if cls.LLM_BACKEND == "openrouter":
            if not cls.OPENROUTER_API_KEY:
                print("⚠️  Warning: OPENROUTER_API_KEY not set. Please set it in .env file.")
                return False
        elif cls.LLM_BACKEND == "ollama":
            print(f"ℹ️  Using local Ollama at {cls.OLLAMA_BASE_URL}")
            print(f"   Model: {cls.OLLAMA_MODEL}")
        return True
