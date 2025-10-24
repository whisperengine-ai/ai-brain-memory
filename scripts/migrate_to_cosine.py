#!/usr/bin/env python3
"""
Migrate ChromaDB collection to use cosine distance instead of l2.
This will preserve all memories while updating the distance metric.
"""
import chromadb
from chromadb.config import Settings
from pathlib import Path
from ai_brain.config import Config

def migrate_to_cosine():
    print("=" * 80)
    print("MIGRATING CHROMADB TO COSINE DISTANCE")
    print("=" * 80)
    print()
    
    # Connect to existing DB
    client = chromadb.PersistentClient(
        path=str(Config.CHROMA_PERSIST_DIR),
        settings=Settings(anonymized_telemetry=False, allow_reset=True)
    )
    
    collection_name = Config.CHROMA_COLLECTION_NAME
    
    try:
        # Get existing collection
        old_collection = client.get_collection(name=collection_name)
        count = old_collection.count()
        
        print(f"📊 Found existing collection: {collection_name}")
        print(f"   Memories: {count}")
        print()
        
        if count == 0:
            print("⚠️  Collection is empty, just updating metadata...")
            client.delete_collection(name=collection_name)
            new_collection = client.create_collection(
                name=collection_name,
                metadata={
                    "description": "AI Brain persistent memory",
                    "hnsw:space": "cosine"
                }
            )
            print("✅ Created new collection with cosine distance")
            return
        
        # Get all data
        print("📥 Retrieving all memories...")
        all_data = old_collection.get()
        
        ids = all_data['ids']
        documents = all_data['documents']
        embeddings = all_data['embeddings']
        metadatas = all_data['metadatas']
        
        print(f"✅ Retrieved {len(ids)} memories")
        print()
        
        # Delete old collection
        print("🗑️  Deleting old collection...")
        client.delete_collection(name=collection_name)
        print("✅ Deleted")
        print()
        
        # Create new collection with cosine distance
        print("🆕 Creating new collection with cosine distance...")
        new_collection = client.create_collection(
            name=collection_name,
            metadata={
                "description": "AI Brain persistent memory",
                "hnsw:space": "cosine"
            }
        )
        print("✅ Created")
        print()
        
        # Re-add all data
        print("📤 Re-adding all memories...")
        new_collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"✅ Added {len(ids)} memories")
        print()
        
        print("=" * 80)
        print("✅ MIGRATION COMPLETE!")
        print("=" * 80)
        print()
        print("The collection now uses cosine distance for better semantic similarity.")
        print("Similarities will now range from -1 (opposite) to 1 (identical).")
        print()
        
    except ValueError:
        # Collection doesn't exist yet
        print(f"ℹ️  Collection doesn't exist yet, will be created with cosine distance.")
        print("✅ No migration needed - run the app to create the collection.")

if __name__ == "__main__":
    migrate_to_cosine()
