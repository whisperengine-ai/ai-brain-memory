# Example Documents

This folder contains sample documents to test the LlamaIndex RAG system.

## Quick Test

Try loading the example document:

```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python scripts/load_documents.py example_documents/about_ai_brain.md
python main_enhanced.py --llamaindex
```

Then ask questions like:
- "What is this AI Brain project about?"
- "What frameworks does it use?"
- "How does cross-platform support work?"

## Add Your Own Documents

You can add your own files here:
- `.txt` - Plain text files
- `.md` - Markdown files
- `.pdf` - PDF documents
- `.docx` - Word documents

Then load them:
```bash
python scripts/load_documents.py example_documents/
```

## Privacy Note

Add your personal documents to a different folder (e.g., `my_documents/`) to keep them separate from the example. Your documents won't be committed to git.
