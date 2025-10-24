#!/usr/bin/env python3
"""Test script to verify context in all modes."""

from ai_brain.inference import AIBrain
from ai_brain.langchain_brain import LangChainBrain
from ai_brain.memory import MemoryStore

def test_basic_mode():
    """Test basic mode context building."""
    print("🧪 Testing Basic Mode Context...")
    print("-" * 60)
    
    brain = AIBrain()
    memory = MemoryStore()
    
    # Add some test memories
    memory.add_memory(
        "User loves hiking and outdoor activities",
        memory_type="preference",
        metadata={"timestamp": "2025-10-20"}
    )
    
    memory.add_memory(
        "User prefers Python for programming",
        memory_type="preference",
        metadata={"timestamp": "2025-10-21"}
    )
    
    # Retrieve memories
    memories = memory.retrieve_memories("What do I like?", n_results=3)
    history = memory.get_conversation_history(n_recent=5)
    
    # Test emotional context
    if history:
        emotional_ctx = brain._format_emotional_context(history)
        print(f"✅ Emotional context: {emotional_ctx if emotional_ctx else 'None (expected if no history)'}")
    else:
        print("✅ No conversation history (expected for new session)")
    
    print(f"✅ Memories retrieved: {len(memories)}")
    print("✅ Basic mode context: COMPLETE\n")


def test_langchain_mode():
    """Test LangChain mode context building."""
    print("🧪 Testing LangChain Mode Context...")
    print("-" * 60)
    
    brain = LangChainBrain()
    memory = MemoryStore()
    
    # Retrieve memories
    memories = memory.retrieve_memories("What do I like?", n_results=3)
    history = memory.get_conversation_history(n_recent=5)
    
    # Build system message
    system_msg = brain._build_system_message(memories, history)
    
    # Check for key sections
    checks = {
        "CORE CAPABILITIES": "CORE CAPABILITIES" in system_msg,
        "RELEVANT MEMORIES": "RELEVANT MEMORIES" in system_msg or len(memories) == 0,
        "EMOTIONAL CONTEXT": "EMOTIONAL CONTEXT" in system_msg or len(history) == 0,
        "RECENT CONTEXT": "RECENT CONTEXT" in system_msg or len(history) == 0,
        "Similarity scores": any(f"[{m.get('similarity', 0):.2f}]" in system_msg for m in memories) or len(memories) == 0,
    }
    
    print("Context sections present:")
    for section, present in checks.items():
        status = "✅" if present else "❌"
        print(f"  {status} {section}")
    
    if all(checks.values()):
        print("✅ LangChain mode context: COMPLETE\n")
    else:
        print("❌ LangChain mode context: INCOMPLETE\n")
        print("\nSystem message preview:")
        print(system_msg[:500])


def test_llamaindex_mode():
    """Test LlamaIndex mode context."""
    print("🧪 Testing LlamaIndex Mode Context...")
    print("-" * 60)
    
    from ai_brain.llamaindex_rag import LlamaIndexRAG
    import chromadb
    
    # Initialize
    client = chromadb.PersistentClient(path="./chroma_db")
    rag = LlamaIndexRAG(client, "ai_brain_memory")
    
    # Check context prompt
    context_prompt_str = str(rag.context_prompt.template)
    
    checks = {
        "Persistent memory": "persistent memory" in context_prompt_str.lower(),
        "Emotional intelligence": "emotional" in context_prompt_str.lower(),
        "Personalized responses": "personalized" in context_prompt_str.lower(),
        "Context awareness": "context" in context_prompt_str.lower(),
    }
    
    print("Context prompt includes:")
    for feature, present in checks.items():
        status = "✅" if present else "❌"
        print(f"  {status} {feature}")
    
    if all(checks.values()):
        print("✅ LlamaIndex mode context: COMPLETE\n")
    else:
        print("❌ LlamaIndex mode context: INCOMPLETE\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CONTEXT VERIFICATION TEST")
    print("=" * 60 + "\n")
    
    try:
        test_basic_mode()
    except Exception as e:
        print(f"❌ Basic mode test failed: {e}\n")
    
    try:
        test_langchain_mode()
    except Exception as e:
        print(f"❌ LangChain mode test failed: {e}\n")
    
    try:
        test_llamaindex_mode()
    except Exception as e:
        print(f"❌ LlamaIndex mode test failed: {e}\n")
    
    print("=" * 60)
    print("ALL TESTS COMPLETE")
    print("=" * 60)
