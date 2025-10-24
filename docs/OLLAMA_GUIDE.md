# 🦙 Using Local Ollama with AI Brain

This guide explains how to use **local Ollama models** instead of remote APIs (OpenRouter).

## Why Use Ollama?

- **🔒 Privacy**: All inference happens locally on your machine
- **💰 Free**: No API costs
- **⚡ Fast**: No network latency (once models are downloaded)
- **🌐 Offline**: Works without internet connection
- **🎯 Control**: Run any model you want (Llama, Mistral, etc.)

## Prerequisites

### 1. Install Ollama

<details>
<summary><b>🍎 macOS</b></summary>

**Option 1: Download Installer**
- Visit [ollama.ai](https://ollama.ai)
- Download the macOS installer
- Double-click to install

**Option 2: Using Terminal**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Verify Installation**
```bash
ollama --version
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

1. Visit [ollama.ai](https://ollama.ai)
2. Download the Windows installer
3. Run the installer
4. Restart your terminal/PowerShell

**Verify Installation**
```cmd
ollama --version
```

**Note**: Ollama runs as a Windows service automatically after installation.

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Installation**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Start Service** (if not auto-started)
```bash
# SystemD
sudo systemctl start ollama

# Or run manually
ollama serve
```

**Verify Installation**
```bash
ollama --version
```

</details>

### 2. Download a Model

<details>
<summary><b>All Platforms</b></summary>

```bash
# Recommended models:
ollama pull llama3.2          # Fast, good quality (7B)
ollama pull llama3.2:1b       # Very fast, smaller (1B)
ollama pull mistral           # Alternative option (7B)
ollama pull phi3              # Compact model (3.8B)
```

**Model sizes**:
- **1B models**: ~1GB download, very fast
- **7B models**: ~4GB download, good balance
- **13B models**: ~7GB download, better quality
- **70B+ models**: 40GB+, best quality (requires powerful GPU)

</details>

### 3. Verify Ollama is Running

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

```bash
# Check running models
ollama list

# Check if service is running
ollama ps
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Check running models
ollama list

# Check if service is running
ollama ps

# If not running, start it
# (Usually auto-starts as Windows service)
```

**Service Management** (Windows):
```cmd
# Check service status
sc query ollama

# Start service
net start ollama

# Stop service
net stop ollama
```

</details>

## Configuration

### Option 1: Environment Variable (Recommended)

Edit your `.env` file:

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

```bash
# Edit with your preferred editor
nano .env
# or
vim .env
# or
code .env  # VS Code
```

Update these lines:
```bash
# Change from openrouter to ollama
LLM_BACKEND=ollama

# Specify the model you downloaded
OLLAMA_MODEL=llama3.2

# Default URL (usually doesn't need changing)
OLLAMA_BASE_URL=http://localhost:11434
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

```cmd
# Edit with Notepad
notepad .env

# Or use your preferred editor
code .env  # VS Code
```

Update these lines:
```bash
# Change from openrouter to ollama
LLM_BACKEND=ollama

# Specify the model you downloaded
OLLAMA_MODEL=llama3.2

# Default URL (usually doesn't need changing)
OLLAMA_BASE_URL=http://localhost:11434
```

</details>

### Option 2: Quick Test (No File Editing)

<details>
<summary><b>🍎 macOS / 🐧 Linux</b></summary>

```bash
LLM_BACKEND=ollama python main.py
```

</details>

<details>
<summary><b>🪟 Windows (Command Prompt)</b></summary>

```cmd
set LLM_BACKEND=ollama
python main.py
```

</details>

<details>
<summary><b>🪟 Windows (PowerShell)</b></summary>

```powershell
$env:LLM_BACKEND="ollama"
python main.py
```

</details>

## Usage

Once configured, the AI Brain works exactly the same:

```bash
# Basic mode
python main.py

# Enhanced mode with LangChain
python run_enhanced.py --langchain

# Enhanced mode with LlamaIndex
python run_enhanced.py --llamaindex
```

You'll see a message on startup:
```
ℹ️  Using local Ollama at http://localhost:11434
   Model: llama3.2
```

## Comparing OpenRouter vs Ollama

| Feature | OpenRouter | Ollama |
|---------|-----------|--------|
| **Cost** | Pay per token | Free |
| **Privacy** | Data sent to API | 100% local |
| **Speed** | Network dependent | Local (fast after warmup) |
| **Models** | Access to GPT-4, Claude, etc. | Open source models |
| **Quality** | Best models available | Good, improving |
| **Setup** | Just API key | Install + download models |
| **Internet** | Required | Not required |

## Recommended Models

### For Chat & Conversation
- **llama3.2** - Best balance (7B parameters)
- **mistral** - Fast and capable (7B)
- **phi3** - Compact and efficient (3.8B)

### For Specific Tasks
- **llama3.2:70b** - Highest quality (requires powerful GPU)
- **codellama** - Code generation
- **llama3.2:1b** - Very fast, minimal resources

### Check Available Models
```bash
ollama list
ollama show llama3.2  # Show model details
```

## Performance Tips

### 1. GPU Acceleration
Ollama automatically uses your GPU:
- **Mac**: Uses Metal (MPS) automatically
- **Windows/Linux**: Uses NVIDIA CUDA if available

### 2. Model Size vs Speed
- **1B models**: Very fast, good for simple tasks
- **7B models**: Good balance (llama3.2, mistral)
- **70B+ models**: Best quality, requires powerful hardware

### 3. Warmup
First response may be slow as model loads. Subsequent responses are faster.

## Switching Between Backends

You can easily switch between OpenRouter and Ollama:

```bash
# Use OpenRouter
LLM_BACKEND=openrouter python main.py

# Use Ollama
LLM_BACKEND=ollama OLLAMA_MODEL=llama3.2 python main.py
```

Or edit your `.env` file to set the default.

## Troubleshooting

### Platform-Specific Issues

<details>
<summary><b>🍎 macOS</b></summary>

**Issue**: "Connection refused"

**Solution 1**: Start Ollama
```bash
ollama serve
```

**Solution 2**: Check if Ollama app is running
- Look for Ollama icon in menu bar
- If not running, launch Ollama from Applications

**Issue**: Port already in use

**Solution**: Change port
```bash
OLLAMA_HOST=0.0.0.0:8080 ollama serve
```

Then update `.env`:
```bash
OLLAMA_BASE_URL=http://localhost:8080
```

</details>

<details>
<summary><b>🪟 Windows</b></summary>

**Issue**: "Connection refused"

**Solution 1**: Check service status
```cmd
sc query ollama
```

**Solution 2**: Start service
```cmd
net start ollama
```

**Solution 3**: Restart Ollama
```cmd
net stop ollama
net start ollama
```

**Issue**: Service won't start

**Solution**: Run Ollama manually
```cmd
ollama serve
```

**Issue**: Firewall blocking

**Solution**: Add firewall exception
- Open Windows Defender Firewall
- Allow Ollama through firewall
- Or temporarily disable for testing

</details>

<details>
<summary><b>🐧 Linux</b></summary>

**Issue**: "Connection refused"

**Solution 1**: Start service
```bash
sudo systemctl start ollama
```

**Solution 2**: Enable auto-start
```bash
sudo systemctl enable ollama
```

**Solution 3**: Run manually
```bash
ollama serve
```

**Issue**: Permission denied

**Solution**: Add user to ollama group
```bash
sudo usermod -aG ollama $USER
```

Then log out and back in.

**Issue**: Port conflict

**Solution**: Change port
```bash
OLLAMA_HOST=0.0.0.0:8080 ollama serve
```

</details>

### General Issues

**Issue**: "Model not found"

**Solution**: Pull the model first
```bash
ollama pull llama3.2
```

**Issue**: Slow responses

**Solution**: 
- Try a smaller model (llama3.2:1b)
- Check if GPU is being used
- Ensure nothing else is using GPU/RAM

### Issue: Out of memory
**Solution**:
- Use smaller model (1B or 3B parameters)
- Close other applications
- Check available RAM with `ollama show <model>`

## Example Session

```bash
# Setup
ollama pull llama3.2

# Configure
echo "LLM_BACKEND=ollama" >> .env
echo "OLLAMA_MODEL=llama3.2" >> .env

# Run
python main.py
```

Output:
```
🖥️  System Information:
   OS: Darwin 24.6.0
   Platform: arm64
   Python: 3.13.7

🚀 Compute Device:
   Device: Apple Silicon GPU (MPS)
   Type: mps

ℹ️  Using local Ollama at http://localhost:11434
   Model: llama3.2

🧠 Initializing memory store at chroma_db...
✅ Memory store initialized with 13 memories
   Using device: Apple Silicon GPU (MPS)

🤖 AI Brain initialized with Ollama model: llama3.2
   Base URL: http://localhost:11434

💬 Welcome to AI Brain! (Type 'exit' to quit)
```

## Advanced Configuration

### Custom Ollama Port
If running Ollama on a different port:
```bash
OLLAMA_BASE_URL=http://localhost:8080
```

### Multiple Models
Switch models easily:
```bash
# Use different model
OLLAMA_MODEL=mistral python main.py
```

### Model Parameters
Some models have variants:
```bash
ollama pull llama3.2:latest    # Default
ollama pull llama3.2:1b        # 1B version
ollama pull llama3.2:70b       # 70B version
```

## Learn More

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Available Models](https://ollama.ai/library)
- [Model Comparison](https://ollama.ai/library?sort=popular)
