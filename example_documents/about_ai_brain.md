# Example Document for Testing

This is a sample document to demonstrate how to load documents into the LlamaIndex RAG system.

## About the AI Brain Project

The AI Brain/Mind with Memory project is a sophisticated AI assistant that combines:

- **Persistent Memory**: Uses ChromaDB to remember conversations across sessions
- **Smart Retrieval**: Semantic search to find relevant past conversations
- **NLP Analysis**: spaCy for linguistic analysis and RoBERTa for sentiment
- **Multiple Frameworks**: Supports basic, LangChain, and LlamaIndex modes

## Key Features

### Memory Storage
Every conversation is stored with embeddings in ChromaDB, allowing the AI to recall:
- Facts you've shared
- Preferences you've mentioned
- Previous topics discussed
- Emotional context

### Cross-Platform Support
Works on:
- macOS with Apple Silicon (MPS GPU acceleration)
- Windows with NVIDIA (CUDA acceleration)
- Linux with NVIDIA (CUDA acceleration)
- Any platform with CPU fallback

### Advanced RAG
The LlamaIndex mode allows you to:
1. Load your own documents
2. Ask questions about them
3. Get context-aware answers
4. Combine document knowledge with conversation memory

## Example Use Cases

### Research Assistant
Load research papers, ask questions about methodologies, findings, and related work.

### Knowledge Base
Load documentation, product specs, or training materials for quick Q&A.

### Personal Assistant
Load notes, schedules, or personal documents for contextual assistance.

## Technical Stack

- **Python 3.13** - Modern Python features
- **ChromaDB** - Vector database for embeddings
- **LangChain** - Advanced prompt engineering
- **LlamaIndex** - RAG and document Q&A
- **spaCy** - NLP and linguistic analysis
- **RoBERTa** - Sentiment analysis
- **OpenRouter/Ollama** - LLM inference

## Getting Started

1. Install dependencies
2. Configure your LLM backend (OpenRouter or Ollama)
3. Load documents (for RAG mode)
4. Start chatting!

The system automatically detects your hardware and optimizes accordingly.
