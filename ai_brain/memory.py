"""Memory management using ChromaDB for persistent vector storage."""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

from .config import Config
from .device_utils import get_torch_device, get_device


class MemoryStore:
    """Persistent memory store using ChromaDB with local embeddings."""
    
    def __init__(self):
        """Initialize ChromaDB and embedding model."""
        print(f"🧠 Initializing memory store at {Config.CHROMA_PERSIST_DIR}...")
        
        # Create persist directory if it doesn't exist
        Config.CHROMA_PERSIST_DIR.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(
            path=str(Config.CHROMA_PERSIST_DIR),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection with cosine distance for semantic similarity
        self.collection = self.client.get_or_create_collection(
            name=Config.CHROMA_COLLECTION_NAME,
            metadata={
                "description": "AI Brain persistent memory",
                "hnsw:space": "cosine"  # Use cosine similarity for embeddings
            }
        )
        
        # Initialize embedding model with proper device
        print(f"🔮 Loading embedding model: {Config.EMBEDDING_MODEL}...")
        device_type, device_desc = get_device()
        
        # SentenceTransformer accepts device string directly
        torch_device = get_torch_device()
        self.embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL, device=torch_device)
        
        print(f"✅ Memory store initialized with {self.collection.count()} memories")
        print(f"   Using device: {device_desc}")
    
    def add_memory(
        self,
        content: str,
        memory_type: str = "conversation",
        metadata: Optional[Dict[str, Any]] = None,
        enable_nlp: bool = True
    ) -> str:
        """
        Add a new memory to the store with optional NLP enrichment.
        
        Args:
            content: The content to remember
            memory_type: Type of memory (conversation, fact, event, etc.)
            metadata: Additional metadata
            enable_nlp: Whether to perform NLP analysis for enrichment
            
        Returns:
            Memory ID
        """
        memory_id = str(uuid.uuid4())
        
        # Generate embedding
        embedding = self.embedding_model.encode(content).tolist()
        
        # Prepare base metadata
        meta = {
            "type": memory_type,
            "timestamp": datetime.now().isoformat(),
            **(metadata or {})
        }
        
        # Add NLP enrichment if enabled
        if enable_nlp:
            try:
                from .nlp_analyzer import get_analyzer
                analyzer = get_analyzer()
                role = metadata.get("role", "user") if metadata else "user"
                nlp_metadata = analyzer.enrich_conversation_entry(content, role=role)
                meta.update(nlp_metadata)
            except Exception as e:
                print(f"⚠️  NLP enrichment failed: {e}")
        
        # Store in ChromaDB
        self.collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta]
        )
        
        return memory_id
    
    def retrieve_memories(
        self,
        query: str,
        n_results: int = None,
        memory_type: Optional[str] = None,
        query_analysis: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories using hybrid search (vector + metadata boosting).
        
        Args:
            query: Query text to find relevant memories
            n_results: Number of results to return
            memory_type: Filter by memory type
            query_analysis: Optional query analysis from enhance_query() for metadata boosting
            
        Returns:
            List of relevant memories with metadata and boosted scores
        """
        if n_results is None:
            n_results = Config.MEMORY_CONTEXT_SIZE
        
        # Check if collection is empty
        collection_count = self.collection.count()
        if collection_count == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Build where clause for filtering
        where_clause = {"type": memory_type} if memory_type else None
        
        # Fetch 3x results for reranking (if we have enough memories)
        fetch_size = min(n_results * 3, collection_count) if query_analysis else min(n_results, collection_count)
        
        # Query ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=fetch_size,
            where=where_clause
        )
        
        # Format results
        memories = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results["distances"] else 0
                similarity = 1 - distance  # Convert distance to similarity
                
                # Filter by relevance threshold
                if similarity >= Config.MEMORY_RELEVANCE_THRESHOLD:
                    memory = {
                        "id": results["ids"][0][i],
                        "content": doc,
                        "metadata": results["metadatas"][0][i],
                        "similarity": similarity,
                        "boosted_score": similarity  # Will be adjusted if query_analysis provided
                    }
                    memories.append(memory)
        
        # HYBRID SEARCH: Boost scores based on metadata matching
        if query_analysis and memories:
            query_entities = set(e.lower() for e in query_analysis.get("entity_values", []))
            query_keywords = set(k.lower() for k in query_analysis.get("top_keywords", []))
            
            for memory in memories:
                entity_boost = 0.0
                keyword_boost = 0.0
                metadata = memory["metadata"]
                
                # Check for entity matches in metadata (higher boost)
                for entity_type in ["entities_person", "entities_org", "entities_gpe", "entities_product"]:
                    if entity_type in metadata and metadata[entity_type]:
                        memory_entities = set(metadata[entity_type].lower().split(", "))
                        entity_overlap = len(query_entities & memory_entities)
                        if entity_overlap > 0:
                            entity_boost += 0.15 * entity_overlap  # +0.15 per entity match
                
                # Check for keyword matches (lower boost)
                if "keywords" in metadata and metadata["keywords"]:
                    memory_keywords = set(metadata["keywords"].lower().split(", "))
                    keyword_overlap = len(query_keywords & memory_keywords)
                    if keyword_overlap > 0:
                        keyword_boost += 0.05 * keyword_overlap  # +0.05 per keyword match
                
                # Calculate total boost (cap at +0.3)
                total_boost = min(entity_boost + keyword_boost, 0.3)
                
                # Store boost details for logging
                memory["entity_boost"] = entity_boost
                memory["keyword_boost"] = keyword_boost
                memory["total_boost"] = total_boost
                
                # Apply boost (cap at 1.0 for final score)
                memory["boosted_score"] = min(memory["similarity"] + total_boost, 1.0)
        
        # Sort by boosted score if hybrid search was used, otherwise by similarity
        if query_analysis:
            memories.sort(key=lambda x: x["boosted_score"], reverse=True)
        
        # Return top n_results
        return memories[:n_results]
    
    def get_conversation_history(self, n_recent: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversation history sorted by timestamp.
        
        Args:
            n_recent: Number of recent conversations to retrieve
            
        Returns:
            List of recent conversation memories (oldest first for context)
        """
        # Get all conversation memories (ChromaDB doesn't support ordering in get())
        results = self.collection.get(
            where={"type": "conversation"}
        )
        
        # Build and sort by timestamp
        memories = []
        if results["documents"]:
            for i, doc in enumerate(results["documents"]):
                memories.append({
                    "id": results["ids"][i],
                    "content": doc,
                    "metadata": results["metadatas"][i]
                })
        
        # Sort by timestamp (newest first)
        memories.sort(
            key=lambda x: x["metadata"].get("timestamp", ""),
            reverse=True
        )
        
        # Get the n most recent
        recent = memories[:n_recent]
        
        # Return in chronological order (oldest first) for proper context flow
        return list(reversed(recent))
    
    def clear_all_memories(self):
        """Clear all memories from the store."""
        # Delete and recreate collection
        self.client.delete_collection(Config.CHROMA_COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=Config.CHROMA_COLLECTION_NAME,
            metadata={"description": "AI Brain persistent memory"}
        )
        print("🗑️  All memories cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory store statistics."""
        total_count = self.collection.count()
        
        return {
            "total_memories": total_count,
            "collection_name": Config.CHROMA_COLLECTION_NAME,
            "persist_dir": str(Config.CHROMA_PERSIST_DIR)
        }
    
    def get_topic_statistics(self) -> Dict[str, Any]:
        """
        Analyze all memories and return topic statistics.
        
        Returns comprehensive statistics about conversation topics including:
        - Count of mentions per topic
        - Sentiment distribution for each topic
        - Dominant sentiment per topic
        - Overall topic trends
        
        Returns:
            Dictionary mapping topics to their statistics:
            {
                "python": {
                    "count": 15,
                    "sentiment_distribution": {"positive": 10, "neutral": 3, "negative": 2},
                    "dominant_sentiment": "positive",
                    "dominant_emotions": ["joy", "optimism"]
                },
                ...
            }
        """
        from collections import Counter
        
        # Get all memories
        results = self.collection.get()
        
        if not results["documents"] or not results["metadatas"]:
            return {}
        
        # Aggregate data by topic (entity and keyword)
        topic_data: Dict[str, Dict[str, Any]] = {}
        
        for i, metadata in enumerate(results["metadatas"]):
            sentiment = metadata.get("sentiment", "neutral")
            
            # Get emotions - check both user and bot emotions
            emotions = []
            user_emotion = metadata.get("user_emotion")
            bot_emotion = metadata.get("bot_emotion")
            if user_emotion and user_emotion != "neutral":
                emotions.append(user_emotion)
            if bot_emotion and bot_emotion != "neutral" and bot_emotion != user_emotion:
                emotions.append(bot_emotion)
            
            # Track all topics from different sources
            all_topics = []
            
            # 1. Get entity values from entity_* keys
            for key, value in metadata.items():
                if key.startswith("entities_") and value:
                    # Split comma-separated entities
                    if isinstance(value, str):
                        entities = [e.strip() for e in value.split(",") if e.strip()]
                        all_topics.extend(entities)
            
            # 2. Get keywords (comma-separated string)
            keywords_str = metadata.get("keywords", "")
            if keywords_str and isinstance(keywords_str, str):
                keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
                all_topics.extend(keywords[:3])  # Limit to top 3 keywords
            
            # Update statistics for each topic
            for topic in all_topics:
                if topic and len(topic) > 1:  # Skip single characters and empty
                    topic_lower = topic.lower()
                    
                    # Initialize topic data if not exists
                    if topic_lower not in topic_data:
                        topic_data[topic_lower] = {
                            "count": 0,
                            "sentiments": [],
                            "emotions": []
                        }
                    
                    # Update counts
                    topic_data[topic_lower]["count"] += 1
                    topic_data[topic_lower]["sentiments"].append(sentiment)
                    if emotions:
                        topic_data[topic_lower]["emotions"].extend(emotions)
        
        # Build final statistics with sentiment distribution
        topic_stats = {}
        for topic, data in topic_data.items():
            if data["count"] >= 2:  # Only include topics mentioned 2+ times
                # Calculate sentiment distribution
                sentiment_counts = Counter(data["sentiments"])
                sentiment_dist = dict(sentiment_counts)
                
                # Find dominant sentiment
                dominant_sentiment = sentiment_counts.most_common(1)[0][0] if sentiment_counts else "neutral"
                
                # Find dominant emotions (top 2)
                emotion_counts = Counter(data["emotions"])
                dominant_emotions = [e for e, _ in emotion_counts.most_common(2)]
                
                topic_stats[topic] = {
                    "count": data["count"],
                    "sentiment_distribution": sentiment_dist,
                    "dominant_sentiment": dominant_sentiment,
                    "dominant_emotions": dominant_emotions if dominant_emotions else []
                }
        
        # Sort by count (most discussed topics first)
        sorted_topics = dict(sorted(
            topic_stats.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        ))
        
        return sorted_topics
