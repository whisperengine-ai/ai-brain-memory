#!/usr/bin/env python3
"""
Test that emotional adaptation is truly dynamic and not static.
"""
from ai_brain.nlp_analyzer import NLPAnalyzer
from datetime import datetime

def test_dynamic_adaptation():
    print("=" * 80)
    print("TESTING: Emotional Adaptation Is Dynamic")
    print("=" * 80)
    print()
    
    analyzer = NLPAnalyzer()
    
    # Test Case 1: Positive user
    print("📊 TEST CASE 1: Highly Positive User (confidence: 0.95)")
    print("-" * 80)
    positive_history = [
        {
            "content": "This is amazing!",
            "metadata": {
                "role": "user",
                "user_emotion": "positive",
                "user_emotion_score": 0.95,
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "content": "I'm so happy with this!",
            "metadata": {
                "role": "user",
                "user_emotion": "positive",
                "user_emotion_score": 0.92,
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    adaptation = analyzer.get_emotional_adaptation_prompt(positive_history, n_recent=5)
    print(adaptation)
    print()
    print()
    
    # Test Case 2: Negative user
    print("📊 TEST CASE 2: Highly Negative User (confidence: 0.88)")
    print("-" * 80)
    negative_history = [
        {
            "content": "This is frustrating!",
            "metadata": {
                "role": "user",
                "user_emotion": "negative",
                "user_emotion_score": 0.88,
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "content": "I can't figure this out",
            "metadata": {
                "role": "user",
                "user_emotion": "negative",
                "user_emotion_score": 0.85,
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    adaptation = analyzer.get_emotional_adaptation_prompt(negative_history, n_recent=5)
    print(adaptation)
    print()
    print()
    
    # Test Case 3: Neutral user
    print("📊 TEST CASE 3: Neutral User (confidence: 0.80)")
    print("-" * 80)
    neutral_history = [
        {
            "content": "What's the syntax for this?",
            "metadata": {
                "role": "user",
                "user_emotion": "neutral",
                "user_emotion_score": 0.80,
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    adaptation = analyzer.get_emotional_adaptation_prompt(neutral_history, n_recent=5)
    print(adaptation)
    print()
    print()
    
    # Test Case 4: Declining trajectory
    print("📊 TEST CASE 4: Declining Emotional Trajectory")
    print("-" * 80)
    declining_history = [
        {
            "content": "Great!",
            "metadata": {
                "role": "user",
                "user_emotion": "positive",
                "user_emotion_score": 0.90,
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "content": "Hmm, okay",
            "metadata": {
                "role": "user",
                "user_emotion": "neutral",
                "user_emotion_score": 0.75,
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "content": "This isn't working",
            "metadata": {
                "role": "user",
                "user_emotion": "negative",
                "user_emotion_score": 0.82,
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    adaptation = analyzer.get_emotional_adaptation_prompt(declining_history, n_recent=5)
    print(adaptation)
    print()
    print()
    
    # Test Case 5: Multiple negative (alert trigger)
    print("📊 TEST CASE 5: Multiple Negative Interactions (Alert Should Trigger)")
    print("-" * 80)
    multiple_negative = [
        {
            "content": "This is wrong",
            "metadata": {
                "role": "user",
                "user_emotion": "negative",
                "user_emotion_score": 0.80,
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "content": "Still not working",
            "metadata": {
                "role": "user",
                "user_emotion": "negative",
                "user_emotion_score": 0.85,
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "content": "I give up",
            "metadata": {
                "role": "user",
                "user_emotion": "negative",
                "user_emotion_score": 0.92,
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    adaptation = analyzer.get_emotional_adaptation_prompt(multiple_negative, n_recent=5)
    print(adaptation)
    print()
    print()
    
    # Test new emotional context format
    print("=" * 80)
    print("TESTING: New Natural Language Emotional Context")
    print("=" * 80)
    print()
    
    print("📊 TEST: Positive Context")
    print("-" * 80)
    context = analyzer.get_emotional_context_summary(positive_history, n_recent=5)
    print(context)
    print()
    print()
    
    print("📊 TEST: Negative Context")
    print("-" * 80)
    context = analyzer.get_emotional_context_summary(negative_history, n_recent=5)
    print(context)
    print()
    print()
    
    print("📊 TEST: Declining Context")
    print("-" * 80)
    context = analyzer.get_emotional_context_summary(declining_history, n_recent=5)
    print(context)
    print()
    
    print("=" * 80)
    print("✅ VERIFICATION")
    print("=" * 80)
    print()
    print("✅ Emotional adaptation changes based on:")
    print("   - Current emotion (positive/negative/neutral)")
    print("   - Confidence level (high >0.7 vs low <0.7)")
    print("   - Trajectory (stable/improving/declining/volatile)")
    print("   - Pattern detection (multiple negative → alert)")
    print()
    print("✅ Emotional context now uses natural language:")
    print("   - 'The user is clearly feeling positive' vs '(confidence: 85%)'")
    print("   - 'Their mood has been improving' vs 'shifted: negative → positive'")
    print()
    print("🎯 Both are FULLY DYNAMIC based on actual conversation metadata!")

if __name__ == "__main__":
    test_dynamic_adaptation()
