#!/usr/bin/env python3
"""
Test to show what's ACTUALLY sent to the LLM vs what's logged.
"""
from ai_brain.memory import MemoryStore
from ai_brain.inference import AIBrain
from ai_brain.config import Config

def test_actual_messages():
    print("=" * 80)
    print("TESTING: What's ACTUALLY sent to LLM")
    print("=" * 80)
    print()
    
    # Initialize
    memory = MemoryStore()
    brain = AIBrain()
    
    # Get some data
    relevant_memories = memory.retrieve_memories("test", n_results=2)
    conversation_history = memory.get_conversation_history(n_recent=6)
    
    print(f"📊 Available Context:")
    print(f"  - Relevant memories: {len(relevant_memories)}")
    print(f"  - Conversation history: {len(conversation_history)}")
    print()
    
    # Manually build what the brain.generate_response() builds
    print("=" * 80)
    print("🔍 WHAT'S ACTUALLY SENT TO LLM (messages array):")
    print("=" * 80)
    print()
    
    messages = [{"role": "system", "content": Config.SYSTEM_PROMPT}]
    
    # Add relevant memories
    if relevant_memories:
        memory_context = brain._format_memories(relevant_memories)
        messages.append({
            "role": "system",
            "content": f"Relevant memories:\n{memory_context}"
        })
        print("✅ [1] Base system prompt")
        print("✅ [2] Relevant memories context")
        print(f"     Content preview: {memory_context[:80]}...")
        print()
    else:
        print("✅ [1] Base system prompt")
        print("⚠️  [2] No relevant memories (below threshold)")
        print()
    
    # Add emotional context
    if conversation_history:
        emotional_context = brain._format_emotional_context(conversation_history)
        if emotional_context:
            messages.append({
                "role": "system",
                "content": f"EMOTIONAL CONTEXT:\n{emotional_context}"
            })
            print(f"✅ [3] Emotional context")
            print(f"     Content: {emotional_context}")
            print()
        
        # Add emotional adaptation
        emotional_adaptation = brain._get_emotional_adaptation(conversation_history)
        if emotional_adaptation:
            messages.append({
                "role": "system",
                "content": emotional_adaptation
            })
            print(f"✅ [4] Emotional adaptation guidance")
            lines = emotional_adaptation.split('\n')
            print(f"     Preview: {lines[0]}")
            print(f"     ... ({len(lines)} total lines)")
            print()
    
    # Add recent conversation history
    if conversation_history:
        recent_turns = conversation_history[-6:]
        count = 0
        for conv in recent_turns:
            content = conv.get("content", "")
            role = conv.get("metadata", {}).get("role", "user")
            if content:
                messages.append({"role": role, "content": content})
                count += 1
        
        print(f"✅ [5-{4+count}] Recent conversation history ({count} messages)")
        for i, conv in enumerate(recent_turns[:2], 1):
            role = conv.get("metadata", {}).get("role", "user")
            content_preview = conv.get("content", "")[:50]
            print(f"     {role}: {content_preview}...")
        if count > 2:
            print(f"     ... and {count - 2} more messages")
        print()
    
    # Add current message
    current_msg = "What do you remember about me?"
    messages.append({"role": "user", "content": current_msg})
    print(f"✅ [{len(messages)}] Current user message")
    print(f"     Content: {current_msg}")
    print()
    
    print("=" * 80)
    print(f"📤 TOTAL MESSAGES SENT TO LLM: {len(messages)}")
    print("=" * 80)
    print()
    
    # Show what's logged
    print()
    print("=" * 80)
    print("📝 WHAT'S CURRENTLY LOGGED (from cli.py line 174-177):")
    print("=" * 80)
    print()
    
    prompt_context = brain._format_emotional_context(conversation_history)
    print("Only this emotional context string:")
    print(prompt_context)
    print()
    
    print()
    print("❌ PROBLEM IDENTIFIED:")
    print("-" * 80)
    print("The logger only receives the emotional_context string,")
    print("but the LLM receives:")
    print("  1. System prompt")
    print("  2. Relevant memories")
    print("  3. Emotional context")
    print("  4. Emotional adaptation guidance")
    print("  5-N. Recent conversation history (actual messages)")
    print("  N+1. Current user message")
    print()
    print("The logs are INCOMPLETE - they don't show the full context!")

if __name__ == "__main__":
    test_actual_messages()
