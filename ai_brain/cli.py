"""Command-line interface for AI Brain chat."""

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from datetime import datetime
from pathlib import Path

from .config import Config
from .memory import MemoryStore
from .inference import AIBrain
from .logger import get_logger


class ChatInterface:
    """Interactive command-line chat interface."""
    
    def __init__(self):
        """Initialize chat interface."""
        self.console = Console()
        self.memory = None
        self.brain = None
        self.session = None
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
        
        # Initialize AI brain
        try:
            self.brain = AIBrain()
        except Exception as e:
            self.console.print(f"[red]❌ Failed to initialize AI brain: {e}[/red]")
            return False
        
        # Initialize prompt session with history
        history_file = Path.home() / ".ai_brain_history"
        self.session = PromptSession(
            history=FileHistory(str(history_file)),
            auto_suggest=AutoSuggestFromHistory(),
        )
        
        return True
    
    def _format_time_ago(self, timestamp: str) -> str:
        """
        Format timestamp as human-readable 'time ago' string.
        
        Args:
            timestamp: ISO format timestamp string
            
        Returns:
            Human-readable time string like "2 hours ago" or "3 days ago"
        """
        try:
            ts = datetime.fromisoformat(timestamp)
            now = datetime.now()
            delta = now - ts
            
            if delta.days > 0:
                return f"{delta.days} day{'s' if delta.days != 1 else ''} ago"
            elif delta.seconds >= 3600:
                hours = delta.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
            elif delta.seconds >= 60:
                minutes = delta.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                return "just now"
        except Exception:
            return "recently"
    
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
        
        welcome = f"""
# 🧠 AI Brain/Mind with Memory

Welcome to your AI assistant with persistent memory!

**Commands:**
- `/help` - Show this help message
- `/stats` - Show memory statistics
- `/topics` - Show conversation topic analysis
- `/clear` - Clear all memories
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
        """
        Handle special commands.
        
        Returns:
            False if should exit, True otherwise
        """
        cmd = command.lower().strip()
        
        if cmd in ["/exit", "/quit"]:
            return False
        
        elif cmd == "/help":
            self.show_welcome()
        
        elif cmd == "/stats":
            self.show_stats()
        
        elif cmd == "/topics":
            self.show_topics()
        
        elif cmd == "/clear":
            if Prompt.ask("Are you sure you want to clear all memories?", 
                         choices=["y", "n"], default="n") == "y":
                self.memory.clear_all_memories()
                self.console.print("[green]✅ All memories cleared[/green]")
        
        else:
            self.console.print(f"[red]Unknown command: {command}[/red]")
            self.console.print("[yellow]Type /help for available commands[/yellow]")
        
        return True
    
    def show_stats(self):
        """Show memory statistics."""
        stats = self.memory.get_stats()
        
        stats_text = f"""
## 📊 Memory Statistics

- **Total Memories:** {stats['total_memories']}
- **Collection:** {stats['collection_name']}
- **Storage:** {stats['persist_dir']}
- **Model:** {Config.OPENROUTER_MODEL}
        """
        self.console.print(Panel(Markdown(stats_text), border_style="blue"))
    
    def show_topics(self):
        """Show conversation topic statistics."""
        self.console.print("\n[cyan]📚 Analyzing conversation topics...[/cyan]")
        
        topics = self.memory.get_topic_statistics()
        
        if not topics:
            self.console.print("[yellow]No topics found yet. Start chatting to build up conversation history![/yellow]")
            return
        
        # Build markdown table
        topic_lines = ["## 📊 Conversation Topics\n"]
        topic_lines.append("| Topic | Mentions | Sentiment | Emotions |")
        topic_lines.append("|-------|----------|-----------|----------|")
        
        for topic, stats in list(topics.items())[:15]:  # Show top 15
            count = stats['count']
            sentiment = stats['dominant_sentiment']
            
            # Format sentiment with emoji
            sentiment_emoji = {
                'positive': '😊',
                'neutral': '😐',
                'negative': '😞'
            }
            sentiment_str = f"{sentiment_emoji.get(sentiment, '😐')} {sentiment}"
            
            # Format emotions
            emotions = stats.get('dominant_emotions', [])
            emotions_str = ", ".join(emotions[:2]) if emotions else "-"
            
            topic_lines.append(f"| **{topic}** | {count} | {sentiment_str} | {emotions_str} |")
        
        # Add summary
        topic_lines.append(f"\n*Showing top {min(len(topics), 15)} topics out of {len(topics)} total*")
        
        self.console.print(Panel(
            Markdown("\n".join(topic_lines)),
            border_style="cyan",
            title="💬 Topic Analysis"
        ))
    
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
        
        # Get recent conversation history
        conversation_history = self.memory.get_conversation_history(n_recent=10)
        
        # Check if user is asking about past topics
        topic_keywords = ["talked about", "discussed", "topics", "conversation history", "what have we", "remember talking", "previous conversation"]
        wants_topic_summary = any(keyword in user_message.lower() for keyword in topic_keywords)
        
        # Build complete prompt context for logging
        prompt_parts = []
        prompt_parts.append("=== SYSTEM PROMPT ===")
        prompt_parts.append(Config.SYSTEM_PROMPT)
        prompt_parts.append("")
        
        # Add topic context if user is asking about conversation history
        if wants_topic_summary:
            topics = self.memory.get_topic_statistics()
            if topics:
                prompt_parts.append("=== CONVERSATION TOPICS ===")
                top_topics = list(topics.items())[:5]  # Top 5 topics
                for topic, stats in top_topics:
                    sentiment_emoji = {"positive": "😊", "neutral": "😐", "negative": "😞", "joy": "😄"}
                    emoji = sentiment_emoji.get(stats["dominant_sentiment"], "💬")
                    emotions_str = f" ({', '.join(stats['dominant_emotions'][:2])})" if stats.get("dominant_emotions") else ""
                    prompt_parts.append(f"• {emoji} {topic.title()}: {stats['count']} mentions - {stats['dominant_sentiment']}{emotions_str}")
                prompt_parts.append("")
        
        # Add query enhancement details
        if query_analysis["enhanced_query"] != user_message or query_analysis["entity_values"] or query_analysis["top_keywords"]:
            prompt_parts.append("=== QUERY ENHANCEMENT ===")
            prompt_parts.append(f"Original Query: {user_message}")
            prompt_parts.append(f"Enhanced Query: {query_analysis['enhanced_query']}")
            if query_analysis["entity_values"]:
                prompt_parts.append(f"🎯 Entities: {', '.join(query_analysis['entity_values'])}")
            if query_analysis["top_keywords"]:
                prompt_parts.append(f"🔑 Keywords: {', '.join(query_analysis['top_keywords'][:5])}")
            prompt_parts.append("")
        
        # Add memories if any
        if relevant_memories:
            prompt_parts.append("=== RELEVANT MEMORIES (Hybrid Search) ===")
            for idx, mem in enumerate(relevant_memories, 1):
                # Extract scores from memory dict (not metadata)
                base_score = mem.get('similarity', 0.0)
                boosted_score = mem.get('boosted_score', base_score)
                boost_amount = boosted_score - base_score
                
                # Format score display
                if boost_amount > 0.01:  # Show boost if significant (>0.01)
                    score_str = f"[{base_score:.2f} → {boosted_score:.2f} (+{boost_amount:.2f})]"
                else:
                    score_str = f"[{boosted_score:.2f}]"
                
                content = mem.get('content', '')
                timestamp = mem.get('metadata', {}).get('timestamp', 'unknown')
                time_ago = self._format_time_ago(timestamp)
                preview = content[:100] + "..." if len(content) > 100 else content
                
                prompt_parts.append(f"{idx}. {score_str} {preview} ({time_ago})")
                
                # Show boost breakdown if applicable
                if boost_amount > 0.01:
                    boost_details = []
                    entity_boost = mem.get('entity_boost', 0)
                    keyword_boost = mem.get('keyword_boost', 0)
                    
                    if entity_boost > 0:
                        boost_details.append(f"Entity: +{entity_boost:.2f}")
                    if keyword_boost > 0:
                        boost_details.append(f"Keyword: +{keyword_boost:.2f}")
                    
                    if boost_details:
                        prompt_parts.append(f"   ↳ {', '.join(boost_details)}")
            prompt_parts.append("")
        
        # Add emotional context
        if conversation_history:
            emotional_context = self.brain._format_emotional_context(conversation_history)
            if emotional_context:
                prompt_parts.append(f"=== EMOTIONAL CONTEXT (Analyzing last {len(conversation_history)} messages) ===")
                prompt_parts.append(emotional_context)
                prompt_parts.append("")
            
            # Add emotional adaptation
            emotional_adaptation = self.brain._get_emotional_adaptation(conversation_history)
            if emotional_adaptation:
                prompt_parts.append("=== EMOTIONAL ADAPTATION ===")
                prompt_parts.append(emotional_adaptation)
                prompt_parts.append("")
        
        # Add recent conversation history
        if conversation_history:
            prompt_parts.append("=== RECENT CONVERSATION (Last 10 Messages) ===")
            # Use all 10 messages to match emotional trajectory analysis window
            recent_turns = conversation_history[-10:]
            for conv in recent_turns:
                role = "User" if conv.get('metadata', {}).get('role') == 'user' else "Assistant"
                content = conv.get('content', '')
                if content:
                    # Show full recent messages for context
                    preview = content if len(content) <= 200 else content[:197] + "..."
                    prompt_parts.append(f"{role}: {preview}")
            prompt_parts.append("")
        
        # Log complete system prompt for debugging
        self.logger.log_system_prompt(
            prompt="\n".join(prompt_parts),
            context_type="basic",
            metadata={
                "num_memories": len(relevant_memories),
                "num_history": len(conversation_history),
                "user_message_preview": user_message[:100]
            }
        )
        
        # Show memory context if any
        if relevant_memories:
            self.console.print(f"[dim]💭 Using {len(relevant_memories)} relevant memories[/dim]")
        
        # Generate response with streaming
        self.console.print("\n[AI] ➜ ", style="bold green", end="")
        
        response_text = ""
        error_occurred = False
        try:
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
            
            # Log the conversation turn
            self.logger.log_conversation_turn(
                user_message=user_message,
                bot_response=response_text,
                metadata={
                    "timestamp": timestamp,
                    "num_memories_used": len(relevant_memories),
                    "response_length": len(response_text)
                }
            )


def main():
    """Main entry point."""
    chat = ChatInterface()
    chat.run()


if __name__ == "__main__":
    main()
