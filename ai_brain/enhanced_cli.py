"""Enhanced CLI with LangChain and LlamaIndex integration."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from datetime import datetime
from pathlib import Path

from .config import Config
from .memory import MemoryStore
from .langchain_brain import LangChainBrain
from .llamaindex_rag import LlamaIndexRAG
from .logger import get_logger


class EnhancedChatInterface:
    """Enhanced interactive command-line chat interface with LangChain and LlamaIndex."""
    
    def __init__(self, use_langchain: bool = True, use_llamaindex: bool = False):
        """
        Initialize enhanced chat interface.
        
        Args:
            use_langchain: Use LangChain for conversation management
            use_llamaindex: Use LlamaIndex for advanced RAG
        """
        self.console = Console()
        self.memory = None
        self.brain = None
        self.rag = None
        self.session = None
        self.use_langchain = use_langchain
        self.use_llamaindex = use_llamaindex
        self.logger = get_logger()
        
    def initialize(self):
        """Initialize components."""
        # Validate config
        if not Config.validate():
            self.console.print("[red]❌ Configuration error. Please check your .env file.[/red]")
            return False
        
        # Initialize memory store
        try:
            self.memory = MemoryStore()
        except Exception as e:
            self.console.print(f"[red]❌ Failed to initialize memory: {e}[/red]")
            return False
        
        # Initialize AI brain (LangChain or basic)
        try:
            if self.use_langchain:
                self.brain = LangChainBrain()
                self.console.print("[green]✨ Using LangChain for advanced conversation management[/green]")
            else:
                from .inference import AIBrain
                self.brain = AIBrain()
        except Exception as e:
            self.console.print(f"[red]❌ Failed to initialize AI brain: {e}[/red]")
            return False
        
        # Initialize LlamaIndex RAG (optional)
        if self.use_llamaindex:
            try:
                self.rag = LlamaIndexRAG(
                    chroma_client=self.memory.client,
                    collection_name=f"{Config.CHROMA_COLLECTION_NAME}_rag"
                )
                self.console.print("[green]✨ Using LlamaIndex for advanced RAG[/green]")
            except Exception as e:
                self.console.print(f"[yellow]⚠️  LlamaIndex initialization failed: {e}[/yellow]")
                self.console.print("[yellow]Continuing with basic memory retrieval...[/yellow]")
                self.use_llamaindex = False
        
        # Initialize prompt session with history
        history_file = Path.home() / ".ai_brain_history"
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
        )
        
        return True
    
    def show_welcome(self):
        """Show welcome message."""
        # Get device info dynamically
        from .device_utils import detect_device
        device_type, device_desc = detect_device()
        
        # Format device line based on detected hardware
        if device_type == "mps":
            device_line = f"- ✅ Fast embeddings on {device_desc}"
        elif device_type == "cuda":
            device_line = f"- ✅ GPU-accelerated embeddings ({device_desc})"
        else:
            device_line = "- ✅ CPU-based embeddings"
        
        # Get LLM backend info dynamically
        if Config.LLM_BACKEND == "ollama":
            llm_model = Config.OLLAMA_MODEL
            llm_line = f"- ✅ Powered by {llm_model} (Ollama - Local)"
        elif Config.LLM_BACKEND == "openrouter":
            llm_model = Config.OPENROUTER_MODEL.split('/')[-1] if '/' in Config.OPENROUTER_MODEL else Config.OPENROUTER_MODEL
            llm_line = f"- ✅ Powered by {llm_model} via OpenRouter"
        else:
            llm_model = "Unknown"
            llm_line = f"- ✅ LLM Backend: {Config.LLM_BACKEND}"
        
        # Get embedding model info
        embedding_model = Config.EMBEDDING_MODEL.split('/')[-1] if '/' in Config.EMBEDDING_MODEL else Config.EMBEDDING_MODEL
        
        mode_info = []
        if self.use_langchain:
            mode_info.append("🔗 LangChain (Advanced Prompts & Chains)")
        if self.use_llamaindex:
            mode_info.append("🦙 LlamaIndex (Advanced RAG)")
        else:
            mode_info.append("🧠 Basic Pipeline")
        
        mode_str = " + ".join(mode_info)
        
        welcome = f"""
# 🧠 AI Brain/Mind with Memory

**Mode**: {mode_str}

Welcome to your AI assistant with persistent memory!

**Commands:**
- `/help` - Show this help message
- `/stats` - Show memory statistics
- `/clear` - Clear all memories
- `/mode` - Switch between LangChain/LlamaIndex/Basic modes
- `/exit` or `/quit` - Exit the chat

**Features:**
- ✅ Persistent memory across sessions (ChromaDB)
- ✅ Semantic memory retrieval with hybrid search
- ✅ Context-aware responses with query enhancement
- ✅ **11-emotion detection** (joy, love, sadness, anger, fear, etc.)
- ✅ **Mixed emotion recognition** (conflicting feelings)
- ✅ Emotional trajectory tracking (improving/declining/volatile)
- ✅ Dynamic tone adaptation based on user emotions
- ✅ Entity extraction and keyword analysis
{llm_line}
- ✅ Embeddings: {embedding_model}
{device_line}

Start chatting below!
        """
        self.console.print(Panel(Markdown(welcome), border_style="green"))
    
    def run(self):
        """Run the chat interface."""
        if not self.initialize():
            return
        
        self.show_welcome()
        
        while True:
            try:
                # Get user input
                self.console.print()
                user_input = self.session.prompt(HTML('<ansibrightcyan><b>[You] ➜</b></ansibrightcyan> '))
                
                if not user_input.strip():
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    if not self.handle_command(user_input):
                        break
                    continue
                
                # Process message
                self.process_message(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Use /exit to quit[/yellow]")
                continue
            except EOFError:
                break
        
        self.console.print("\n[green]👋 Goodbye![/green]")
    
    def handle_command(self, command: str) -> bool:
        """Handle special commands."""
        cmd = command.lower().strip()
        
        if cmd in ["/exit", "/quit"]:
            return False
        
        elif cmd == "/help":
            self.show_welcome()
        
        elif cmd == "/stats":
            self.show_stats()
        
        elif cmd == "/clear":
            if Prompt.ask("Are you sure you want to clear all memories?", 
                         choices=["y", "n"], default="n") == "y":
                self.memory.clear_all_memories()
                if self.use_langchain:
                    self.brain.clear_conversation_memory()
                if self.use_llamaindex:
                    self.rag.clear_chat_history()
                self.console.print("[green]✅ All memories cleared[/green]")
        
        elif cmd == "/mode":
            self.show_mode_info()
        
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self.console.print("[yellow]Type /help for available commands[/yellow]")
        
        return True
    
    def show_stats(self):
        """Show memory statistics."""
        stats = self.memory.get_stats()
        
        mode = "LangChain" if self.use_langchain else "Basic"
        if self.use_llamaindex:
            mode += " + LlamaIndex"
        
        stats_text = f"""
## 📊 Memory Statistics

- **Total Memories:** {stats['total_memories']}
- **Collection:** {stats['collection_name']}
- **Storage:** {stats['persist_dir']}
- **Model:** {Config.OPENROUTER_MODEL}
- **Pipeline Mode:** {mode}
        """
        
        if self.use_llamaindex:
            rag_stats = self.rag.get_stats()
            stats_text += f"\n- **RAG Documents:** {rag_stats['total_documents']}"
        
        self.console.print(Panel(Markdown(stats_text), border_style="blue"))
    
    def show_mode_info(self):
        """Show current mode information."""
        info = f"""
## 🔧 Current Configuration

- **LangChain:** {"✅ Enabled" if self.use_langchain else "❌ Disabled"}
- **LlamaIndex RAG:** {"✅ Enabled" if self.use_llamaindex else "❌ Disabled"}
- **Embedding Model:** {Config.EMBEDDING_MODEL}
- **LLM Model:** {Config.OPENROUTER_MODEL}

To change modes, edit the code in `main.py` or create command-line flags.
        """
        self.console.print(Panel(Markdown(info), border_style="yellow"))
    
    def process_message(self, user_message: str):
        """Process user message and generate response."""
        # Analyze incoming message with spaCy to enhance query
        from .nlp_analyzer import get_analyzer
        analyzer = get_analyzer()
        query_analysis = analyzer.enhance_query(user_message)
        
        # Show query enhancement in CLI (optional debug info)
        if query_analysis["entity_values"] or query_analysis["top_keywords"]:
            focus_items = query_analysis["entity_values"][:2] if query_analysis["entity_values"] else query_analysis["top_keywords"][:2]
            if focus_items:
                self.console.print(f"[dim]🔍 Query focus: {', '.join(focus_items)}[/dim]")
        
        # Retrieve relevant memories using enhanced query WITH hybrid search
        relevant_memories = self.memory.retrieve_memories(
            query=query_analysis["enhanced_query"],
            n_results=Config.MEMORY_CONTEXT_SIZE,
            query_analysis=query_analysis  # Pass for metadata boosting
        )
        
        # Get recent conversation history for emotional context
        conversation_history = self.memory.get_conversation_history(n_recent=10)
        
        # Log system prompt for debugging
        if self.use_langchain and self.brain:
            # Get the full system message that will be sent to LLM
            system_message = self.brain._build_system_message(
                relevant_memories, conversation_history, query_analysis
            ) if hasattr(self.brain, '_build_system_message') else "N/A"
            
            # Add note about recent messages that will be added separately
            full_prompt = system_message
            if conversation_history:
                # Use all 10 messages to match emotional trajectory analysis window
                recent_turns = conversation_history[-10:]
                full_prompt += "\n\n=== RECENT MESSAGES (Added to chat history) ==="
                full_prompt += f"\n(Last {len(recent_turns)} messages will be added as proper chat messages)"
                for conv in recent_turns[:3]:  # Show preview of first 3
                    role = "User" if conv.get('metadata', {}).get('role') == 'user' else "Assistant"
                    content_preview = conv.get('content', '')[:80]
                    full_prompt += f"\n{role}: {content_preview}..."
                if len(recent_turns) > 3:
                    full_prompt += f"\n... and {len(recent_turns) - 3} more messages"
            
            self.logger.log_system_prompt(
                prompt=full_prompt,
                context_type="langchain",
                metadata={
                    "num_memories": len(relevant_memories),
                    "num_history": len(conversation_history),
                    "user_message_preview": user_message[:100]
                }
            )
        elif self.use_llamaindex:
            self.logger.log_system_prompt(
                prompt="LlamaIndex RAG Mode (system prompt built internally)",
                context_type="llamaindex",
                metadata={
                    "user_message_preview": user_message[:100]
                }
            )
        
        # Show memory context if any
        if relevant_memories:
            self.console.print(f"[dim]💭 Using {len(relevant_memories)} relevant memories[/dim]")
        
        # Show emotional context hint if available
        if conversation_history:
            try:
                from .nlp_analyzer import get_analyzer
                analyzer = get_analyzer()
                latest_msg = conversation_history[0] if conversation_history else None
                if latest_msg and "metadata" in latest_msg:
                    meta = latest_msg["metadata"]
                    if "user_emotion" in meta:
                        emotion = meta["user_emotion"]
                        self.console.print(f"[dim]😊 Detected emotion: {emotion}[/dim]")
            except:
                pass
        
        # Generate response
        self.console.print("\n[bold green][AI] ➜[/bold green] ", end="")
        
        response_text = ""
        error_occurred = False
        try:
            if self.use_llamaindex:
                # Use LlamaIndex RAG chat
                for chunk in self.rag.chat(user_message, stream=True):
                    self.console.print(chunk, end="")
                    response_text += chunk
            elif self.use_langchain:
                # Use LangChain brain with streaming
                for chunk in self.brain.generate_response_streaming(
                    message=user_message,
                    relevant_memories=relevant_memories,
                    conversation_history=conversation_history,
                    query_analysis=query_analysis
                ):
                    self.console.print(chunk, end="")
                    response_text += chunk
            else:
                # Use basic inference
                for chunk in self.brain.generate_response(
                    message=user_message,
                    relevant_memories=relevant_memories,
                    conversation_history=conversation_history,
                    stream=True
                ):
                    self.console.print(chunk, end="")
                    response_text += chunk
        except Exception as e:
            self.console.print(f"\n[red]❌ Error: {e}[/red]")
            error_occurred = True
            return
        
        self.console.print()  # Newline after response
        
        # Only store conversation in memory if no error occurred
        if not error_occurred and response_text.strip():
            timestamp = datetime.now().isoformat()
            
            # Store user message with NLP analysis
            self.memory.add_memory(
                content=user_message,
                memory_type="conversation",
                metadata={"role": "user", "timestamp": timestamp},
                enable_nlp=True  # Enable NLP enrichment
            )
            
            # Store AI response with NLP analysis
            self.memory.add_memory(
                content=response_text,
                memory_type="conversation",
                metadata={"role": "assistant", "timestamp": timestamp},
                enable_nlp=True  # Enable NLP enrichment
            )
            
            # Also add to LlamaIndex if enabled
            if self.use_llamaindex:
                self.rag.add_memory(
                    content=f"User: {user_message}\nAssistant: {response_text}",
                    metadata={"timestamp": timestamp}
                )
            
            # Log the conversation turn
            self.logger.log_conversation_turn(
                user_message=user_message,
                bot_response=response_text,
                metadata={
                    "timestamp": timestamp,
                    "mode": "llamaindex" if self.use_llamaindex else ("langchain" if self.use_langchain else "basic"),
                    "num_memories_used": len(relevant_memories),
                    "response_length": len(response_text)
                }
            )


def main():
    """Main entry point with mode selection."""
    import sys
    
    # Parse command line arguments
    use_langchain = "--langchain" in sys.argv or "--lc" in sys.argv or True  # Default to True
    use_llamaindex = "--llamaindex" in sys.argv or "--li" in sys.argv
    
    chat = EnhancedChatInterface(
        use_langchain=use_langchain,
        use_llamaindex=use_llamaindex
    )
    chat.run()


if __name__ == "__main__":
    main()
