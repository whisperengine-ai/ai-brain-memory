# 📝 Configuration Quick Reference

## Complete .env Configuration Options

```bash
# ============================================
# LLM Backend Configuration
# ============================================
# Choose your LLM backend
# Options: "openrouter" (remote) or "ollama" (local)
LLM_BACKEND=openrouter

# ──────────────────────────────────────────
# OpenRouter (Remote API)
# ──────────────────────────────────────────
# Get API key from: https://openrouter.ai/keys
OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Popular models:
# - anthropic/claude-3.5-sonnet  (Best quality)
# - openai/gpt-4-turbo          (Very capable)
# - meta-llama/llama-3-70b      (Open source)
# - mistralai/mistral-medium    (Fast & good)

# ──────────────────────────────────────────
# Ollama (Local Models)
# ──────────────────────────────────────────
# Install from: https://ollama.ai
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Popular models:
# - llama3.2       (7B - good balance)
# - llama3.2:1b    (1B - very fast)
# - mistral        (7B - alternative)
# - phi3           (3.8B - compact)
# - codellama      (7B - code focused)

# ============================================
# ChromaDB Configuration
# ============================================
# Where to store vector database
CHROMA_PERSIST_DIR=./chroma_db

# ============================================
# Embedding & NLP Models
# ============================================

# ──────────────────────────────────────────
# Embedding Model (for semantic search)
# ──────────────────────────────────────────
# GPU-accelerated on Mac (MPS), Windows/Linux (CUDA)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Options:
# - all-MiniLM-L6-v2           (Fast, 384 dims)
# - all-mpnet-base-v2          (Better, 768 dims)
# - multi-qa-mpnet-base-dot-v1 (QA optimized)

# ──────────────────────────────────────────
# Sentiment Analysis Model
# ──────────────────────────────────────────
# RoBERTa model for emotion detection
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest

# Options:
# - cardiffnlp/twitter-roberta-base-sentiment-latest (Conversational)
# - distilbert-base-uncased-finetuned-sst-2-english (Fast)
# - nlptown/bert-base-multilingual-uncased-sentiment (Multilingual)

# ──────────────────────────────────────────
# spaCy Model (NER & linguistics)
# ──────────────────────────────────────────
SPACY_MODEL=en_core_web_sm

# Options:
# - en_core_web_sm  (12MB - fast, good for most uses)
# - en_core_web_md  (40MB - better, includes word vectors)
# - en_core_web_lg  (540MB - best, largest vocab)

# ============================================
# Memory Settings
# ============================================
# Maximum number of memories to store
MAX_MEMORY_ITEMS=1000

# Similarity threshold for memory retrieval (0.0-1.0)
# Lower = more memories retrieved, Higher = only very relevant
MEMORY_RELEVANCE_THRESHOLD=0.7
```

## Platform-Specific Notes

### 🍎 macOS
- **GPU**: Automatically uses Metal Performance Shaders (MPS)
- **MLX**: Available for future optimizations
- **Ollama**: Runs as menu bar app

### 🪟 Windows
- **GPU**: Automatically uses CUDA if NVIDIA GPU present
- **Ollama**: Runs as Windows service
- **Virtual Env**: Use `.venv\Scripts\activate` instead of `source`

### 🐧 Linux
- **GPU**: Automatically uses CUDA if NVIDIA GPU present
- **Ollama**: Can run as systemd service
- **Permissions**: May need to add user to ollama group

## Quick Configuration Presets

### Preset 1: Best Quality (Remote)
```bash
LLM_BACKEND=openrouter
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
SPACY_MODEL=en_core_web_lg
```

### Preset 2: Fast & Private (Local)
```bash
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2:1b
SENTIMENT_MODEL=distilbert-base-uncased-finetuned-sst-2-english
SPACY_MODEL=en_core_web_sm
```

### Preset 3: Balanced
```bash
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
SPACY_MODEL=en_core_web_sm
```

### Preset 4: Cost-Effective Remote
```bash
LLM_BACKEND=openrouter
OPENROUTER_MODEL=meta-llama/llama-3-8b
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest
SPACY_MODEL=en_core_web_sm
```

## Testing Your Configuration

```bash
# Test all settings
python test_config.py

# Test device detection
python ai_brain/device_utils.py

# Test NLP features
python test_nlp.py

# Test emotional tracking
python test_emotional_tracking.py

# Test full integration
python test_full_emotional_integration.py
```

## Environment Variable Priority

1. **Command line** (highest priority)
   ```bash
   LLM_BACKEND=ollama python main.py
   ```

2. **`.env` file** (medium priority)
   ```bash
   LLM_BACKEND=ollama
   ```

3. **Default values** (lowest priority)
   - Defined in `ai_brain/config.py`

## Common Configuration Scenarios

### Scenario 1: Developer with Fast Local Testing
```bash
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2:1b  # Fast 1B model
SPACY_MODEL=en_core_web_sm  # Small model
```

### Scenario 2: Production with Best Quality
```bash
LLM_BACKEND=openrouter
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
SPACY_MODEL=en_core_web_lg
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### Scenario 3: Privacy-Focused
```bash
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2
# Everything runs locally, no external API calls
```

### Scenario 4: Budget-Conscious
```bash
LLM_BACKEND=ollama  # Free local models
# Or use cheaper OpenRouter models:
# OPENROUTER_MODEL=meta-llama/llama-3-8b
```

## Model Size vs Performance Trade-offs

| Model Type | Size | Speed | Quality | Use Case |
|-----------|------|-------|---------|----------|
| **1B** | ~1GB | Very Fast | Good | Testing, simple tasks |
| **3-7B** | ~4GB | Fast | Very Good | Daily use, balanced |
| **13-30B** | ~15GB | Medium | Excellent | Complex tasks |
| **70B+** | ~40GB | Slow | Best | Production, quality critical |

## Troubleshooting Configuration

### Issue: Can't find .env file
```bash
# Create from example
cp .env.example .env
```

### Issue: Changes not taking effect
```bash
# Restart Python/reload environment
# Or check for typos in variable names
```

### Issue: Model not loading
```bash
# Check model is available:
ollama list  # For Ollama
# Or verify spelling in .env matches exactly
```

## Learn More

- **Full Setup**: See [README.md](README.md)
- **Ollama Guide**: See [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md)
- **NLP Features**: See [NLP_FEATURES.md](NLP_FEATURES.md)
- **Recent Updates**: See [UPDATES.md](UPDATES.md)
