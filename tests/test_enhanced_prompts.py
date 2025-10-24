#!/usr/bin/env python3
"""
Test Enhanced Prompt Generation with 11-Emotion System
Shows how the new emotional context and trajectory sections will appear in logs.
"""

import sys
from ai_brain.nlp_analyzer import NLPAnalyzer

def test_emotional_prompts():
    """Test the enhanced emotional prompt generation."""
    
    analyzer = NLPAnalyzer()
    
    print("=" * 80)
    print("🧪 TESTING ENHANCED EMOTIONAL PROMPTS")
    print("=" * 80)
    
    # Test 1: Simple single emotion
    print("\n" + "=" * 80)
    print("TEST 1: Single Emotion (Joy)")
    print("=" * 80)
    
    test_messages_1 = [
        {
            "content": "I'm so happy about this!",
            "metadata": {
                "user_emotion": "joy",
                "user_emotion_score": 0.92,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:00:00"
            }
        }
    ]
    
    context = analyzer.get_emotional_context_summary(test_messages_1)
    adaptation = analyzer.get_emotional_adaptation_prompt(test_messages_1)
    
    print("\n=== EMOTIONAL CONTEXT ===")
    print(context)
    print("\n=== EMOTIONAL ADAPTATION ===")
    print(adaptation)
    
    # Test 2: Mixed emotions
    print("\n\n" + "=" * 80)
    print("TEST 2: Mixed Emotions (Love + Fear)")
    print("=" * 80)
    
    test_messages_2 = [
        {
            "content": "I love this project but I'm worried about the deadline",
            "metadata": {
                "user_emotion": "love",
                "user_emotion_score": 0.78,
                "user_emotion_is_mixed": True,
                "secondary_emotion": "fear",
                "timestamp": "2025-10-24T12:05:00"
            }
        }
    ]
    
    context = analyzer.get_emotional_context_summary(test_messages_2)
    adaptation = analyzer.get_emotional_adaptation_prompt(test_messages_2)
    
    print("\n=== EMOTIONAL CONTEXT ===")
    print(context)
    print("\n=== EMOTIONAL ADAPTATION ===")
    print(adaptation)
    
    # Test 3: Emotional trajectory - Improving
    print("\n\n" + "=" * 80)
    print("TEST 3: Emotional Trajectory - Improving (Fear → Anticipation → Joy)")
    print("=" * 80)
    
    test_messages_3 = [
        {
            "content": "I'm really worried about this task",
            "metadata": {
                "user_emotion": "fear",
                "user_emotion_score": 0.85,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:00:00"
            }
        },
        {
            "content": "Actually, I think I'm starting to figure it out",
            "metadata": {
                "user_emotion": "anticipation",
                "user_emotion_score": 0.75,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:02:00"
            }
        },
        {
            "content": "It works! I'm so happy!",
            "metadata": {
                "user_emotion": "joy",
                "user_emotion_score": 0.92,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:05:00"
            }
        }
    ]
    
    context = analyzer.get_emotional_context_summary(test_messages_3)
    adaptation = analyzer.get_emotional_adaptation_prompt(test_messages_3)
    
    print("\n=== EMOTIONAL CONTEXT ===")
    print(context)
    print("\n=== EMOTIONAL ADAPTATION ===")
    print(adaptation)
    
    # Test 4: Emotional trajectory - Declining
    print("\n\n" + "=" * 80)
    print("TEST 4: Emotional Trajectory - Declining (Joy → Pessimism → Anger)")
    print("=" * 80)
    
    test_messages_4 = [
        {
            "content": "I'm excited to start this project!",
            "metadata": {
                "user_emotion": "joy",
                "user_emotion_score": 0.88,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:00:00"
            }
        },
        {
            "content": "Hmm, this isn't working as expected",
            "metadata": {
                "user_emotion": "pessimism",
                "user_emotion_score": 0.72,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:10:00"
            }
        },
        {
            "content": "This is so frustrating! Nothing works!",
            "metadata": {
                "user_emotion": "anger",
                "user_emotion_score": 0.90,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:15:00"
            }
        }
    ]
    
    context = analyzer.get_emotional_context_summary(test_messages_4)
    adaptation = analyzer.get_emotional_adaptation_prompt(test_messages_4)
    
    print("\n=== EMOTIONAL CONTEXT ===")
    print(context)
    print("\n=== EMOTIONAL ADAPTATION ===")
    print(adaptation)
    
    # Test 5: Volatile emotions
    print("\n\n" + "=" * 80)
    print("TEST 5: Volatile Trajectory (Joy → Anger → Surprise → Sadness)")
    print("=" * 80)
    
    test_messages_5 = [
        {
            "content": "Great!",
            "metadata": {
                "user_emotion": "joy",
                "user_emotion_score": 0.85,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:00:00"
            }
        },
        {
            "content": "Wait, that's wrong!",
            "metadata": {
                "user_emotion": "anger",
                "user_emotion_score": 0.80,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:02:00"
            }
        },
        {
            "content": "Oh wow, I didn't expect that",
            "metadata": {
                "user_emotion": "surprise",
                "user_emotion_score": 0.75,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:04:00"
            }
        },
        {
            "content": "I give up, this is too much",
            "metadata": {
                "user_emotion": "sadness",
                "user_emotion_score": 0.82,
                "user_emotion_is_mixed": False,
                "timestamp": "2025-10-24T12:06:00"
            }
        }
    ]
    
    context = analyzer.get_emotional_context_summary(test_messages_5)
    adaptation = analyzer.get_emotional_adaptation_prompt(test_messages_5)
    
    print("\n=== EMOTIONAL CONTEXT ===")
    print(context)
    print("\n=== EMOTIONAL ADAPTATION ===")
    print(adaptation)
    
    # Test 6: All 11 emotions quick reference
    print("\n\n" + "=" * 80)
    print("TEST 6: All 11 Emotions - Quick Reference")
    print("=" * 80)
    
    all_emotions = [
        ("joy", "I'm so happy!"),
        ("love", "I love this so much!"),
        ("optimism", "I'm hopeful about the future"),
        ("trust", "I trust this will work out"),
        ("anticipation", "I'm excited about what's coming!"),
        ("anger", "This makes me so angry!"),
        ("disgust", "That's disgusting"),
        ("fear", "I'm scared about this"),
        ("sadness", "I feel so sad"),
        ("pessimism", "This probably won't work"),
        ("surprise", "Wow, I didn't expect that!")
    ]
    
    for emotion, example in all_emotions:
        test_msg = [{
            "content": example,
            "metadata": {
                "user_emotion": emotion,
                "user_emotion_score": 0.85,
                "user_emotion_is_mixed": False
            }
        }]
        context = analyzer.get_emotional_context_summary(test_msg)
        print(f"\n{emotion.upper()}: {context}")
    
    print("\n\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print("\nNOTE: To see these emotions in actual logs:")
    print("1. Start a new conversation (python main.py)")
    print("2. Express emotions like 'I'm excited but nervous'")
    print("3. Check logs/prompts/ for the enhanced formatting")
    print("\nThe old logs show 'NEUTRAL/POSITIVE' because they were created")
    print("BEFORE we upgraded to the 11-emotion model.")
    print("=" * 80)

if __name__ == "__main__":
    test_emotional_prompts()
