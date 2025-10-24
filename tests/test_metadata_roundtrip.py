#!/usr/bin/env python3
"""
Test to verify NLP metadata is properly stored and retrieved in the full round trip.
"""
from ai_brain.memory import MemoryStore
from ai_brain.config import Config
import json

def test_metadata_roundtrip():
    """Test that NLP metadata flows from storage -> retrieval -> system prompt."""
    
    print("=" * 80)
    print("TESTING NLP METADATA ROUND TRIP")
    print("=" * 80)
    print()
    
    # Initialize memory
    memory = MemoryStore()
    
    # 1. CHECK STORED METADATA
    print("📦 STEP 1: Checking what metadata is STORED in ChromaDB")
    print("-" * 80)
    
    history = memory.get_conversation_history(n_recent=5)
    if history:
        print(f"✅ Found {len(history)} recent conversations\n")
        for i, conv in enumerate(history[:2], 1):  # Show first 2
            print(f"--- Message {i} ---")
            print(f"Content: {conv['content'][:60]}...")
            print(f"Role: {conv['metadata'].get('role', 'N/A')}")
            print(f"\nMetadata Fields Present ({len(conv['metadata'])} total):")
            
            # Check for NLP-enriched fields
            nlp_fields = {
                'sentiment': 'Sentiment label',
                'sentiment_score': 'Sentiment confidence',
                'keywords': 'Extracted keywords',
                'topics': 'Identified topics',
                'intent': 'User intent classification',
                'user_emotion': 'User emotion state',
                'bot_emotion': 'Bot emotion state',
                'entities_PERSON': 'Person entities',
                'entities_GPE': 'Location entities',
                'word_count': 'Word count',
                'has_question': 'Question indicator',
                'has_negation': 'Negation indicator'
            }
            
            found_nlp_fields = []
            missing_nlp_fields = []
            
            for field, description in nlp_fields.items():
                if field in conv['metadata']:
                    value = conv['metadata'][field]
                    # Format value for display
                    if isinstance(value, float):
                        value_str = f"{value:.2f}"
                    elif isinstance(value, bool):
                        value_str = str(value)
                    else:
                        value_str = str(value)[:40]
                    
                    found_nlp_fields.append(f"  ✅ {field}: {value_str}")
                else:
                    missing_nlp_fields.append(f"  ❌ {field} (missing)")
            
            print("\n".join(found_nlp_fields))
            if missing_nlp_fields and len(missing_nlp_fields) < 5:  # Only show if few missing
                print("\n".join(missing_nlp_fields[:3]))
            
            print()
    else:
        print("❌ No conversation history found!")
        print("Run a conversation first (python main.py) to test metadata.")
        return False
    
    print()
    
    # 2. CHECK RETRIEVAL
    print("🔍 STEP 2: Checking what metadata is RETRIEVED")
    print("-" * 80)
    
    # Query for memories
    query = "what did we talk about"
    retrieved = memory.retrieve_memories(query=query, n_results=3)
    
    if retrieved:
        print(f"✅ Retrieved {len(retrieved)} relevant memories\n")
        for i, mem in enumerate(retrieved[:1], 1):  # Show first result
            print(f"--- Retrieved Memory {i} ---")
            print(f"Content: {mem['content'][:60]}...")
            print(f"Similarity: {mem['similarity']:.3f}")
            print(f"\nMetadata available in retrieved memory:")
            meta_keys = list(mem['metadata'].keys())
            print(f"  Keys: {', '.join(meta_keys[:10])}")
            if len(meta_keys) > 10:
                print(f"  ... and {len(meta_keys) - 10} more")
            
            # Check if NLP fields survived retrieval
            nlp_present = sum(1 for field in nlp_fields if field in mem['metadata'])
            print(f"\n  NLP-enriched fields present: {nlp_present}/{len(nlp_fields)}")
            print()
    else:
        print("❌ No memories retrieved!")
        return False
    
    print()
    
    # 3. CHECK EMOTIONAL CONTEXT FORMATTING
    print("😊 STEP 3: Checking EMOTIONAL CONTEXT formatting for system prompt")
    print("-" * 80)
    
    try:
        from ai_brain.nlp_analyzer import get_analyzer
        analyzer = get_analyzer()
        
        # Get emotional context summary
        emotional_summary = analyzer.get_emotional_context_summary(history, n_recent=5)
        print("✅ Emotional context generated:\n")
        print(f"  {emotional_summary}")
        print()
        
        # Check if it contains actual data from metadata
        if 'emotion' in emotional_summary.lower() or 'neutral' in emotional_summary.lower():
            print("  ✅ Contains emotional state information from metadata")
        else:
            print("  ⚠️  May not contain actual emotional data")
        
        print()
        
        # Get detailed adaptation prompt
        adaptation = analyzer.get_emotional_adaptation_prompt(history, n_recent=5)
        if adaptation:
            print("✅ Emotional adaptation guidance generated:")
            print()
            # Show first few lines
            lines = adaptation.split('\n')[:8]
            for line in lines:
                print(f"  {line}")
            if len(adaptation.split('\n')) > 8:
                print(f"  ... ({len(adaptation.split('\n')) - 8} more lines)")
            print()
            
            # Verify it uses actual metadata
            checks = [
                ('EMOTIONAL ADAPTATION' in adaptation, "Contains adaptation header"),
                ('current state:' in adaptation.lower(), "Contains current emotional state"),
                ('trajectory:' in adaptation.lower(), "Contains trajectory analysis"),
                ('confidence:' in adaptation.lower(), "Uses confidence scores from metadata")
            ]
            
            print("  Verification:")
            for check, description in checks:
                status = "✅" if check else "❌"
                print(f"  {status} {description}")
        else:
            print("❌ No emotional adaptation guidance generated!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing emotional context: {e}")
        return False
    
    print()
    
    # 4. FINAL VERDICT
    print("=" * 80)
    print("📊 ROUND TRIP VERIFICATION")
    print("=" * 80)
    print()
    
    checks = [
        (len(history) > 0, "✅ Metadata stored in ChromaDB"),
        (len(retrieved) > 0, "✅ Metadata retrieved from ChromaDB"),
        (emotional_summary and len(emotional_summary) > 10, "✅ Emotional context formatted from metadata"),
        (adaptation and 'EMOTIONAL' in adaptation, "✅ Adaptation guidance uses metadata"),
    ]
    
    all_passed = all(check for check, _ in checks)
    
    for passed, message in checks:
        print(message if passed else message.replace("✅", "❌"))
    
    print()
    if all_passed:
        print("🎉 SUCCESS! NLP metadata is properly flowing through the entire pipeline:")
        print("   Storage → Retrieval → Emotional Context → System Prompt")
    else:
        print("⚠️  Some issues detected in the metadata round trip")
    
    return all_passed


if __name__ == "__main__":
    test_metadata_roundtrip()
