#!/usr/bin/env python3
"""Test the logging functionality."""

from ai_brain.logger import ConversationLogger

def test_logger():
    """Test conversation and prompt logging."""
    print("🧪 Testing ConversationLogger...")
    
    # Create logger
    logger = ConversationLogger()
    print(f"✅ Logger created with session ID: {logger.get_session_id()}")
    
    # Test conversation logging
    print("\n📝 Testing conversation logging...")
    logger.log_conversation_turn(
        user_message="Hello, how are you?",
        bot_response="I'm doing well, thank you! How can I help you today?",
        metadata={
            "mode": "test",
            "num_memories_used": 3,
            "response_length": 56
        }
    )
    print("✅ Conversation turn logged")
    
    logger.log_conversation_turn(
        user_message="What's the weather like?",
        bot_response="I don't have access to real-time weather data, but I'd be happy to discuss weather patterns!",
        metadata={
            "mode": "test",
            "num_memories_used": 1,
            "response_length": 94
        }
    )
    print("✅ Second conversation turn logged")
    
    # Test system prompt logging
    print("\n📝 Testing system prompt logging...")
    test_prompt = """You are a helpful AI assistant with memory.

CONTEXT:
- User has asked about weather
- Previous conversation: 2 turns
- Emotional state: neutral

INSTRUCTIONS:
1. Be helpful and accurate
2. Acknowledge limitations
3. Provide context when relevant

Remember to maintain a friendly tone."""
    
    logger.log_system_prompt(
        prompt=test_prompt,
        context_type="test",
        metadata={
            "num_memories": 3,
            "num_history": 2,
            "user_message_preview": "What's the weather like?"
        }
    )
    print("✅ System prompt logged")
    
    # Test session summary
    print("\n📝 Testing session summary...")
    logger.save_session_summary({
        "test_mode": True,
        "total_prompts_logged": 1,
        "notes": "Testing logging functionality"
    })
    print("✅ Session summary saved")
    
    # Show results
    print(f"\n📊 Session Results:")
    print(f"   Session ID: {logger.get_session_id()}")
    print(f"   Total turns: {len(logger.get_conversation_log())}")
    print(f"   Logs directory: logs/")
    print(f"   - conversations/conversation_{logger.get_session_id()}.json")
    print(f"   - conversations/summary_{logger.get_session_id()}.json")
    print(f"   - prompts/prompts_{logger.get_session_id()}.log")
    
    print("\n✅ All logging tests passed!")
    print("\n💡 Check the 'logs/' directory to see the generated files")

if __name__ == "__main__":
    test_logger()
