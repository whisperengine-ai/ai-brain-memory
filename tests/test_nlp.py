#!/usr/bin/env python3
"""
Test NLP analysis features.

This script demonstrates the NLP enrichment capabilities including:
- Entity extraction
- Sentiment analysis
- Keyword extraction
- Intent detection
"""

from ai_brain.nlp_analyzer import NLPAnalyzer


def test_nlp_analysis():
    """Test NLP analyzer with various inputs."""
    print("=" * 80)
    print("🧪 Testing NLP Analyzer")
    print("=" * 80)
    
    # Initialize analyzer
    analyzer = NLPAnalyzer()
    
    # Test cases
    test_texts = [
        "I absolutely love building AI projects with Python! It's amazing how far we've come.",
        "What are the best frameworks for machine learning on Apple Silicon?",
        "My name is Mark and I work at Apple in Cupertino, California.",
        "I'm feeling frustrated with this bug. It's been three days and still no solution.",
        "Can you help me understand how transformers work in natural language processing?"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n{'─' * 80}")
        print(f"Test {i}: {text}")
        print(f"{'─' * 80}")
        
        # Analyze
        analysis = analyzer.analyze_text(text)
        
        # Display results
        print(f"\n📊 Sentiment: {analysis['sentiment']['label'].upper()} "
              f"(confidence: {analysis['sentiment']['score']:.2%})")
        
        print(f"\n🎯 Intent: {analyzer.extract_intent(text)}")
        
        if analysis['entities']:
            print(f"\n🏷️  Entities:")
            for entity_type, entities in analysis['entities'].items():
                print(f"   • {entity_type}: {', '.join(entities)}")
        
        if analysis['keywords']:
            print(f"\n🔑 Keywords: {', '.join(analysis['keywords'][:5])}")
        
        if analysis['topics']:
            print(f"\n💭 Topics: {', '.join(analysis['topics'][:3])}")
        
        # Show metadata that would be stored
        metadata = analyzer.create_metadata_tags(analysis)
        print(f"\n📋 Metadata for Storage:")
        for key, value in list(metadata.items())[:8]:  # Show first 8 fields
            if value:
                print(f"   • {key}: {value}")
    
    print(f"\n{'=' * 80}")
    print("✅ NLP Analysis Test Complete!")
    print(f"{'=' * 80}\n")


if __name__ == "__main__":
    test_nlp_analysis()
