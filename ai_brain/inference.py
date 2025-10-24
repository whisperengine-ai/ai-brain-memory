"""AI inference using OpenRouter API or local Ollama."""

from openai import OpenAI
from typing import List, Dict, Generator
from datetime import datetime
from .config import Config


class AIBrain:
    """AI Brain for inference using OpenRouter or Ollama."""
    
    def __init__(self):
        """Initialize LLM client based on configuration."""
        backend = Config.LLM_BACKEND.lower()
        
        if backend == "ollama":
            # Use local Ollama
            self.client = OpenAI(
                base_url=f"{Config.OLLAMA_BASE_URL}/v1",
                api_key="ollama",  # Ollama doesn't require a real key
            )
            self.model = Config.OLLAMA_MODEL
            print(f"🤖 AI Brain initialized with Ollama model: {self.model}")
            print(f"   Base URL: {Config.OLLAMA_BASE_URL}")
        else:
            # Use OpenRouter (default)
            self.client = OpenAI(
                base_url=Config.OPENROUTER_BASE_URL,
                api_key=Config.OPENROUTER_API_KEY,
            )
            self.model = Config.OPENROUTER_MODEL
            print(f"🤖 AI Brain initialized with OpenRouter model: {self.model}")
    
    def generate_response(
        self,
        message: str,
        relevant_memories: List[Dict] = None,
        conversation_history: List[Dict] = None,
        stream: bool = True
    ) -> Generator[str, None, None] | str:
        """
        Generate a response using OpenRouter API.
        
        Args:
            message: User message
            relevant_memories: Relevant memories from vector store
            conversation_history: Recent conversation history
            stream: Whether to stream the response
            
        Returns:
            Generated response (streamed or complete)
        """
        # Build messages
        messages = [{"role": "system", "content": Config.SYSTEM_PROMPT}]
        
        # Add relevant memories as context
        if relevant_memories:
            memory_context = self._format_memories(relevant_memories)
            messages.append({
                "role": "system",
                "content": f"Relevant memories:\n{memory_context}"
            })
        
        # Add emotional context if available
        if conversation_history:
            emotional_context = self._format_emotional_context(conversation_history)
            if emotional_context:
                messages.append({
                    "role": "system",
                    "content": f"EMOTIONAL CONTEXT:\n{emotional_context}"
                })
            
            # Add detailed emotional adaptation guidance
            emotional_adaptation = self._get_emotional_adaptation(conversation_history)
            if emotional_adaptation:
                messages.append({
                    "role": "system",
                    "content": emotional_adaptation
                })
        
        # Add conversation history with intelligent summarization
        if conversation_history:
            # If conversation is long (>20 messages), summarize older messages
            if len(conversation_history) > 20:
                # Summarize messages 1 to N-10 (keep last 10 in full)
                old_messages = conversation_history[:-10]
                summary = self._summarize_conversation_chunk(old_messages)
                if summary:
                    messages.append({
                        "role": "system",
                        "content": f"=== EARLIER CONVERSATION SUMMARY ===\n{summary}"
                    })
            
            # Add recent conversation history (last 10 messages = 5 user/assistant turns)
            # Get the most recent 10 messages (5 complete turns)
            # This matches our emotional trajectory analysis window
            recent_turns = conversation_history[-10:]
            for conv in recent_turns:
                content = conv.get("content", "")
                role = conv.get("metadata", {}).get("role", "user")
                if content:
                    messages.append({"role": role, "content": content})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Generate response
        try:
            if stream:
                return self._stream_response(messages)
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                )
                return response.choices[0].message.content
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            print(f"❌ {error_msg}")
            return error_msg if not stream else iter([error_msg])
    
    def _stream_response(self, messages: List[Dict]) -> Generator[str, None, None]:
        """Stream response from OpenRouter."""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n\n❌ Error: {e}"
    
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
    
    def _format_memories(self, memories: List[Dict]) -> str:
        """Format memories for context with human-readable timestamps."""
        if not memories:
            return "No relevant memories found."
        
        formatted = []
        for i, mem in enumerate(memories, 1):
            content = mem.get("content", "")
            similarity = mem.get("similarity", 0)
            timestamp = mem.get("metadata", {}).get("timestamp", "unknown")
            time_ago = self._format_time_ago(timestamp)
            formatted.append(f"{i}. [{similarity:.2f}] {content} ({time_ago})")
        
        return "\n".join(formatted)
    
    def _format_emotional_context(self, conversation_history: List[Dict]) -> str:
        """Format emotional context from conversation history."""
        try:
            from .nlp_analyzer import get_analyzer
            analyzer = get_analyzer()
            return analyzer.get_emotional_context_summary(conversation_history)
        except Exception:
            return ""
    
    def _get_emotional_adaptation(self, conversation_history: List[Dict]) -> str:
        """Get detailed emotional adaptation guidance for the system prompt."""
        try:
            from .nlp_analyzer import get_analyzer
            analyzer = get_analyzer()
            return analyzer.get_emotional_adaptation_prompt(conversation_history, n_recent=5)
        except Exception:
            return ""
    
    def _summarize_conversation_chunk(self, messages: List[Dict]) -> str:
        """
        Summarize a chunk of older conversation messages.
        
        Args:
            messages: List of conversation messages to summarize
            
        Returns:
            A concise summary of the conversation chunk
        """
        if not messages:
            return ""
        
        # Build conversation text for summarization
        conversation_text = []
        for msg in messages:
            role = msg.get('metadata', {}).get('role', 'user')
            content = msg.get('content', '')
            if content:
                role_label = "User" if role == "user" else "Assistant"
                conversation_text.append(f"{role_label}: {content}")
        
        if not conversation_text:
            return ""
        
        # Create summarization prompt
        summary_prompt = [
            {
                "role": "system",
                "content": "You are a conversation summarizer. Create a concise summary of the following conversation, focusing on key topics, decisions, and important information. Keep it under 100 words."
            },
            {
                "role": "user",
                "content": "\n".join(conversation_text)
            }
        ]
        
        try:
            # Use OpenRouter to generate summary (non-streaming)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=summary_prompt,
                temperature=0.3,  # Lower temperature for more focused summaries
                max_tokens=150,  # Limit summary length
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️  Warning: Failed to summarize conversation: {e}")
            # Fallback: return a simple concatenation
            return f"Earlier conversation covered: {len(messages)} messages"
