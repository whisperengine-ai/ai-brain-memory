# Quick Start: Using RAG with Documents

This guide shows you how to load documents and ask questions about them.

## Step-by-Step Example

### 1. Activate Environment
```bash
cd ai-brain-memory
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2. Load Documents

**Option A: Load the example document (to test)**
```bash
python load_documents.py example_documents/about_ai_brain.md
```

**Option B: Load your own documents**
```bash
# Create a folder for your docs
mkdir my_research

# Add your files
cp ~/Downloads/research_paper.pdf my_research/
cp ~/Documents/notes.txt my_research/

# Load them
python load_documents.py my_research/
```

**Output:**
```
📁 Loading 2 file(s) into LlamaIndex RAG...
🧠 Initializing ChromaDB...
🦙 Initializing LlamaIndex RAG...
   Using device: Apple Silicon GPU (MPS)
✅ LlamaIndex RAG initialized

📄 Loading documents...
✅ Loaded 1 document(s) from research_paper.pdf
✅ Loaded 1 document(s) from notes.txt

✅ Successfully loaded 2 document(s)
```

### 3. Start Chatting with Documents
```bash
python main_enhanced.py --llamaindex
```

### 4. Ask Questions

**Example session:**
```
[You] ➜ What are the main topics in these documents?
💭 Using 3 relevant documents
[AI] ➜ Based on the loaded documents, the main topics are...

[You] ➜ Summarize the key findings
💭 Using 2 relevant documents
[AI] ➜ The key findings include...

[You] ➜ What does it say about methodology?
💭 Using 4 relevant documents
[AI] ➜ According to the documents, the methodology involves...
```

## Supported File Types

- ✅ `.txt` - Plain text
- ✅ `.md` - Markdown
- ✅ `.pdf` - PDF documents
- ✅ `.docx` - Word documents

## Tips

### Loading Multiple Files
```bash
# Load all PDFs in a folder
python load_documents.py research/*.pdf

# Load entire directory
python load_documents.py my_documents/

# Load specific files
python load_documents.py file1.pdf file2.txt file3.md
```

### Organizing Documents
```bash
# Create topic-based folders
mkdir project_docs
mkdir research_papers
mkdir meeting_notes

# Load each separately
python load_documents.py project_docs/
python load_documents.py research_papers/
python load_documents.py meeting_notes/
```

### Checking Loaded Documents
After loading, you can ask:
- "What documents do you have?"
- "List all the files you've loaded"
- "What topics are covered in your knowledge base?"

## Persistent Storage

Documents are stored in `chroma_db/` and persist across sessions:
- ✅ Load once, query forever
- ✅ Add more documents anytime
- ⚠️  Delete `chroma_db/` to start fresh

## Troubleshooting

**Problem:** "File not found"
```bash
# Use absolute paths or check file location
python load_documents.py /full/path/to/file.pdf
```

**Problem:** "Failed to load PDF"
```bash
# Make sure PDF isn't password protected
# Try converting to text first
```

**Problem:** "No documents in directory"
```bash
# Check directory has supported files
ls my_documents/  # Should show .txt, .md, .pdf, .docx files
```

## Next Steps

Once documents are loaded:
1. Ask specific questions
2. Request summaries
3. Compare information across documents
4. Extract key facts
5. Generate insights

The AI will use both the documents AND conversation memory to answer!
