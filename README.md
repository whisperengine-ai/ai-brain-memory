# 🧠 AI Brain/Mind with Memory

A state-of-the-art AI assistant with persistent memory, **cross-platform compatible** (macOS & Windows). Features **LangChain**, **LlamaIndex**, **spaCy NLP**, **RoBERTa sentiment analysis**, **emotional context tracking**, ChromaDB, and OpenRouter.

<img width="838" height="860" alt="image" src="https://github.com/user-attachments/assets/c3c8e636-6eed-40d4-adf0-4a4d95cb574c" />




<img width="890" height="738" alt="image" src="https://github.com/user-attachments/assets/b6a731a0-48fb-4ae0-b536-7f597a8817d4" />



<img width="898" height="533" alt="image" src="https://github.com/user-attachments/assets/ed65f2db-3d85-4686-8979-365a6011a574" />


## ⚡ Quick Start (30 seconds)

```bash
# 1. Setup (first time only)
cd ai-brain-memory
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e .
cp .env.example .env               # Then add your OpenRouter API key to .env

# 2. Run it!
python main.py                     # Basic mode (simple & fast)
# OR
python main_enhanced.py            # Enhanced mode with LangChain (recommended!)
# OR
python main_enhanced.py --llamaindex   # Enhanced + Document Q&A
```

**That's it!** You now have an AI with memory. Type `/help` for commands, `/quit` to exit.

### 📊 Which Mode Should I Use? (Decision Tree)

```
Start Here → What do you need?
                     │
        ┌────────────┼────────────────┐
        │            │                │
   Speed &      Best Overall    Document Q&A
   Simplicity   Experience      over PDFs/Files
        │            │                │
        ↓            ↓                ↓
   main.py    main_enhanced.py   main_enhanced.py
                                   --llamaindex
        │            │                │
    ✅ Done!     ✅ Done!          ✅ Done!
    
    Fastest      LangChain        LangChain
    Basic AI     Enabled          + RAG
```

**TL;DR:** 
- New users? → `python main_enhanced.py` (best experience!)
- Need speed? → `python main.py` (basic mode)
- Have documents? → `python main_enhanced.py --llamaindex` (Q&A mode)

---

---

## 🎉 What's New in v2.0 (Phase 2 - Oct 2024)

**Major enhancements achieving 9.0/10 score:**

- ⏰ **Human-Readable Times**: Memory timestamps show "28 minutes ago" instead of ISO format
- 📋 **Topic Tracking**: New `/topics` command shows what you've discussed with sentiment analysis
- 📝 **Extended History**: 10-message conversation window (up from 6) for better context
- 💭 **Smart Summarization**: Long conversations (>20 messages) automatically summarized - no more context cliff!
- 🔍 **Hybrid Search**: Enhanced memory retrieval with entity (+0.15) and keyword (+0.05) boosting

**Score progression:** 7.5 → 8.5 (Phase 1) → 9.0 (Phase 2) 🎯

---

## 🖥️ Cross-Platform Support

This project automatically detects and optimizes for your hardware:

- **macOS (Apple Silicon)**: M1/M2/M3/M4 with MPS (Metal Performance Shaders) GPU acceleration
- **Windows/Linux**: NVIDIA GPUs with CUDA acceleration
- **Fallback**: CPU processing on any platform

The system automatically:
- ✅ Detects available GPU (MPS, CUDA, or CPU)
- ✅ Loads models on the optimal device
- ✅ Uses platform-specific optimizations
- ✅ Displays device info on startup

## ✨ Features

### **Core Capabilities**
- 🤖 **Remote Inference**: OpenRouter API for powerful LLM responses
- 🧠 **Persistent Memory**: ChromaDB vector storage for long-term memory
- ⚡ **Fast Embeddings**: Local sentence transformers optimized for M4 GPU
- � **Interactive CLI**: Beautiful command-line chat interface
- 🔍 **Semantic Search**: Retrieves relevant memories based on context
- 📊 **Memory Statistics**: Track and manage your AI's memory
- 📋 **Topic Tracking**: NEW! `/topics` command to see conversation topics

### **Advanced NLP Pipeline**
- 🔬 **spaCy Analysis**: Named entity recognition, POS tagging, dependency parsing
- 😊 **11-Emotion Tracking**: RoBERTa model with 11 specific emotions (joy, optimism, gratitude, etc.)
- 🏷️ **Smart Tagging**: Automatic keyword extraction and topic identification
- 🎯 **Intent Detection**: Classify questions, statements, commands, expressions
- 📝 **Metadata Enrichment**: Every conversation tagged with linguistic features
- 📈 **Emotional Trajectory**: Track emotional patterns over conversation history

### **Intelligent Context Management** ✨ NEW in Phase 2
- 💭 **Conversation Summarization**: Automatic summarization for conversations >20 messages
- 📝 **Extended History**: 10-message window aligned with emotional analysis  
- ⏰ **Human-Readable Times**: "28 minutes ago" instead of ISO timestamps
- 🔍 **Hybrid Search**: Vector similarity + entity boosting (+0.15) + keyword boosting (+0.05)
- 🎯 **Smart Context**: No more "context cliff" - smooth transition from summary to details

### **AI Frameworks**
- � **LangChain Integration**: Advanced prompt engineering & conversation chains
- 🦙 **LlamaIndex RAG**: Sophisticated retrieval-augmented generation
- 🧩 **Multiple Modes**: Switch between basic, LangChain, or LlamaIndex pipelines

## 🏗️ Architecture

### **Basic Mode**
```
┌─────────────────────────────────────────────────┐
│           User (Command Line Interface)          │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              AI Brain (cli.py)                   │
├──────────────────────────────────────────────────┤
│  • Chat Interface                                │
│  • Command Handling                              │
│  • Session Management                            │
└──────┬───────────────────────────────────┬───────┘
       │                                   │
┌──────▼────────────────┐     ┌───────────▼────────┐
│   Memory Store        │     │    AI Inference    │
│   (memory.py)         │     │   (inference.py)   │
├───────────────────────┤     ├────────────────────┤
│ • ChromaDB (Vector)   │     │ • OpenRouter API   │
│ • Embeddings (Local)  │     │ • Streaming        │
│ • Semantic Search     │     │ • Context Building │
└───────────────────────┘     └────────────────────┘
```

### **Enhanced Mode (LangChain + LlamaIndex)**
```
┌─────────────────────────────────────────────────┐
│           User (Command Line Interface)          │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         Enhanced AI Brain (enhanced_cli.py)      │
├──────────────────────────────────────────────────┤
│  • Advanced Chat Interface                       │
│  • Mode Switching                                │
│  • Multi-Pipeline Support                        │
└──────┬────────────────────┬─────────────┬────────┘
       │                    │             │
┌──────▼────────────┐  ┌────▼───────┐  ┌─▼─────────┐
│   Memory Store    │  │ LangChain  │  │ LlamaIndex│
│   (memory.py)     │  │   Brain    │  │    RAG    │
├───────────────────┤  ├────────────┤  ├───────────┤
│ • ChromaDB        │  │ • Prompts  │  │ • Query   │
│ • Embeddings      │  │ • Chains   │  │ • Index   │
│ • Search          │  │ • Memory   │  │ • Nodes   │
└───────────────────┘  └────────────┘  └───────────┘
```

## 📦 Installation

### Prerequisites
- **Python 3.10+** (3.13 recommended)
- **macOS**: Works on Intel or Apple Silicon (M1/M2/M3/M4)
- **Windows**: Works with or without NVIDIA GPU
- **Linux**: Supported (CUDA optional)

### Platform-Specific Setup

<details>
<summary><b>🍎 macOS Installation</b></summary>

```bash
# 1. Navigate to project
cd /path/to/ai-brain-memory

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e .

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Configure environment
cp .env.example .env
# Edit .env with your preferred text editor
nano .env  # or: code .env, vim .env
```

**GPU Support**: Automatically uses Apple Silicon GPU (MPS) if available.

</details>

<details>
<summary><b>🪟 Windows Installation</b></summary>

```cmd
# 1. Navigate to project
cd C:\path\to\ai-brain-memory

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -e .

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Configure environment
copy .env.example .env
# Edit .env with Notepad or your preferred editor
notepad .env
```

**GPU Support**: 
- Automatically uses NVIDIA CUDA if available
- Works on CPU if no GPU present

**Note**: If you have an NVIDIA GPU, install CUDA Toolkit from [nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)

</details>

<details>
<summary><b>🐧 Linux Installation</b></summary>

```bash
# 1. Navigate to project
cd /path/to/ai-brain-memory

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e .

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Configure environment
cp .env.example .env
# Edit .env with your preferred editor
nano .env  # or: vim .env, gedit .env
```

**GPU Support**:
- Automatically uses NVIDIA CUDA if available
- Works on CPU if no GPU present

**NVIDIA GPU Users**: Install CUDA Toolkit:
```bash
# Ubuntu/Debian
sudo apt install nvidia-cuda-toolkit

# Fedora/RHEL
sudo dnf install cuda
```

</details>

## ⚙️ Configuration

### LLM Backend Options

You can use either **remote APIs** (OpenRouter) or **local models** (Ollama):

#### Option 1: OpenRouter (Remote - Default)

Edit `.env`:
```bash
LLM_BACKEND=openrouter
OPENROUTER_API_KEY=your-api-key-here
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

- ✅ Access to best models (GPT-4, Claude, etc.)
- ✅ No local setup required
- ❌ Requires API key and internet
- ❌ Pay per use

#### Option 2: Ollama (Local - Private & Free)

1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Pull a model**: `ollama pull llama3.2`
3. **Configure** `.env`:
```bash
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

- ✅ 100% private and free
- ✅ Works offline
- ✅ Fast (no network latency)
- ❌ Requires local installation
- ❌ Limited to open-source models

See [OLLAMA_GUIDE.md](OLLAMA_GUIDE.md) for detailed instructions.

### NLP & Embedding Configuration

```bash
# Embedding Model (GPU-accelerated)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Sentiment Analysis (RoBERTa)
SENTIMENT_MODEL=cardiffnlp/twitter-roberta-base-sentiment-latest

# spaCy Model (NER & Linguistics)
SPACY_MODEL=en_core_web_sm

# ChromaDB Storage
CHROMA_PERSIST_DIR=./chroma_db

# Memory Settings
MAX_MEMORY_ITEMS=1000
MEMORY_RELEVANCE_THRESHOLD=0.7
```

### System Prompt Customization ✨ NEW

You can customize the AI's personality and behavior by editing the system prompt in three ways:

#### Option 1: Use a Template File (Recommended)

Edit one of the provided templates in the `templates/` directory or use an existing one:

```bash
# Use the default template
SYSTEM_PROMPT_FILE=templates/system_prompt.txt

# Or choose a pre-configured personality
SYSTEM_PROMPT_FILE=templates/system_prompt_professional.txt  # Business tone
SYSTEM_PROMPT_FILE=templates/system_prompt_creative.txt      # Creative assistant
SYSTEM_PROMPT_FILE=templates/system_prompt_technical.txt     # Technical support
```

**Available Templates:**
- `system_prompt.txt` - Default balanced assistant
- `system_prompt_professional.txt` - Business/professional tone
- `system_prompt_creative.txt` - Creative writing assistant
- `system_prompt_technical.txt` - Technical/coding assistant

Edit the `.txt` files directly to customize the AI's personality!

#### Option 2: Set as Environment Variable

```bash
SYSTEM_PROMPT="You are a helpful AI assistant that specializes in..."
```

#### Option 3: Edit the Default in Code

Modify `ai_brain/config.py` and change the `DEFAULT_SYSTEM_PROMPT` variable.

**Priority:** File template → Environment variable → Default in code

See `templates/README.md` for more details on creating custom templates.

### Test Your Configuration

```bash
python test_config.py
```

This shows your current configuration and device information.

## 🚀 Usage

### Understanding the Different Modes

This AI Brain has **TWO main programs** you can run, each with different capabilities:

#### 1️⃣ **Basic Mode** (`main.py`)
- **What it does**: Simple, straightforward AI chat with memory
- **Best for**: Quick conversations, testing, everyday use
- **Features**: Memory retrieval, sentiment analysis, emotional adaptation, conversation storage
- **Command**: `python main.py`

#### 2️⃣ **Enhanced Mode** (`main_enhanced.py`)
- **What it does**: Advanced AI with sophisticated frameworks
- **Best for**: Complex tasks, research, advanced prompting, document Q&A
- **Features**: Everything from Basic + LangChain AND/OR LlamaIndex pipelines
- **Commands**:
  - `python main_enhanced.py` (defaults to LangChain mode)
  - `python main_enhanced.py --langchain` (explicitly enable LangChain)
  - `python main_enhanced.py --llamaindex` (enable both LangChain + LlamaIndex RAG)

### Command Reference Table

| Command | LangChain | LlamaIndex | Best For |
|---------|-----------|------------|----------|
| `python main.py` | ❌ | ❌ | Quick chats, testing, everyday use |
| `python main_enhanced.py` | ✅ | ❌ | **Default enhanced mode** - Better prompts & context |
| `python main_enhanced.py --langchain` | ✅ | ❌ | Same as above (explicit) |
| `python main_enhanced.py --llamaindex` | ✅ | ✅ | Document Q&A, research, RAG |

**Important Notes:**
- `python main_enhanced.py` with **no flags** defaults to **LangChain mode** (not basic mode!)
- LangChain provides better prompt engineering and context management
- LlamaIndex adds document Q&A capabilities on top of LangChain
- All modes include emotional adaptation and memory retrieval

### Quick Start Guide

**Step 1: Activate your virtual environment first (required!)**

<details>
<summary><b>🍎 macOS</b></summary>

```bash
cd /path/to/ai-brain-memory
source .venv/bin/activate
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
cd C:\path\to\ai-brain-memory
.venv\Scripts\activate
```

</details>

<details>
<summary><b>🐧 Linux</b></summary>

```bash
cd /path/to/ai-brain-memory
source .venv/bin/activate
```

</details>

**Step 2: Choose which mode to run**

```bash
# OPTION A: Basic Mode (simple and fast)
python main.py

# OPTION B: Enhanced Mode (default - uses LangChain)
python main_enhanced.py

# OPTION C: Enhanced Mode with LangChain (explicit)
python main_enhanced.py --langchain

# OPTION D: Enhanced Mode with LlamaIndex RAG (document Q&A)
python main_enhanced.py --llamaindex
```

**💡 Pro Tip:** Just running `python main_enhanced.py` gives you LangChain automatically!

### Mode Comparison

| Feature | Basic Mode | Enhanced (Default) | Enhanced + RAG |
|---------|------------|-------------------|----------------|
| **Command** | `python main.py` | `python main_enhanced.py` | `python main_enhanced.py --llamaindex` |
| **LangChain** | ❌ No | ✅ Yes | ✅ Yes |
| **LlamaIndex RAG** | ❌ No | ❌ No | ✅ Yes |
| **Memory Retrieval** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Emotional Adaptation** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Sentiment Analysis** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Advanced Prompts** | ❌ No | ✅ Yes | ✅ Yes |
| **Recent Context (5 turns)** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Document Q&A** | ❌ No | ❌ No | ✅ Yes |
| **Speed** | 🚀 Fastest | ⚡ Fast | 💨 Moderate |
| **Complexity** | 🟢 Simple | 🟡 Moderate | 🔴 Advanced |

### Which Mode Should I Use?

**Use Basic Mode (`python main.py`) when:**
- You want quick, simple conversations
- You're just testing the system
- You don't need advanced features
- You want the fastest performance

**Use Enhanced Mode (`python main_enhanced.py`) when:**
- You want sophisticated prompt engineering (LangChain)
- You need better conversation flow management
- You're working on complex tasks requiring structured prompts
- You want the AI to maintain better context
- **This is the recommended default for most users!**

**Use Enhanced + RAG Mode (`python main_enhanced.py --llamaindex`) when:**
- You're doing research or Q&A over documents
- You need to chat with PDFs, notes, or documentation
- You're building a knowledge base application
- You want document-aware responses

### Loading Documents for RAG (LlamaIndex)

The LlamaIndex mode lets you ask questions about your own documents!

**Step 1: Load your documents**
```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Load a single file
python scripts/load_documents.py research_paper.pdf

# Load multiple files
python scripts/load_documents.py notes.txt report.pdf documentation.md

# Load all files in a directory
python scripts/load_documents.py documents/
```

**Supported formats:** `.txt`, `.md`, `.pdf`, `.docx`

**Step 2: Ask questions about them**
```bash
python main_enhanced.py --llamaindex
```

```
[You] ➜ Summarize the main findings from the research paper
💭 Using 3 relevant documents
[AI] ➜ Based on the research paper you provided, the main findings are...
```

**Example workflow:**
```bash
# 1. Create a documents folder
mkdir my_documents
mv research.pdf my_documents/
mv notes.txt my_documents/

# 2. Load all documents
python scripts/load_documents.py my_documents/

# 3. Chat with your documents
python main_enhanced.py --llamaindex
```

The documents are stored in ChromaDB and will persist across sessions!

**For a complete step-by-step guide, see [RAG_QUICKSTART.md](RAG_QUICKSTART.md)**

### Practical Examples

**Example 1: Basic everyday chat**
```bash
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
python main.py
```
```
[You] ➜ My name is Alex and I love hiking
[AI] ➜ Nice to meet you, Alex! Hiking is a wonderful activity...

[You] ➜ What's my name?
💭 Using 1 relevant memories
[AI] ➜ Your name is Alex! You mentioned that when you told me about your love for hiking.
```

**Example 2: Enhanced mode with better context handling**
```bash
source .venv/bin/activate
python main_enhanced.py --langchain
```
```
[You] ➜ I'm working on a Python project about machine learning
[AI] ➜ That sounds exciting! Machine learning with Python is a great combination...

[You] ➜ Can you help me with my project?
💭 Using 1 relevant memories
😊 Detected emotion: positive
[AI] ➜ Of course! Based on what you told me about your Python machine learning project,
      I'd be happy to help. What specific aspect are you working on?
```

**Example 3: Research mode with LlamaIndex**
```bash
source .venv/bin/activate

# First, load some documents
python scripts/load_documents.py example_documents/about_ai_brain.md

# Then chat with your documents
python main_enhanced.py --llamaindex
```
```
[You] ➜ What is this AI Brain project about?
💭 Using 3 relevant documents
[AI] ➜ Based on the loaded documents, the AI Brain/Mind with Memory project 
      is a sophisticated AI assistant that combines persistent memory using 
      ChromaDB, smart retrieval with semantic search, NLP analysis with spaCy 
      and RoBERTa, and supports multiple frameworks including basic, LangChain, 
      and LlamaIndex modes...

[You] ➜ What frameworks does it support?
💭 Using 2 relevant documents
[AI] ➜ The project supports three main frameworks:
      1. Basic mode - for simple conversations
      2. LangChain - for advanced prompt engineering
      3. LlamaIndex - for document Q&A and RAG...
```

*Best for document Q&A and knowledge base queries*

### What Happens on Startup

The system will automatically:
- ✅ Detect your GPU (MPS/CUDA/CPU)
- ✅ Load models on optimal device
- ✅ Connect to configured LLM backend
- ✅ Initialize memory store

Example output:
```
🖥️  System Information:
   OS: Darwin 24.6.0
   Platform: arm64
   Python: 3.13.7

🚀 Compute Device:
   Device: Apple Silicon GPU (MPS)
   Type: mps

🤖 AI Brain initialized with OpenRouter model: anthropic/claude-3.5-sonnet
```

### Available Commands

- `/help` - Show help message
- `/stats` - Show memory statistics
- `/topics` - Show conversation topics with sentiment analysis (NEW!)
- `/clear` - Clear all memories
- `/exit` or `/quit` - Exit the chat

## ❓ FAQ - Common Questions

### "Which file do I run?"

Run **ONE** of these:
- `python main.py` - Basic mode (fastest, simple)
- `python main_enhanced.py` - Enhanced mode with LangChain (recommended!)
- `python main_enhanced.py --llamaindex` - Enhanced + document Q&A

**Don't run both at the same time.** Pick one based on your needs.

**New to the project?** Start with `python main_enhanced.py` for the best experience!

### "What's the difference between the modes?"

**Quick answer:**
- `python main.py` = Basic AI chat (fast and simple)
- `python main_enhanced.py` = **Better prompts + context** (LangChain - recommended default)
- `python main_enhanced.py --llamaindex` = Document Q&A + everything above

**All modes include:**
- ✅ Persistent memory (ChromaDB)
- ✅ Emotional adaptation
- ✅ Recent conversation context (last 3 turns)
- ✅ Sentiment analysis

**Enhanced mode adds:**
- ✅ Advanced prompt engineering with LangChain
- ✅ Better system prompts with detailed context
- ✅ Emotional adaptation guidance in prompts

**LlamaIndex mode adds:**
- ✅ Document Q&A (PDF, TXT, MD, DOCX)
- ✅ RAG (Retrieval-Augmented Generation)
- ✅ Chat with your documents

**💡 Tip:** `python main_enhanced.py` (with no flags) automatically enables LangChain!

### "Do I need to activate the virtual environment?"

**YES!** Always run this first:
```bash
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
```

If you forget, you'll see errors like "ModuleNotFoundError".

### "Do I need OpenRouter or Ollama?"

You need **ONE** of them:
- **OpenRouter**: Cloud-based, requires API key, uses best models (Claude, GPT-4)
- **Ollama**: Local, free, private, but requires installation

Configure your choice in `.env` file (see [Configuration](#%EF%B8%8F-configuration) section).

### "How do I know it's working?"

You should see:
```
🧠 AI Brain/Mind with Memory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[You] ➜ 
```

If you see errors instead, check [Troubleshooting](#-troubleshooting).

### "What files will be created?"

The program creates:
- `chroma_db/` - Your AI's memory storage
- `logs/conversations/` - JSON logs of your chats
- `logs/prompts/` - System prompts for debugging
- `.chat_history` - Command history

All are automatically ignored by git (private to your machine).

### "Can I delete the logs?"

Yes! Safe to delete anytime:
```bash
rm -rf logs/          # Deletes all logs
rm -rf chroma_db/     # Deletes AI memory (fresh start)
```
### "How do I add documents for RAG/Q&A?"

Use the `scripts/load_documents.py` script:

```bash
# Load files
python scripts/load_documents.py my_file.pdf another_file.txt

# Load directory
python scripts/load_documents.py documents/

# Then chat with them
python main_enhanced.py --llamaindex
```

Supported: `.txt`, `.md`, `.pdf`, `.docx`

See [Loading Documents for RAG](#loading-documents-for-rag-llamaindex) for details.

### Example Session

```
🧠 AI Brain/Mind with Memory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[You] ➜ My name is Mark and I'm working on AI projects

💭 Using 0 relevant memories

[AI] ➜ Nice to meet you, Mark! AI projects are exciting. What specific 
area are you focusing on?

[You] ➜ What's my name?

💭 Using 2 relevant memories

[AI] ➜ Your name is Mark! You mentioned that earlier when you told me 
you're working on AI projects.
```

## How It Works

1. **User Input**: You type a message in the CLI
2. **Memory Retrieval**: System searches ChromaDB for relevant past conversations
3. **Context Building**: Combines relevant memories + recent history + emotional context
4. **Inference**: Sends to LLM (OpenRouter or Ollama) with context
5. **Response**: Streams AI response back to you
6. **Memory Storage**: Saves both your message and AI response with NLP analysis to ChromaDB

## 🐛 Troubleshooting

### Platform-Specific Issues

<details>
<summary><b>🍎 macOS</b></summary>

**Issue**: `ModuleNotFoundError: No module named 'mlx'`
```bash
# Solution: Reinstall dependencies
pip install -e .
```

**Issue**: `MPS backend not available`
```bash
# Solution: Update macOS to 12.3+
# Or system will fall back to CPU automatically
```

**Issue**: Permission denied when installing
```bash
# Solution: Don't use sudo with pip in venv
# Make sure venv is activated:
source .venv/bin/activate
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

**Issue**: `'python' is not recognized`
```cmd
# Solution: Use 'py' instead of 'python'
py main.py
```

**Issue**: Virtual environment activation fails
```cmd
# Solution: Use different activation script
.venv\Scripts\activate.bat   # For cmd
.venv\Scripts\Activate.ps1   # For PowerShell

# Or if PowerShell execution policy blocks:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Issue**: CUDA not detected (with NVIDIA GPU)
```cmd
# Solution: Install CUDA Toolkit
# Download from: https://developer.nvidia.com/cuda-downloads
# Restart after installation
```

**Issue**: `OSError: [WinError 126]` when loading spaCy
```cmd
# Solution: Install Visual C++ Redistributable
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
```

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Issue**: `ImportError: libcudart.so not found`
```bash
# Solution: Install CUDA Toolkit
sudo apt install nvidia-cuda-toolkit  # Ubuntu/Debian
sudo dnf install cuda                  # Fedora/RHEL
```

**Issue**: Permission denied
```bash
# Solution: Don't use sudo with pip in venv
# Make sure venv is activated:
source .venv/bin/activate
```

**Issue**: `OSError: [Errno 28] No space left on device`
```bash
# Solution: Clean up space or change ChromaDB directory
# In .env:
CHROMA_PERSIST_DIR=/path/to/larger/disk/chroma_db
```

</details>

### General Issues

**Issue**: Slow performance
- **Mac M1+**: Ensure MPS is being used (check startup messages)
- **Windows/Linux**: Install CUDA for NVIDIA GPUs
- **All**: Try a smaller embedding model or switch to Ollama for faster local inference

**Issue**: Out of memory
- Use a smaller model (e.g., `OLLAMA_MODEL=llama3.2:1b`)
- Reduce `MAX_MEMORY_ITEMS` in `.env`
- Close other applications

**Issue**: API errors with OpenRouter
- Check your API key is correct in `.env`
- Verify you have credits at [openrouter.ai](https://openrouter.ai)
- Try switching to Ollama for local inference

**Issue**: ChromaDB errors
- Delete `chroma_db` folder and restart (WARNING: deletes all memories)
- Check disk space
- Verify write permissions

## 💻 Performance

### By Platform

| Platform | GPU | Embedding Speed | Memory Retrieval |
|----------|-----|----------------|------------------|
| **Mac M1/M2/M3/M4** | MPS | ~10-20ms | <5ms |
| **Windows + NVIDIA** | CUDA | ~5-15ms | <5ms |
| **Linux + NVIDIA** | CUDA | ~5-15ms | <5ms |
| **Any (CPU only)** | CPU | ~100-200ms | <5ms |

### Inference Speed

- **OpenRouter**: 20-100ms/token (network dependent)
- **Ollama (local)**: 10-50ms/token (hardware dependent)
- **Memory operations**: <5ms

## 📁 Project Structure

```
ai-brain-memory/
├── ai_brain/                   # Core package
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration management
│   ├── memory.py              # ChromaDB memory store + topic tracking
│   ├── inference.py           # OpenRouter API + conversation summarization
│   ├── cli.py                 # Command-line interface
│   ├── enhanced_cli.py        # Enhanced CLI with mode switching
│   ├── langchain_brain.py     # LangChain integration
│   ├── llamaindex_brain.py    # LlamaIndex RAG
│   └── nlp_analyzer.py        # spaCy + RoBERTa NLP pipeline
│
├── docs/                       # Documentation
│   ├── ARCHITECTURE_REVIEW.md # Complete technical analysis
│   ├── FLOW_DIAGRAM.md        # Visual processing pipeline
│   ├── IMPLEMENTATION_PLAN.md # Prioritized roadmap
│   ├── REMAINING_ARCHITECTURE_ITEMS.md  # Progress tracking
│   ├── PHASE_2_COMPLETION_SUMMARY.md    # Phase 2 achievements
│   ├── QUERY_ENHANCEMENT.md   # Query preprocessing details
│   ├── EMOTIONAL_TRAJECTORY.md # 11-emotion system
│   ├── TIME_FORMATTING_IMPLEMENTATION.md
│   ├── TOPIC_TRACKING_IMPLEMENTATION.md
│   ├── EXTENDED_HISTORY_IMPLEMENTATION.md
│   └── CONVERSATION_SUMMARIZATION_IMPLEMENTATION.md
│
├── tests/                      # Test suite
│   ├── test_phase1_fixes.py   # Phase 1 validation
│   ├── test_emotional_tracking.py  # 11-emotion system tests
│   ├── test_query_enhancement.py   # Query preprocessing tests
│   ├── test_topic_feature.py       # Topic tracking tests
│   ├── test_conversation_summarization.py
│   └── ...                    # Additional test files
│
├── scripts/                    # Utility scripts
│   ├── inspect_metadata.py    # Inspect ChromaDB metadata
│   ├── load_documents.py      # Load docs for RAG
│   └── migrate_to_cosine.py   # Database migration
│
├── example_documents/          # Sample documents for RAG
├── main.py                    # Entry point (basic mode)
├── main_enhanced.py           # Entry point (enhanced mode)
├── pyproject.toml             # Dependencies
├── requirements.txt           # Pinned dependencies
├── .env.example               # Configuration template
└── README.md                  # This file
```

## Advanced Usage

### Quick Command Reference

```bash
# Activate environment (always first!)
source .venv/bin/activate        # Mac/Linux
.venv\Scripts\activate           # Windows

# Run modes
python main.py                        # Basic chat
python main_enhanced.py --langchain   # Advanced prompts
python main_enhanced.py --llamaindex  # Document Q&A

# Load documents for RAG
python scripts/load_documents.py file.pdf      # Single file
python scripts/load_documents.py docs/*.txt    # Multiple files
python scripts/load_documents.py documents/    # Whole directory

# Test and debug
python tests/test_config.py            # Check configuration
python tests/test_logging.py           # Test logging system
python tests/test_nlp.py              # Test NLP features

# Run all Phase 2 tests
python tests/test_topic_feature.py
python tests/test_conversation_summarization.py

# View logs
ls logs/conversations/          # Conversation JSON files
ls logs/prompts/               # System prompt logs
cat logs/prompts/prompts_*.log # View latest prompts
```

### Programmatic Access

```python
from ai_brain.memory import MemoryStore
from ai_brain.inference import AIBrain
from ai_brain.config import Config

# Initialize
memory = MemoryStore()
brain = AIBrain()

# Add a memory
memory.add_memory("User prefers Python over JavaScript", memory_type="preference")

# Retrieve memories
memories = memory.retrieve_memories("programming languages", n_results=5)

# Generate response
response = brain.generate_response(
    message="What do I prefer?",
    relevant_memories=memories,
    stream=False
)
```

## 📚 Documentation

### Architecture & Design

Comprehensive documentation on system design, flow analysis, and improvements:

- **[REVIEW_SUMMARY.md](REVIEW_SUMMARY.md)** - Executive summary of architecture review (START HERE)
- **[ARCHITECTURE_REVIEW.md](ARCHITECTURE_REVIEW.md)** - Complete technical analysis of all components
- **[FLOW_DIAGRAM.md](FLOW_DIAGRAM.md)** - Visual flow diagrams showing message processing pipeline
- **[IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md)** - Prioritized roadmap for enhancements
- **[QUERY_ENHANCEMENT.md](QUERY_ENHANCEMENT.md)** - How query preprocessing works with spaCy

### Key Insights from Architecture Review

**Current Score**: 7.5/10 → **Target**: 9.0/10

**What's Working Well**:
- ✅ Excellent separation of concerns (memory, NLP, inference, CLI)
- ✅ Dual-use spaCy analysis (pre-query routing + post-storage enrichment)
- ✅ Emotional intelligence with natural language summaries
- ✅ GPU-accelerated embeddings and sentiment analysis

**Priority Improvements**:
- 🔴 Query enhancement deduplication (fixes "Mark Mark" duplicates)
- 🔴 Hybrid search with metadata boosting (use NLP tags in retrieval)
- 🟡 Extended emotional context window (10 messages instead of 5)
- 🟡 Conversation summarization for long sessions
- 🟢 Memory consolidation for long-term scalability

See `REVIEW_SUMMARY.md` for complete details and implementation timeline.

## Troubleshooting

**Issue**: `OPENROUTER_API_KEY not set`
- **Solution**: Copy `.env.example` to `.env` and add your API key

**Issue**: Slow embeddings
- **Solution**: Ensure you're using the M4 GPU (automatic with sentence-transformers)

**Issue**: ChromaDB errors
- **Solution**: Delete `./chroma_db` folder and restart

## Future Enhancements

- [ ] Add local MLX inference option
- [ ] Implement memory consolidation
- [ ] Add multi-modal memory (images, audio)
- [ ] Memory importance scoring
- [ ] Export/import conversations
- [ ] Web interface

## License

MIT License - Feel free to use and modify!

## Contributing

This is a personal project, but suggestions are welcome!
