#!/usr/bin/env python3
"""Test emotional tracking in conversation."""

import sys
from ai_brain.memory import MemoryStore
from ai_brain.nlp_analyzer import get_analyzer

def test_emotional_tracking():
    """Test storing and retrieving emotional context."""
    print("🧪 Testing Emotional Tracking")
    print("=" * 50)
    
    # Initialize memory and analyzer
    memory = MemoryStore()
    analyzer = get_analyzer()
    
    # Simulate a conversation with varying emotions
    conversations = [
        ("I'm so excited about this new AI project!", "user"),
        ("That's wonderful! I'm here to help you build it.", "assistant"),
        ("Actually, I'm worried it might be too complex.", "user"),
        ("Don't worry, we'll break it down into manageable steps.", "assistant"),
        ("This bug is really frustrating me!", "user"),
        ("I understand your frustration. Let's debug it together.", "assistant"),
    ]
    
    print("\n📝 Storing conversation with emotional analysis...")
    for content, role in conversations:
        enriched = analyzer.enrich_conversation_entry(content, role)
        
        # Show what was detected
        emotion_key = "user_emotion" if role == "user" else "bot_emotion"
        score_key = "user_emotion_score" if role == "user" else "bot_emotion_score"
        
        if emotion_key in enriched:
            emotion = enriched[emotion_key]
            score = enriched.get(score_key, 0)
            print(f"  [{role}] {emotion.upper()} ({score:.1%}): {content[:50]}...")
        
        # Store in memory
        memory.add_memory(
            content=content,
            metadata=enriched,
            enable_nlp=False  # Already enriched
        )
    
    print("\n🔍 Retrieving conversation history...")
    history = memory.get_conversation_history(n_recent=6)
    print(f"Retrieved {len(history)} messages")
    
    print("\n😊 Generating emotional context summary...")
    emotional_summary = analyzer.get_emotional_context_summary(history)
    print(emotional_summary)
    
    print("\n🎯 Testing tone adjustment recommendations...")
    if history:
        latest = history[0]  # Most recent message
        meta = latest.get("metadata", {})
        if "user_emotion" in meta:
            user_emotion = meta["user_emotion"]
            user_score = meta.get("user_emotion_score", 0.5)
            should_adjust, suggestion = analyzer.should_adjust_tone(user_emotion, user_score)
            if should_adjust:
                print(f"✓ Tone adjustment suggested: {suggestion}")
            else:
                print(f"✓ No tone adjustment needed: {suggestion}")
    
    print("\n✅ Emotional tracking test complete!")

if __name__ == "__main__":
    try:
        test_emotional_tracking()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
