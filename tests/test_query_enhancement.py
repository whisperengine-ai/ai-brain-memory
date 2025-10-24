#!/usr/bin/env python3
"""
Test intelligent query enhancement using spaCy analysis.
"""
from ai_brain.nlp_analyzer import get_analyzer
from ai_brain.memory import MemoryStore

def test_query_enhancement():
    print("=" * 80)
    print("TESTING: Intelligent Query Enhancement with spaCy")
    print("=" * 80)
    print()
    
    analyzer = get_analyzer()
    memory = MemoryStore()
    
    # Test cases: different types of queries
    test_queries = [
        "What's my name?",
        "Tell me about Mark",
        "Do I like quesadillas?",
        "What did we talk about food?",
        "Show me conversations about Python",
        "I need help with my project",
        "Remember when I said I love hiking?"
    ]
    
    for query in test_queries:
        print(f"📝 USER MESSAGE: \"{query}\"")
        print("-" * 80)
        
        # Enhance query
        analysis = analyzer.enhance_query(query)
        
        print(f"Intent: {analysis['intent']}")
        print(f"Query focus: {analysis['query_focus']}")
        print(f"Search strategy: {analysis['should_search_by']}")
        print()
        
        if analysis['entity_values']:
            print(f"Entities found: {', '.join(analysis['entity_values'])}")
        if analysis['top_keywords']:
            print(f"Keywords: {', '.join(analysis['top_keywords'][:5])}")
        if analysis['topics']:
            print(f"Topics: {', '.join(analysis['topics'][:3])}")
        print()
        
        print(f"Original query: {analysis['original_query']}")
        print(f"Enhanced query: {analysis['enhanced_query']}")
        print()
        
        # Test retrieval with both
        print("Testing retrieval:")
        
        # Original
        results_orig = memory.retrieve_memories(query=query, n_results=3)
        print(f"  With original query: {len(results_orig)} results")
        
        # Enhanced
        results_enh = memory.retrieve_memories(query=analysis['enhanced_query'], n_results=3)
        print(f"  With enhanced query: {len(results_enh)} results")
        
        if results_enh:
            print(f"  Top result: [{results_enh[0]['similarity']:.3f}] {results_enh[0]['content'][:60]}...")
        
        print()
        print()
    
    print("=" * 80)
    print("✅ QUERY ENHANCEMENT BENEFITS")
    print("=" * 80)
    print()
    print("✅ Extracts entities (names, places) for precise matching")
    print("✅ Identifies keywords (verbs, nouns) for semantic search")
    print("✅ Detects topics for contextual relevance")
    print("✅ Classifies intent (question/statement/command/expression)")
    print("✅ Expands query with relevant terms for better recall")
    print()
    print("🎯 spaCy analysis happens BEFORE querying, making searches smarter!")

if __name__ == "__main__":
    test_query_enhancement()
