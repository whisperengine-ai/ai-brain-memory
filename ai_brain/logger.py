"""Logging utilities for conversation and system prompt tracking."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ConversationLogger:
    """Log conversations and system prompts for debugging and analysis."""
    
    def __init__(self, logs_dir: str = "logs"):
        """
        Initialize the logger.
        
        Args:
            logs_dir: Directory to store log files
        """
        self.logs_dir = Path(logs_dir)
        self.conversations_dir = self.logs_dir / "conversations"
        self.prompts_dir = self.logs_dir / "prompts"
        
        # Create directories
        self.conversations_dir.mkdir(parents=True, exist_ok=True)
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        
        # Current session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.conversation_log: List[Dict[str, Any]] = []
        
    def log_conversation_turn(
        self,
        user_message: str,
        bot_response: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a single conversation turn.
        
        Args:
            user_message: User's input message
            bot_response: Bot's response
            metadata: Additional metadata (memories, emotions, etc.)
        """
        turn = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "bot": bot_response,
            "metadata": metadata or {}
        }
        
        self.conversation_log.append(turn)
        
        # Append to JSON file
        conversation_file = self.conversations_dir / f"conversation_{self.session_id}.json"
        
        try:
            # Read existing data
            if conversation_file.exists():
                with open(conversation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {
                    "session_id": self.session_id,
                    "started_at": turn["timestamp"],
                    "turns": []
                }
            
            # Append new turn
            data["turns"].append(turn)
            data["last_updated"] = turn["timestamp"]
            
            # Write back
            with open(conversation_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️  Failed to log conversation turn: {e}")
    
    def log_system_prompt(
        self,
        prompt: str,
        context_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Log a system prompt for debugging.
        
        Args:
            prompt: The full system prompt
            context_type: Type of context (e.g., 'langchain', 'basic', 'rag')
            metadata: Additional metadata about the prompt
        """
        timestamp = datetime.now()
        prompt_file = self.prompts_dir / f"prompts_{self.session_id}.log"
        
        try:
            with open(prompt_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*80}\n")
                f.write(f"Timestamp: {timestamp.isoformat()}\n")
                f.write(f"Context Type: {context_type}\n")
                
                if metadata:
                    f.write(f"Metadata: {json.dumps(metadata, indent=2)}\n")
                
                f.write(f"{'-'*80}\n")
                f.write("SYSTEM PROMPT:\n")
                f.write(f"{'-'*80}\n")
                f.write(prompt)
                f.write(f"\n{'='*80}\n\n")
                
        except Exception as e:
            print(f"⚠️  Failed to log system prompt: {e}")
    
    def save_session_summary(self, summary_data: Optional[Dict[str, Any]] = None):
        """
        Save a summary of the current session.
        
        Args:
            summary_data: Additional summary information
        """
        summary_file = self.conversations_dir / f"summary_{self.session_id}.json"
        
        try:
            summary = {
                "session_id": self.session_id,
                "total_turns": len(self.conversation_log),
                "started_at": self.conversation_log[0]["timestamp"] if self.conversation_log else None,
                "ended_at": datetime.now().isoformat(),
                "custom_data": summary_data or {}
            }
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️  Failed to save session summary: {e}")
    
    def get_session_id(self) -> str:
        """Get the current session ID."""
        return self.session_id
    
    def get_conversation_log(self) -> List[Dict[str, Any]]:
        """Get the current conversation log."""
        return self.conversation_log.copy()


# Global logger instance (lazy initialization)
_logger: Optional[ConversationLogger] = None


def get_logger() -> ConversationLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = ConversationLogger()
    return _logger


def reset_logger():
    """Reset the global logger (useful for new sessions)."""
    global _logger
    _logger = None
