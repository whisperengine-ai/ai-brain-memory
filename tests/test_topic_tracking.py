"""Test topic tracking functionality."""

from ai_brain.memory import MemoryStore
from ai_brain.config import Config
import json

def test_topic_statistics():
    """Test the get_topic_statistics method."""
    print("🧪 Testing Topic Statistics\n")
    
    # Initialize memory store
    memory = MemoryStore()
    
    # Get topic statistics
    print("📊 Fetching topic statistics...")
    topics = memory.get_topic_statistics()
    
    if not topics:
        print("❌ No topics found!")
        return
    
    print(f"✅ Found {len(topics)} topics\n")
    
    # Display top 10 topics
    print("=" * 80)
    print("TOP 10 CONVERSATION TOPICS")
    print("=" * 80)
    
    for i, (topic, stats) in enumerate(list(topics.items())[:10], 1):
        print(f"\n{i}. {topic.upper()}")
        print(f"   Mentions: {stats['count']}")
        print(f"   Dominant Sentiment: {stats['dominant_sentiment']}")
        print(f"   Sentiment Distribution: {stats['sentiment_distribution']}")
        if stats.get('dominant_emotions'):
            print(f"   Dominant Emotions: {', '.join(stats['dominant_emotions'])}")
    
    print("\n" + "=" * 80)
    print(f"Total unique topics: {len(topics)}")
    print("=" * 80)
    
    # Save to JSON for inspection
    output_file = "topic_statistics.json"
    with open(output_file, 'w') as f:
        json.dump(topics, f, indent=2)
    print(f"\n💾 Full results saved to {output_file}")

if __name__ == "__main__":
    test_topic_statistics()
