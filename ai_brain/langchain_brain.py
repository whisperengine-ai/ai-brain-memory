"""LangChain-based pipeline for AI Brain with advanced prompt management."""

from typing import List, Dict, Optional
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from .config import Config


class LangChainBrain:
    """
    Advanced AI Brain using LangChain for sophisticated prompt management and conversation.
    """
    
    def __init__(self):
        """Initialize LangChain components."""
        backend = Config.LLM_BACKEND.lower()
        
        if backend == "ollama":
            # Initialize with local Ollama
            # Use dummy API key since Ollama doesn't need authentication
            self.llm = ChatOpenAI(
                base_url=f"{Config.OLLAMA_BASE_URL}/v1",
                api_key="ollama",  # Dummy key for local Ollama
                model=Config.OLLAMA_MODEL,
                temperature=0.7,
            )
            print(f"🔗 LangChain Brain initialized with Ollama: {Config.OLLAMA_MODEL}")
        else:
            # Initialize with OpenRouter (default)
            self.llm = ChatOpenAI(
                base_url=Config.OPENROUTER_BASE_URL,
                api_key=Config.OPENROUTER_API_KEY,
                model=Config.OPENROUTER_MODEL,
                temperature=0.7,
            )
            print(f"🔗 LangChain Brain initialized with OpenRouter: {Config.OPENROUTER_MODEL}")
        
        # Simple message history (in-session)
        self.message_history: List[HumanMessage | AIMessage | SystemMessage] = []
    
    def _format_time_ago(self, timestamp: str) -> str:
        """
        Format timestamp as human-readable 'time ago' string.
        
        Args:
            timestamp: ISO format timestamp string
            
        Returns:
            Human-readable time string like "2 hours ago" or "3 days ago"
        """
        try:
            ts = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
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
    
    def _build_system_message(
        self,
        relevant_memories: Optional[List[Dict]] = None,
        conversation_history: Optional[List[Dict]] = None,
        query_analysis: Optional[Dict] = None
    ) -> str:
        """Build system message with memory context."""
        system_parts = [
            "You are an advanced AI assistant with persistent memory capabilities.",
            "",
            "CORE CAPABILITIES:",
            "- You have access to long-term memory from previous conversations",
            "- You can recall facts, preferences, and context from past interactions",
            "- You maintain conversation continuity across sessions",
            "- You provide thoughtful, contextual, and personalized responses",
            "",
            "INSTRUCTIONS:",
            "1. When relevant memories are provided, use them to enhance your responses",
            "2. Reference past conversations naturally when appropriate",
            "3. If you remember something about the user, mention it contextually",
            "4. Be helpful, accurate, and maintain a consistent personality",
            "5. If you're unsure about a memory, ask for clarification",
            ""
        ]
        
        # Add query enhancement details if available
        if query_analysis:
            if query_analysis.get("entity_values") or query_analysis.get("top_keywords"):
                system_parts.append("=== QUERY ENHANCEMENT ===")
                if query_analysis.get("entity_values"):
                    system_parts.append(f"🎯 Entities: {', '.join(query_analysis['entity_values'])}")
                if query_analysis.get("top_keywords"):
                    system_parts.append(f"🔑 Keywords: {', '.join(query_analysis['top_keywords'][:5])}")
                system_parts.append("")
        
        # Add memory context if available
        if relevant_memories:
            system_parts.append("=== RELEVANT MEMORIES (Hybrid Search) ===")
            for i, mem in enumerate(relevant_memories[:5], 1):  # Limit to top 5
                content = mem.get('content', '')
                
                # Extract scores from memory dict (not metadata)
                base_score = mem.get('similarity', 0.0)
                boosted_score = mem.get('boosted_score', base_score)
                boost_amount = boosted_score - base_score
                
                # Format score display
                if boost_amount > 0.01:  # Show boost if significant
                    score_str = f"[{base_score:.2f} → {boosted_score:.2f} (+{boost_amount:.2f})]"
                else:
                    score_str = f"[{boosted_score:.2f}]"
                
                # Truncate long memories
                if len(content) > 200:
                    content = content[:197] + "..."
                
                system_parts.append(f"{i}. {score_str} {content}")
                
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
                        system_parts.append(f"   ↳ {', '.join(boost_details)}")
            system_parts.append("")
        
        # Add emotional context if available
        if conversation_history:
            emotional_context = self._format_emotional_context(conversation_history)
            if emotional_context:
                system_parts.append(f"=== EMOTIONAL CONTEXT (Analyzing last {len(conversation_history)} messages) ===")
                system_parts.append(emotional_context)
                system_parts.append("")
            
            # Add detailed emotional adaptation guidance
            emotional_adaptation = self._get_emotional_adaptation(conversation_history)
            if emotional_adaptation:
                system_parts.append("=== EMOTIONAL ADAPTATION ===")
                system_parts.append(emotional_adaptation)
                system_parts.append("")
        
        # Add conversation history with intelligent summarization
        if conversation_history:
            # If conversation is long (>20 messages), summarize older messages
            if len(conversation_history) > 20:
                system_parts.append("=== EARLIER CONVERSATION SUMMARY ===")
                # Summarize messages 1 to N-10 (keep last 10 in full)
                old_messages = conversation_history[:-10]
                summary = self._summarize_conversation_chunk(old_messages)
                if summary:
                    system_parts.append(summary)
                system_parts.append("")
            
            # Add recent conversation context (last 10 messages = 5 complete turns)
            system_parts.append("=== RECENT CONVERSATION (Last 5 Turns) ===")
            # Get the most recent 10 messages (5 user/assistant pairs)
            # This matches our emotional trajectory analysis window
            recent_turns = conversation_history[-10:]
            for entry in recent_turns:
                role = "User" if entry.get('metadata', {}).get('role') == 'user' else "Assistant"
                content = entry.get('content', '')
                # Don't truncate - show full recent messages for better context
                if len(content) > 300:
                    content = content[:297] + "..."
                system_parts.append(f"{role}: {content}")
            system_parts.append("")
        
        system_parts.append("Remember: Be natural, helpful, and make the user feel remembered and understood.")
        
        return "\n".join(system_parts)
    
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
        summary_message = (
            "Create a concise summary of the following conversation, "
            "focusing on key topics, decisions, and important information. "
            "Keep it under 100 words.\n\n"
            + "\n".join(conversation_text)
        )
        
        try:
            # Use LangChain to generate summary
            summary_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a conversation summarizer. Be concise and focus on key information."),
                ("human", "{conversation}")
            ])
            
            chain = summary_prompt | self.llm
            response = chain.invoke({"conversation": summary_message})
            
            if hasattr(response, 'content'):
                return response.content
            return str(response)
        except Exception as e:
            print(f"⚠️  Warning: Failed to summarize conversation: {e}")
            # Fallback: return a simple message
            return f"Earlier conversation covered: {len(messages)} messages"
    
    def generate_response(
        self,
        message: str,
        relevant_memories: Optional[List[Dict]] = None,
        conversation_history: Optional[List[Dict]] = None,
        query_analysis: Optional[Dict] = None
    ) -> str:
        """
        Generate a response using LangChain with memory context.
        
        Args:
            message: User's input message
            relevant_memories: List of relevant memories from vector DB
            conversation_history: Recent conversation history
            query_analysis: Query enhancement details (entities, keywords)
            
        Returns:
            Generated response text
        """
        # Build the system message with context
        system_content = self._build_system_message(relevant_memories, conversation_history, query_analysis)
        
        # Create message sequence with recent history from DB
        messages = [SystemMessage(content=system_content)]
        
        # Add recent conversation history from database (last 5 turns = 10 messages)
        # This matches our emotional trajectory analysis window
        if conversation_history:
            recent_turns = conversation_history[-10:]
            for entry in recent_turns:
                role = entry.get('metadata', {}).get('role', 'user')
                content = entry.get('content', '')
                if role == 'user':
                    messages.append(HumanMessage(content=content))
                else:
                    messages.append(AIMessage(content=content))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        try:
            # Get response from LLM
            response = self.llm.invoke(messages)
            response_text = response.content
            
            # Store in session history (for continuity within this session)
            self.message_history.append(HumanMessage(content=message))
            self.message_history.append(AIMessage(content=response_text))
            if len(self.message_history) > 20:  # Keep last 10 exchanges
                self.message_history = self.message_history[-20:]
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def generate_response_streaming(
        self,
        message: str,
        relevant_memories: Optional[List[Dict]] = None,
        conversation_history: Optional[List[Dict]] = None,
        query_analysis: Optional[Dict] = None
    ):
        """
        Generate a streaming response using LangChain with memory context.
        
        Args:
            message: User's input message
            relevant_memories: List of relevant memories from vector DB
            conversation_history: Recent conversation history
            query_analysis: Query enhancement details (entities, keywords)
            
        Yields:
            Response text chunks
        """
        # Build the system message with context
        system_content = self._build_system_message(relevant_memories, conversation_history, query_analysis)
        
        # Create message sequence with recent history from DB
        messages = [SystemMessage(content=system_content)]
        
        # Add recent conversation history from database (last 5 turns = 10 messages)
        # This matches our emotional trajectory analysis window
        if conversation_history:
            recent_turns = conversation_history[-10:]
            for entry in recent_turns:
                role = entry.get('metadata', {}).get('role', 'user')
                content = entry.get('content', '')
                if role == 'user':
                    messages.append(HumanMessage(content=content))
                else:
                    messages.append(AIMessage(content=content))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        full_response = []
        try:
            # Stream response from LLM
            for chunk in self.llm.stream(messages):
                if hasattr(chunk, 'content') and chunk.content:
                    full_response.append(chunk.content)
                    yield chunk.content
            
            # Store in session history after streaming completes
            response_text = "".join(full_response)
            self.message_history.append(HumanMessage(content=message))
            self.message_history.append(AIMessage(content=response_text))
            if len(self.message_history) > 20:
                self.message_history = self.message_history[-20:]
                
        except Exception as e:
            error_msg = f"Error generating streaming response: {str(e)}"
            print(f"❌ {error_msg}")
            yield error_msg
    
    def format_memory_for_display(self, memories: List[Dict]) -> str:
        """Format memories for display to the user."""
        if not memories:
            return "No relevant memories found."
        
        lines = ["📚 Relevant Memories:"]
        for i, mem in enumerate(memories[:5], 1):
            content = mem.get('content', 'N/A')
            if len(content) > 100:
                content = content[:97] + "..."
            
            # Get timestamp if available
            timestamp = mem.get('metadata', {}).get('timestamp', 'Unknown time')
            if timestamp != 'Unknown time':
                time_ago = self._format_time_ago(timestamp)
            else:
                time_ago = "Unknown time"
            
            lines.append(f"  {i}. [{time_ago}] {content}")
        
        return "\n".join(lines)
    
    def clear_session_history(self):
        """Clear the in-session conversation history."""
        self.message_history = []
        print("🧹 Session history cleared")
    
    def get_session_history(self) -> List[Dict]:
        """Get the current session history."""
        return [
            {
                "role": "user" if isinstance(msg, HumanMessage) else "assistant",
                "content": msg.content
            }
            for msg in self.message_history
        ]
