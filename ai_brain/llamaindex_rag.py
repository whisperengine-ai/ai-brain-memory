"""LlamaIndex-based RAG pipeline for advanced memory retrieval."""

from typing import List, Dict, Optional
from llama_index.core import (
    VectorStoreIndex,
    Document,
    StorageContext,
    Settings,
    PromptTemplate
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.chat_engine import CondensePlusContextChatEngine
import chromadb
from datetime import datetime

from .config import Config
from .device_utils import get_torch_device, get_device


class LlamaIndexRAG:
    """
    Advanced RAG (Retrieval Augmented Generation) using LlamaIndex
    for sophisticated memory retrieval and context generation.
    """
    
    def __init__(self, chroma_client: chromadb.PersistentClient, collection_name: str):
        """Initialize LlamaIndex RAG components."""
        print("🦙 Initializing LlamaIndex RAG...")
        
        # Get device info
        device_type, device_desc = get_device()
        torch_device = get_torch_device()
        print(f"   Using device: {device_desc}")
        
        # Configure LlamaIndex settings with proper device
        Settings.embed_model = HuggingFaceEmbedding(
            model_name=Config.EMBEDDING_MODEL,
            device=torch_device
        )
        
        backend = Config.LLM_BACKEND.lower()
        
        if backend == "ollama":
            # Use local Ollama
            Settings.llm = OpenAI(
                api_base=f"{Config.OLLAMA_BASE_URL}/v1",
                api_key="ollama",
                model=Config.OLLAMA_MODEL,
                temperature=0.7,
            )
            print(f"   Using Ollama model: {Config.OLLAMA_MODEL}")
        else:
            # Use OpenRouter (default)
            Settings.llm = OpenAI(
                api_base=Config.OPENROUTER_BASE_URL,
                api_key=Config.OPENROUTER_API_KEY,
                model=Config.OPENROUTER_MODEL,
                temperature=0.7,
            )
            print(f"   Using OpenRouter model: {Config.OPENROUTER_MODEL}")
        
        # Get ChromaDB collection
        self.chroma_collection = chroma_client.get_or_create_collection(
            name=collection_name
        )
        
        # Create ChromaDB vector store
        self.vector_store = ChromaVectorStore(
            chroma_collection=self.chroma_collection
        )
        
        # Create storage context
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        
        # Create or load index
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            storage_context=self.storage_context
        )
        
        # Create chat memory
        self.chat_memory = ChatMemoryBuffer.from_defaults(token_limit=4096)
        
        # Custom prompt templates
        self._setup_custom_prompts()
        
        print("✅ LlamaIndex RAG initialized")
    
    def _setup_custom_prompts(self):
        """Setup custom prompt templates for RAG."""
        # Context prompt for retrieved memories
        self.context_prompt = PromptTemplate(
            "You are an advanced AI assistant with persistent memory and emotional intelligence.\n\n"
            "CAPABILITIES:\n"
            "- Access to long-term memory from previous conversations\n"
            "- Awareness of emotional context and user sentiment\n"
            "- Ability to recall facts, preferences, and interaction history\n\n"
            "Context information from past conversations:\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n\n"
            "INSTRUCTIONS:\n"
            "- Use the context information to provide personalized responses\n"
            "- Reference relevant memories naturally when appropriate\n"
            "- Be aware of emotional context and adjust your tone accordingly\n"
            "- Maintain conversation continuity and show understanding\n"
            "- Be helpful, accurate, and make the user feel remembered\n\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        
        # Condensing prompt for follow-up questions
        self.condense_prompt = PromptTemplate(
            "Given the conversation history:\n"
            "{chat_history}\n\n"
            "And the follow-up question: {question}\n"
            "Rephrase the follow-up question to be a standalone question."
        )
    
    def add_memory(
        self,
        content: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Add a memory/document to the index.
        
        Args:
            content: The content to remember
            metadata: Additional metadata
            
        Returns:
            Document ID
        """
        doc_metadata = {
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }
        
        document = Document(
            text=content,
            metadata=doc_metadata
        )
        
        # Insert into index
        self.index.insert(document)
        
        return document.doc_id
    
    def load_documents_from_files(
        self,
        file_paths: List[str],
        metadata: Optional[Dict] = None
    ) -> int:
        """
        Load documents from files into the RAG index.
        
        Supports: .txt, .md, .pdf, .docx (if dependencies installed)
        
        Args:
            file_paths: List of file paths to load
            metadata: Additional metadata to add to all documents
            
        Returns:
            Number of documents successfully loaded
        """
        from llama_index.core import SimpleDirectoryReader
        from pathlib import Path
        
        loaded_count = 0
        
        for file_path in file_paths:
            try:
                path = Path(file_path)
                if not path.exists():
                    print(f"⚠️  File not found: {file_path}")
                    continue
                
                # Load document
                if path.is_file():
                    documents = SimpleDirectoryReader(
                        input_files=[str(path)]
                    ).load_data()
                elif path.is_dir():
                    documents = SimpleDirectoryReader(
                        input_dir=str(path)
                    ).load_data()
                else:
                    print(f"⚠️  Invalid path: {file_path}")
                    continue
                
                # Add metadata
                for doc in documents:
                    doc.metadata["source"] = str(file_path)
                    doc.metadata["loaded_at"] = datetime.now().isoformat()
                    if metadata:
                        doc.metadata.update(metadata)
                
                # Insert into index
                for doc in documents:
                    self.index.insert(doc)
                    loaded_count += 1
                
                print(f"✅ Loaded {len(documents)} document(s) from {path.name}")
                
            except Exception as e:
                print(f"❌ Failed to load {file_path}: {e}")
        
        return loaded_count
    
    def query(
        self,
        query_text: str,
        top_k: int = None,
        stream: bool = False
    ):
        """
        Query the RAG system for relevant information.
        
        Args:
            query_text: Query string
            top_k: Number of relevant documents to retrieve
            stream: Whether to stream the response
            
        Returns:
            Response from the query engine
        """
        if top_k is None:
            top_k = Config.MEMORY_CONTEXT_SIZE
        
        # Create query engine
        query_engine = self.index.as_query_engine(
            similarity_top_k=top_k,
            text_qa_template=self.context_prompt,
            streaming=stream
        )
        
        # Execute query
        response = query_engine.query(query_text)
        
        if stream:
            return response.response_gen
        else:
            return response.response
    
    def chat(
        self,
        message: str,
        stream: bool = True
    ):
        """
        Interactive chat with RAG and memory.
        
        Args:
            message: User message
            stream: Whether to stream response
            
        Yields:
            Response chunks or complete response
        """
        # Create chat engine with context
        chat_engine = self.index.as_chat_engine(
            chat_mode="condense_plus_context",
            memory=self.chat_memory,
            context_prompt=self.context_prompt,
            condense_prompt=self.condense_prompt,
            streaming=stream,
            similarity_top_k=Config.MEMORY_CONTEXT_SIZE
        )
        
        # Get response
        response = chat_engine.chat(message)
        
        if stream:
            for chunk in response.response_gen:
                yield chunk
        else:
            yield response.response
    
    def retrieve_relevant_context(
        self,
        query: str,
        top_k: int = None
    ) -> List[Dict]:
        """
        Retrieve relevant context without generating a response.
        
        Args:
            query: Query text
            top_k: Number of results
            
        Returns:
            List of relevant documents with metadata
        """
        if top_k is None:
            top_k = Config.MEMORY_CONTEXT_SIZE
        
        retriever = self.index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)
        
        results = []
        for node in nodes:
            results.append({
                "content": node.text,
                "metadata": node.metadata,
                "score": node.score
            })
        
        return results
    
    def clear_chat_history(self):
        """Clear the chat memory."""
        self.chat_memory.reset()
        print("🧹 Chat history cleared")
    
    def get_stats(self) -> Dict:
        """Get statistics about the RAG system."""
        return {
            "total_documents": len(self.index.docstore.docs),
            "embedding_model": Config.EMBEDDING_MODEL,
            "llm_model": Config.OPENROUTER_MODEL
        }
