#!/usr/bin/env python3
"""Test emotional adaptation system."""

from ai_brain.nlp_analyzer import get_analyzer
from ai_brain.memory import MemoryStore
from ai_brain.langchain_brain import LangChainBrain

# Get analyzer
analyzer = get_analyzer()

# Create test conversation history with different emotional states
test_history = [
    {
        "content": "I'm really frustrated with this error I keep getting",
        "metadata": {
            "role": "user",
            "timestamp": "2025-10-24T10:00:00",
            "user_emotion": "negative",
            "user_emotion_score": 0.85
        }
    },
    {
        "content": "I understand your frustration. Let me help you troubleshoot this.",
        "metadata": {
            "role": "assistant",
            "timestamp": "2025-10-24T10:00:05",
            "bot_emotion": "neutral",
            "bot_emotion_score": 0.75
        }
    },
    {
        "content": "This is the third time I've tried and it still doesn't work!",
        "metadata": {
            "role": "user",
            "timestamp": "2025-10-24T10:01:00",
            "user_emotion": "negative",
            "user_emotion_score": 0.92
        }
    },
    {
        "content": "I can see why this is frustrating. Let's try a different approach together.",
        "metadata": {
            "role": "assistant",
            "timestamp": "2025-10-24T10:01:05",
            "bot_emotion": "neutral",
            "bot_emotion_score": 0.80
        }
    },
]

print("=" * 70)
print("EMOTIONAL ADAPTATION SYSTEM TEST")
print("=" * 70)
print()

print("📊 Test Scenario: User is frustrated with repeated errors")
print()

# Test 1: Basic emotional context
print("1️⃣  BASIC EMOTIONAL CONTEXT:")
print("-" * 70)
context = analyzer.get_emotional_context_summary(test_history, n_recent=5)
print(context)
print()

# Test 2: Detailed adaptation guidance
print("2️⃣  EMOTIONAL ADAPTATION GUIDANCE:")
print("-" * 70)
adaptation = analyzer.get_emotional_adaptation_prompt(test_history, n_recent=5)
print(adaptation)
print()

# Test 3: Real conversation history from database
print("3️⃣  REAL CONVERSATION HISTORY:")
print("-" * 70)
memory = MemoryStore()
real_history = memory.get_conversation_history(n_recent=10)

if real_history:
    print(f"Found {len(real_history)} messages in history")
    
    # Check if any have emotional data
    has_emotion = any("user_emotion" in msg.get("metadata", {}) for msg in real_history)
    if has_emotion:
        print("\n✅ Emotional data found in history")
        real_adaptation = analyzer.get_emotional_adaptation_prompt(real_history, n_recent=5)
        if real_adaptation:
            print("\nEmotional Adaptation for Real History:")
            print(real_adaptation)
        else:
            print("\n⚠️  No adaptation generated (may not have enough emotional data)")
    else:
        print("\n⚠️  No emotional metadata in recent history")
else:
    print("No conversation history found")
print()

# Test 4: Full system prompt with adaptation
print("4️⃣  FULL SYSTEM PROMPT (with emotional adaptation):")
print("-" * 70)
brain = LangChainBrain()
system_prompt = brain._build_system_message([], test_history)

# Show the emotional sections
if "EMOTIONAL ADAPTATION" in system_prompt:
    start = system_prompt.find("=== EMOTIONAL")
    end = system_prompt.find("=== RECENT CONVERSATION")
    if start >= 0:
        emotional_section = system_prompt[start:end if end > 0 else len(system_prompt)]
        print(emotional_section)
        print("\n✅ Emotional adaptation is included in system prompt!")
else:
    print("❌ Emotional adaptation section not found")

print()
print("=" * 70)
print("TEST COMPLETE")
print("=" * 70)
