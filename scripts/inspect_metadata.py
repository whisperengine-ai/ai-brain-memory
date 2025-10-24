"""Debug script to check metadata structure in database."""

from ai_brain.memory import MemoryStore
import json

def inspect_metadata():
    """Inspect metadata structure in the database."""
    print("🔍 Inspecting Database Metadata\n")
    
    # Initialize memory store
    memory = MemoryStore()
    
    # Get all memories
    results = memory.collection.get()
    
    if not results["metadatas"]:
        print("❌ No memories found in database!")
        return
    
    print(f"✅ Found {len(results['metadatas'])} memories\n")
    
    # Show first 5 metadata examples
    print("=" * 80)
    print("SAMPLE METADATA (First 5 Memories)")
    print("=" * 80)
    
    for i, metadata in enumerate(results["metadatas"][:5], 1):
        print(f"\n{i}. Memory Metadata:")
        print(json.dumps(metadata, indent=2))
        print("-" * 80)
    
    # Analyze metadata keys
    print("\n" + "=" * 80)
    print("METADATA KEY ANALYSIS")
    print("=" * 80)
    
    all_keys = set()
    for metadata in results["metadatas"]:
        all_keys.update(metadata.keys())
    
    print(f"\nAll metadata keys found: {sorted(all_keys)}")
    
    # Count memories with specific keys
    print("\n" + "=" * 80)
    print("KEY PRESENCE COUNTS")
    print("=" * 80)
    
    key_counts = {}
    for key in all_keys:
        count = sum(1 for m in results["metadatas"] if key in m)
        key_counts[key] = count
    
    for key, count in sorted(key_counts.items()):
        print(f"  {key}: {count}/{len(results['metadatas'])} memories")

if __name__ == "__main__":
    inspect_metadata()
