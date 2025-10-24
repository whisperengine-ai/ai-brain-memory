"""
NLP Analysis module using spaCy and RoBERTa for enhanced memory tagging.

This module provides:
- Named Entity Recognition (NER)
- Part-of-Speech tagging
- Dependency parsing
- Sentiment analysis using RoBERTa
- Keyword extraction
- Topic identification
"""

import spacy
from typing import Dict, List, Any, Optional
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
from collections import Counter
from .device_utils import get_torch_device, get_device
from .config import Config


class NLPAnalyzer:
    """
    Advanced NLP analyzer for text processing, entity extraction,
    and sentiment analysis to enrich memory metadata.
    """
    
    def __init__(self, spacy_model: str = None, sentiment_model: str = None):
        """
        Initialize NLP components.
        
        Args:
            spacy_model: spaCy model to use (defaults to Config.SPACY_MODEL)
            sentiment_model: Sentiment model to use (defaults to Config.SENTIMENT_MODEL)
        """
        print(f"🔬 Initializing NLP Analyzer...")
        
        # Use config defaults if not specified
        spacy_model = spacy_model or Config.SPACY_MODEL
        sentiment_model = sentiment_model or Config.SENTIMENT_MODEL
        
        # Detect device
        device_type, device_desc = get_device()
        print(f"   Using device: {device_desc}")
        
        # Load spaCy model
        try:
            self.nlp = spacy.load(spacy_model)
            print(f"✅ Loaded spaCy model: {spacy_model}")
        except OSError:
            print(f"⚠️  spaCy model '{spacy_model}' not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", spacy_model])
            self.nlp = spacy.load(spacy_model)
            print(f"✅ Downloaded and loaded spaCy model: {spacy_model}")
        
        # Initialize RoBERTa sentiment analyzer
        print(f"🤖 Loading sentiment analyzer: {sentiment_model}...")
        
        # Determine device for transformers pipeline
        # pipeline uses: device=0 for CUDA/MPS, device=-1 for CPU
        torch_device = get_torch_device()
        pipeline_device = 0 if torch_device in ["cuda", "mps"] else -1
        
        # Use text-classification for emotion detection (multi-label)
        self.sentiment_analyzer = pipeline(
            "text-classification",
            model=sentiment_model,
            tokenizer=sentiment_model,
            device=pipeline_device,
            top_k=None  # Return all emotion scores
        )
        
        device_name = "GPU" if pipeline_device == 0 else "CPU"
        print(f"✅ Emotion analyzer loaded (11 emotions) on {device_name}")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive NLP analysis on text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with analysis results including entities, sentiment, keywords, etc.
        """
        # Process with spaCy
        doc = self.nlp(text)
        
        # Extract named entities
        entities = self._extract_entities(doc)
        
        # Extract keywords (nouns and proper nouns)
        keywords = self._extract_keywords(doc)
        
        # Extract topics/themes
        topics = self._extract_topics(doc)
        
        # Perform sentiment analysis
        sentiment = self._analyze_sentiment(text)
        
        # Extract linguistic features
        linguistic_features = self._extract_linguistic_features(doc)
        
        # Get key phrases
        key_phrases = self._extract_key_phrases(doc)
        
        return {
            "entities": entities,
            "keywords": keywords,
            "topics": topics,
            "sentiment": sentiment,
            "linguistic_features": linguistic_features,
            "key_phrases": key_phrases,
            "language": doc.lang_,
            "length": {
                "chars": len(text),
                "words": len([token for token in doc if not token.is_punct]),
                "sentences": len(list(doc.sents))
            }
        }
    
    def _extract_entities(self, doc: spacy.tokens.Doc) -> Dict[str, List[str]]:
        """Extract and categorize named entities."""
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        # Remove duplicates while preserving order
        for label in entities:
            entities[label] = list(dict.fromkeys(entities[label]))
        
        return entities
    
    def _extract_keywords(self, doc: spacy.tokens.Doc) -> List[str]:
        """Extract important keywords (nouns, proper nouns, verbs)."""
        keywords = []
        for token in doc:
            # Include important POS tags
            if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop:
                keywords.append(token.lemma_.lower())
        
        # Count frequency and return top keywords
        keyword_freq = Counter(keywords)
        return [word for word, _ in keyword_freq.most_common(10)]
    
    def _extract_topics(self, doc: spacy.tokens.Doc) -> List[str]:
        """Extract potential topics from noun chunks and entities."""
        topics = []
        
        # Add noun chunks
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:  # Keep it concise
                topics.append(chunk.text.lower())
        
        # Add named entities as topics
        for ent in doc.ents:
            topics.append(ent.text.lower())
        
        # Remove duplicates and return top topics
        topic_freq = Counter(topics)
        return [topic for topic, _ in topic_freq.most_common(5)]
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze emotions using Cardiff NLP RoBERTa multi-label model.
        
        Detects 11 emotions: anger, anticipation, disgust, fear, joy, love, 
        optimism, pessimism, sadness, surprise, trust
        
        Returns primary emotion, all scores, and mixed emotion detection.
        """
        # Truncate text if too long (RoBERTa has token limit)
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        try:
            # Get all emotion scores (returns list of dicts with label and score)
            results = self.sentiment_analyzer(text)[0]
            
            # Sort by score to get primary and secondary emotions
            sorted_emotions = sorted(results, key=lambda x: x['score'], reverse=True)
            
            # Get primary emotion (highest score)
            primary = sorted_emotions[0]
            primary_emotion = primary['label'].lower()
            primary_score = primary['score']
            
            # Get all emotions above threshold (0.3) for mixed emotion detection
            significant_emotions = [e for e in sorted_emotions if e['score'] > 0.3]
            
            # Categorize emotions into positive, negative, neutral for compatibility
            emotion_categories = {
                "positive": ["joy", "love", "optimism", "trust", "anticipation"],
                "negative": ["anger", "disgust", "fear", "sadness", "pessimism"],
                "neutral": ["surprise"]
            }
            
            # Determine category of primary emotion
            category = "neutral"
            for cat, emotions in emotion_categories.items():
                if primary_emotion in emotions:
                    category = cat
                    break
            
            # Detect mixed emotions
            is_mixed = False
            mixed_emotions = []
            secondary_emotion = None
            secondary_score = 0.0
            
            if len(significant_emotions) > 1:
                # Check if we have emotions from different categories
                categories_present = set()
                for emotion in significant_emotions[:3]:  # Top 3
                    for cat, emo_list in emotion_categories.items():
                        if emotion['label'].lower() in emo_list:
                            categories_present.add(cat)
                            mixed_emotions.append(emotion['label'].lower())
                
                # Mixed if we have both positive and negative
                if "positive" in categories_present and "negative" in categories_present:
                    is_mixed = True
                    secondary_emotion = significant_emotions[1]['label'].lower()
                    secondary_score = significant_emotions[1]['score']
            
            # Detect linguistic contrast markers for additional mixed emotion detection
            text_lower = text.lower()
            contrast_markers = ["but", "however", "although", "though", "yet", 
                              "on the other hand", "at the same time", "mixed feelings"]
            has_contrast = any(marker in text_lower for marker in contrast_markers)
            
            # Build comprehensive result
            sentiment_result = {
                "label": primary_emotion,  # Specific emotion (joy, sadness, etc.)
                "category": category,  # Simplified category (positive/negative/neutral)
                "score": primary_score,
                "confidence": primary_score,
                "is_mixed": is_mixed or (has_contrast and len(significant_emotions) > 1),
                "has_contrast_markers": has_contrast,
                "all_emotions": {e['label'].lower(): e['score'] for e in sorted_emotions},
                "significant_emotions": mixed_emotions[:3] if is_mixed else [primary_emotion]
            }
            
            # Add secondary emotion if mixed
            if is_mixed and secondary_emotion:
                sentiment_result["secondary_emotion"] = secondary_emotion
                sentiment_result["secondary_score"] = secondary_score
                sentiment_result["mixed_context"] = f"Expressing both {primary_emotion} and {secondary_emotion}"
            elif has_contrast:
                sentiment_result["mixed_context"] = "Contains contrasting emotional indicators"
            
            return sentiment_result
            
        except Exception as e:
            print(f"⚠️  Emotion analysis failed: {e}")
            return {
                "label": "neutral",
                "category": "neutral",
                "score": 0.5,
                "confidence": 0.0,
                "is_mixed": False,
                "has_contrast_markers": False,
                "all_emotions": {},
                "significant_emotions": ["neutral"]
            }
    
    def _extract_linguistic_features(self, doc: spacy.tokens.Doc) -> Dict[str, Any]:
        """Extract linguistic features like POS distribution."""
        pos_counts = Counter([token.pos_ for token in doc if not token.is_punct])
        
        return {
            "pos_distribution": dict(pos_counts),
            "has_questions": any(token.text == "?" for token in doc),
            "has_negation": any(token.dep_ == "neg" for token in doc),
            "avg_word_length": sum(len(token.text) for token in doc if not token.is_punct) / max(1, len([t for t in doc if not t.is_punct]))
        }
    
    def _extract_key_phrases(self, doc: spacy.tokens.Doc) -> List[str]:
        """Extract key phrases using noun chunks and important patterns."""
        phrases = []
        
        # Noun chunks
        for chunk in doc.noun_chunks:
            if 2 <= len(chunk.text.split()) <= 4:
                phrases.append(chunk.text)
        
        # Subject-Verb-Object patterns
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                subjects = [child.text for child in token.children if child.dep_ in ["nsubj", "nsubjpass"]]
                objects = [child.text for child in token.children if child.dep_ in ["dobj", "pobj"]]
                if subjects and objects:
                    phrases.append(f"{' '.join(subjects)} {token.text} {' '.join(objects)}")
        
        return phrases[:5]  # Return top 5
    
    def enhance_query(self, user_message: str) -> Dict[str, Any]:
        """
        Analyze incoming user message with spaCy to enhance memory retrieval.
        
        This extracts key information BEFORE querying to make searches smarter:
        - Keywords and entities for expanded search
        - Intent for filtering (questions vs statements)
        - Topics for semantic context
        
        Args:
            user_message: The incoming user message to analyze
            
        Returns:
            Dictionary with enhanced query info:
            {
                "original_query": str,
                "enhanced_query": str,  # Expanded with keywords/entities
                "keywords": List[str],
                "entities": Dict[str, List[str]],
                "topics": List[str],
                "intent": str,
                "query_focus": str,  # What user is asking about
                "should_search_by": str  # "entities", "keywords", "topics", "all"
            }
        """
        # Analyze with spaCy
        doc = self.nlp(user_message)
        
        # Extract components
        entities = self._extract_entities(doc)
        keywords = self._extract_keywords(doc)
        topics = self._extract_topics(doc)
        intent = self.extract_intent(user_message)
        
        # Build enhanced query with deduplication
        query_parts = [user_message]  # Start with original
        
        # Add entity values (more specific)
        entity_values = []
        for entity_type, values in entities.items():
            if entity_type in ["PERSON", "ORG", "GPE", "PRODUCT", "EVENT"]:
                entity_values.extend(values)
        
        # Add top keywords (more general)
        top_keywords = keywords[:5]
        
        # Build deduplicated query parts
        # Create set of all words/terms in original message (lowercase)
        original_lower = user_message.lower()
        original_words = set(original_lower.split())
        
        # Helper function to check if term is already represented
        def is_already_present(term: str) -> bool:
            term_lower = term.lower()
            # Check if term is in original words
            if term_lower in original_words:
                return True
            # Check if term appears as substring in original
            if term_lower in original_lower:
                return True
            # Check if any word in term appears in original
            term_words = set(term_lower.split())
            if term_words.issubset(original_words):
                return True
            return False
        
        # Determine query focus and add non-duplicate terms
        if entity_values:
            query_focus = f"entities: {', '.join(entity_values[:3])}"
            should_search_by = "entities"
            # Add entity values NOT already in original query
            new_entities = [e for e in entity_values if not is_already_present(e)]
            if new_entities:
                query_parts.extend(new_entities[:3])  # Limit to top 3
        elif topics:
            query_focus = f"topics: {', '.join(topics[:2])}"
            should_search_by = "topics"
            # Add topics NOT already in original
            new_topics = [t for t in topics[:3] if not is_already_present(t)]
            if new_topics:
                query_parts.extend(new_topics)
        else:
            query_focus = f"keywords: {', '.join(top_keywords[:3])}"
            should_search_by = "keywords"
            # Add keywords NOT already in original
            new_keywords = [k for k in top_keywords if not is_already_present(k)]
            if new_keywords:
                query_parts.extend(new_keywords[:3])  # Limit to top 3
        
        # Build enhanced query string (deduplicated)
        enhanced_query = " ".join(query_parts)
        
        return {
            "original_query": user_message,
            "enhanced_query": enhanced_query,
            "keywords": keywords,
            "entities": entities,
            "topics": topics,
            "intent": intent,
            "query_focus": query_focus,
            "should_search_by": should_search_by,
            "entity_values": entity_values,
            "top_keywords": top_keywords
        }
    
    def create_metadata_tags(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create structured metadata tags from analysis for vector store.
        
        Args:
            analysis: Result from analyze_text()
            
        Returns:
            Clean metadata dictionary suitable for ChromaDB
        """
        metadata = {
            # Sentiment
            "sentiment": analysis["sentiment"]["label"],
            "sentiment_score": float(analysis["sentiment"]["score"]),
            
            # Content type indicators
            "has_question": analysis["linguistic_features"]["has_questions"],
            "has_negation": analysis["linguistic_features"]["has_negation"],
            
            # Length metrics
            "word_count": analysis["length"]["words"],
            "sentence_count": analysis["length"]["sentences"],
            
            # Keywords (top 5, joined as string for ChromaDB)
            "keywords": ", ".join(analysis["keywords"][:5]) if analysis["keywords"] else "",
            
            # Topics
            "topics": ", ".join(analysis["topics"][:3]) if analysis["topics"] else "",
            
            # Entity counts
            "entity_count": sum(len(entities) for entities in analysis["entities"].values()),
        }
        
        # Add entity types as separate fields
        for entity_type, entities in analysis["entities"].items():
            if entities:
                # Store first few entities of each type
                metadata[f"entities_{entity_type.lower()}"] = ", ".join(entities[:3])
        
        return metadata
    
    def extract_intent(self, text: str) -> str:
        """
        Determine user intent from text.
        
        Returns intent category like: question, statement, command, expression
        """
        doc = self.nlp(text)
        
        # Check for question
        if any(token.text == "?" for token in doc):
            return "question"
        
        # Check for question words at start
        question_words = ["what", "when", "where", "who", "why", "how", "which", "whose", "whom"]
        if doc[0].text.lower() in question_words:
            return "question"
        
        # Check for imperative (commands)
        if doc[0].pos_ == "VERB" and doc[0].dep_ == "ROOT":
            return "command"
        
        # Check for expression/emotion (exclamation)
        if any(token.text == "!" for token in doc):
            return "expression"
        
        # Default to statement
        return "statement"
    
    def enrich_conversation_entry(self, text: str, role: str = "user") -> Dict[str, Any]:
        """
        Create enriched conversation entry with full NLP analysis.
        
        Args:
            text: Conversation text
            role: "user" or "assistant"
            
        Returns:
            Complete metadata dictionary for storage
        """
        analysis = self.analyze_text(text)
        metadata = self.create_metadata_tags(analysis)
        
        # Add role and intent
        metadata["role"] = role
        if role == "user":
            metadata["intent"] = self.extract_intent(text)
        
        # Add emotion scores with role prefix for tracking
        if role == "user":
            metadata["user_emotion"] = analysis["sentiment"]["label"]
            metadata["user_emotion_score"] = float(analysis["sentiment"]["score"])
            # Add mixed emotion flags
            metadata["user_emotion_is_mixed"] = analysis["sentiment"].get("is_mixed", False)
            if metadata["user_emotion_is_mixed"]:
                metadata["user_emotion_mixed_context"] = analysis["sentiment"].get("mixed_context", "")
        else:  # assistant
            metadata["bot_emotion"] = analysis["sentiment"]["label"]
            metadata["bot_emotion_score"] = float(analysis["sentiment"]["score"])
        
        return metadata
    
    def get_emotional_context_summary(self, recent_messages: List[Dict[str, Any]], n_recent: int = 10) -> str:
        """
        Generate emotional context summary from recent conversation history.
        
        Args:
            recent_messages: List of recent message dictionaries with metadata
            n_recent: Number of recent messages to analyze (default: 10, increased from 5)
            
        Returns:
            Human-readable emotional context string
        """
        if not recent_messages:
            return "No recent emotional context available."
        
        # Analyze recent messages (limit to n_recent)
        recent = recent_messages[:n_recent]
        
        user_emotions = []
        bot_emotions = []
        
        for msg in recent:
            metadata = msg.get("metadata", {})
            
            # Collect user emotions
            if "user_emotion" in metadata:
                user_emotions.append({
                    "emotion": metadata["user_emotion"],
                    "score": metadata.get("user_emotion_score", 0.0),
                    "is_mixed": metadata.get("user_emotion_is_mixed", False),
                    "mixed_context": metadata.get("user_emotion_mixed_context", "")
                })
            
            # Collect bot emotions
            if "bot_emotion" in metadata:
                bot_emotions.append({
                    "emotion": metadata["bot_emotion"],
                    "score": metadata.get("bot_emotion_score", 0.0)
                })
        
        # Build summary with natural language descriptions
        summary_parts = []
        
        if user_emotions:
            # Get dominant user emotion
            latest_user = user_emotions[-1]
            emotion = latest_user['emotion']
            score = latest_user['score']
            is_mixed = latest_user.get('is_mixed', False)
            
            # Convert confidence to natural language
            if score >= 0.85:
                confidence_desc = "very clearly"
            elif score >= 0.70:
                confidence_desc = "clearly"
            elif score >= 0.60:
                confidence_desc = "somewhat"
            else:
                confidence_desc = "slightly"
            
            # Build natural language description for 11 emotions
            emotion_descriptions = {
                # Positive emotions
                "joy": f"The user is {confidence_desc} feeling joyful and happy",
                "love": f"The user is {confidence_desc} expressing love, affection, or deep appreciation",
                "optimism": f"The user is {confidence_desc} feeling optimistic and hopeful about the future",
                "trust": f"The user is {confidence_desc} showing trust and confidence",
                "anticipation": f"The user is {confidence_desc} feeling anticipation and excitement",
                # Negative emotions
                "anger": f"The user is {confidence_desc} feeling angry or frustrated",
                "disgust": f"The user is {confidence_desc} expressing disgust or strong disapproval",
                "fear": f"The user is {confidence_desc} feeling afraid or anxious",
                "sadness": f"The user is {confidence_desc} feeling sad or disappointed",
                "pessimism": f"The user is {confidence_desc} feeling pessimistic or discouraged",
                # Neutral/ambiguous
                "surprise": f"The user is {confidence_desc} feeling surprised or caught off guard"
            }
            
            # Handle mixed emotions
            if is_mixed:
                secondary = latest_user.get('secondary_emotion', '')
                if secondary:
                    summary_parts.append(f"The user is expressing {confidence_desc} mixed emotions - primarily {emotion} with elements of {secondary}")
                else:
                    summary_parts.append(f"The user is expressing {confidence_desc} complex emotions with {emotion} being most prominent")
            else:
                description = emotion_descriptions.get(emotion, f"The user appears {emotion}")
                summary_parts.append(description)
            
            # Check for emotional shifts
            if len(user_emotions) >= 2:
                emotions_list = [e["emotion"] for e in user_emotions]
                if len(set(emotions_list)) > 1:
                    # Describe the shift in natural language with specific emotions
                    shift_sequence = emotions_list[-3:] if len(emotions_list) >= 3 else emotions_list[-2:]
                    
                    # Categorize emotions for trajectory detection
                    positive_emotions = ["joy", "love", "optimism", "trust", "anticipation"]
                    negative_emotions = ["anger", "disgust", "fear", "sadness", "pessimism"]
                    
                    # Check if mood is improving
                    first_is_negative = shift_sequence[0] in negative_emotions
                    last_is_positive = shift_sequence[-1] in positive_emotions
                    first_is_positive = shift_sequence[0] in positive_emotions
                    last_is_negative = shift_sequence[-1] in negative_emotions
                    
                    if first_is_negative and last_is_positive:
                        summary_parts.append(f"Their mood has been improving: {' → '.join(shift_sequence)}")
                    elif first_is_positive and last_is_negative:
                        summary_parts.append(f"Their mood appears to be declining: {' → '.join(shift_sequence)} - be extra careful and supportive")
                    elif len(set(shift_sequence)) > 2:
                        summary_parts.append(f"Their emotions have shifted through: {' → '.join(shift_sequence)}")
                    else:
                        # Show progression even if trajectory is stable
                        summary_parts.append(f"Recent emotional state: {' → '.join(shift_sequence)}")
        
        if bot_emotions:
            # Get dominant bot emotion
            latest_bot = bot_emotions[-1]
            bot_emotion = latest_bot['emotion']
            
            # Categorize bot emotions
            positive_bot_emotions = ["joy", "love", "optimism", "trust", "anticipation"]
            negative_bot_emotions = ["anger", "disgust", "fear", "sadness", "pessimism"]
            
            if bot_emotion in positive_bot_emotions:
                bot_desc = "Your recent responses have been upbeat and encouraging"
            elif bot_emotion in negative_bot_emotions:
                bot_desc = "Your recent responses have been more serious or cautionary"
            else:
                bot_desc = "Your recent responses have been informative and professional"
            
            summary_parts.append(bot_desc)
        
        # Join parts into readable sentences with wrapping
        if summary_parts:
            full_text = ". ".join(summary_parts) + "."
            # Wrap text at 80 characters for better readability
            import textwrap
            wrapped = textwrap.fill(full_text, width=80, break_long_words=False, break_on_hyphens=False)
            return wrapped
        else:
            return "No strong emotional signals detected in recent conversation."
    
    def should_adjust_tone(self, user_emotion: str, user_score: float) -> Dict[str, str]:
        """
        Determine if bot should adjust its tone based on user's emotion.
        
        Args:
            user_emotion: Current user emotion (positive/negative/neutral)
            user_score: Confidence score
            
        Returns:
            Dictionary with tone adjustment recommendations
        """
        if user_score < 0.6:
            return {
                "adjust": False,
                "recommendation": "maintain neutral tone",
                "reason": "low confidence in emotion detection"
            }
        
        adjustments = {
            "negative": {
                "adjust": True,
                "recommendation": "be more empathetic and supportive",
                "reason": "user appears frustrated or upset"
            },
            "positive": {
                "adjust": True,
                "recommendation": "be enthusiastic and engaging",
                "reason": "user appears happy and excited"
            },
            "neutral": {
                "adjust": False,
                "recommendation": "maintain informative and helpful tone",
                "reason": "user appears calm and factual"
            }
        }
        
        return adjustments.get(user_emotion, adjustments["neutral"])
    
    def get_emotional_adaptation_prompt(self, recent_messages: List[Dict[str, Any]], n_recent: int = 10) -> str:
        """
        Generate detailed emotional adaptation instructions for the system prompt.
        
        This analyzes recent emotional patterns and provides specific guidance on:
        - Current emotional state and trajectory
        - Recommended tone adjustments
        - Communication style suggestions
        - Warning signs to watch for
        
        Args:
            recent_messages: List of recent message dictionaries with metadata
            n_recent: Number of recent messages to analyze (default: 10, increased from 5)
            
        Returns:
            Detailed emotional adaptation instructions for system prompt
        """
        if not recent_messages:
            return ""
        
        # Analyze recent messages
        recent = recent_messages[-n_recent:] if len(recent_messages) > n_recent else recent_messages
        
        user_emotions = []
        bot_emotions = []
        
        for msg in recent:
            metadata = msg.get("metadata", {})
            
            if "user_emotion" in metadata:
                user_emotions.append({
                    "emotion": metadata["user_emotion"],
                    "score": metadata.get("user_emotion_score", 0.0),
                    "timestamp": metadata.get("timestamp", ""),
                    "is_mixed": metadata.get("user_emotion_is_mixed", False)
                })
            
            if "bot_emotion" in metadata:
                bot_emotions.append({
                    "emotion": metadata["bot_emotion"],
                    "score": metadata.get("bot_emotion_score", 0.0)
                })
        
        if not user_emotions:
            return ""
        
        # Analyze patterns
        latest_emotion = user_emotions[-1]
        emotion_type = latest_emotion["emotion"]
        confidence = latest_emotion["score"]
        is_mixed = latest_emotion.get("is_mixed", False)
        
        # Detect emotional trajectory by analyzing last 3 messages from metadata
        # HOW IT WORKS:
        # 1. Gets emotion labels from user_emotions list (extracted from message metadata)
        # 2. Compares first and last emotions in recent window (3 messages)
        # 3. Categorizes emotions as positive (joy, love, optimism, trust, anticipation)
        #    or negative (anger, disgust, fear, sadness, pessimism)
        # 4. Determines trajectory:
        #    - "improving": Started negative → ended positive (e.g., fear → joy)
        #    - "declining": Started positive → ended negative (e.g., joy → sadness)
        #    - "volatile": Changed through 3+ different emotions (e.g., joy → anger → surprise)
        #    - "stable": Stayed in same emotion or category
        trajectory = "stable"
        positive_emotions = ["joy", "love", "optimism", "trust", "anticipation"]
        negative_emotions = ["anger", "disgust", "fear", "sadness", "pessimism"]
        
        if len(user_emotions) >= 3:
            emotions_list = [e["emotion"] for e in user_emotions[-3:]]
            
            # Check if moving from negative to positive
            first_is_negative = emotions_list[0] in negative_emotions
            last_is_positive = emotions_list[-1] in positive_emotions
            first_is_positive = emotions_list[0] in positive_emotions
            last_is_negative = emotions_list[-1] in negative_emotions
            
            if first_is_negative and last_is_positive:
                trajectory = "improving"
            elif first_is_positive and last_is_negative:
                trajectory = "declining"
            elif len(set(emotions_list)) > 2:
                trajectory = "volatile"
        
        # Build adaptation instructions
        instructions = []
        
        instructions.append("EMOTIONAL ADAPTATION GUIDANCE:")
        if is_mixed:
            instructions.append(f"• User's current state: {emotion_type.upper()} with MIXED EMOTIONS (confidence: {confidence:.0%})")
            instructions.append("• ⚠️  MIXED EMOTIONS DETECTED: User expressing conflicting feelings")
        else:
            instructions.append(f"• User's current state: {emotion_type.upper()} (confidence: {confidence:.0%})")
        
        # Show trajectory with actual emotional progression
        if len(user_emotions) >= 3:
            emotions_list = [e["emotion"] for e in user_emotions[-3:]]
            instructions.append(f"• Emotional trajectory: {trajectory.upper()} ({' → '.join(emotions_list)})")
        elif len(user_emotions) >= 2:
            emotions_list = [e["emotion"] for e in user_emotions[-2:]]
            instructions.append(f"• Emotional trajectory: {trajectory.upper()} ({' → '.join(emotions_list)})")
        else:
            instructions.append(f"• Emotional trajectory: {trajectory.upper()}")
        
        # Handle mixed emotions specially
        if is_mixed:
            instructions.append("• PRIORITY: User has complex, mixed feelings - requires nuanced response")
            instructions.append("• Response style: Acknowledge both aspects of their emotions")
            instructions.append("• Tone: Understanding, balanced, non-dismissive")
            instructions.append("• Actions: Validate all feelings, help clarify emotions, offer balanced perspective")
            instructions.append("• Avoid: Oversimplifying, focusing on only one emotion, being too cheerful or pessimistic")
        # Specific recommendations for each of 11 emotions
        elif emotion_type == "joy":
            instructions.append("• User is feeling joyful and happy")
            instructions.append("• Response style: Match their positive energy")
            instructions.append("• Tone: Upbeat, warm, celebratory")
            instructions.append("• Actions: Share in their happiness, build on positive momentum")
        
        elif emotion_type == "love":
            instructions.append("• User is expressing love, affection, or deep appreciation")
            instructions.append("• Response style: Be warm and genuine")
            instructions.append("• Tone: Kind, appreciative, heartfelt")
            instructions.append("• Actions: Acknowledge their feelings, respond with warmth")
        
        elif emotion_type == "optimism":
            instructions.append("• User is feeling optimistic and hopeful")
            instructions.append("• Response style: Support their positive outlook")
            instructions.append("• Tone: Encouraging, forward-looking")
            instructions.append("• Actions: Reinforce their optimism, discuss positive possibilities")
        
        elif emotion_type == "trust":
            instructions.append("• User is showing trust and confidence")
            instructions.append("• Response style: Honor their trust with reliability")
            instructions.append("• Tone: Professional, dependable, honest")
            instructions.append("• Actions: Provide accurate information, be transparent")
        
        elif emotion_type == "anticipation":
            instructions.append("• User is feeling anticipation and excitement")
            instructions.append("• Response style: Match their forward-looking energy")
            instructions.append("• Tone: Engaging, enthusiastic about future")
            instructions.append("• Actions: Help them prepare, discuss what's coming")
        
        elif emotion_type == "anger":
            instructions.append("• PRIORITY: User is feeling angry or frustrated")
            instructions.append("• Response style: Be calm, patient, and understanding")
            instructions.append("• Tone: Measured, empathetic, non-defensive")
            instructions.append("• Actions: Acknowledge their frustration, focus on solutions")
            instructions.append("• Avoid: Being dismissive, defensive, or argumentative")
        
        elif emotion_type == "disgust":
            instructions.append("• User is expressing disgust or strong disapproval")
            instructions.append("• Response style: Validate their concerns without judgment")
            instructions.append("• Tone: Understanding, respectful")
            instructions.append("• Actions: Address the source of disapproval professionally")
        
        elif emotion_type == "fear":
            instructions.append("• PRIORITY: User is feeling afraid or anxious")
            instructions.append("• Response style: Be reassuring and supportive")
            instructions.append("• Tone: Calm, steady, comforting")
            instructions.append("• Actions: Provide clear information, reduce uncertainty")
            instructions.append("• Avoid: Minimizing their concerns or adding worry")
        
        elif emotion_type == "sadness":
            instructions.append("• User is feeling sad or disappointed")
            instructions.append("• Response style: Be empathetic and compassionate")
            instructions.append("• Tone: Gentle, understanding, supportive")
            instructions.append("• Actions: Acknowledge their feelings, offer comfort")
            instructions.append("• Avoid: Being overly cheerful or dismissive")
        
        elif emotion_type == "pessimism":
            instructions.append("• User is feeling pessimistic or discouraged")
            instructions.append("• Response style: Be supportive without toxic positivity")
            instructions.append("• Tone: Understanding, gently encouraging")
            instructions.append("• Actions: Acknowledge difficulties, offer realistic perspective")
        
        elif emotion_type == "surprise":
            instructions.append("• User is feeling surprised or caught off guard")
            instructions.append("• Response style: Help them process the unexpected")
            instructions.append("• Tone: Clear, informative")
            instructions.append("• Actions: Provide context, clarify situation")
        
        # Add trajectory-specific guidance
        if trajectory == "improving":
            instructions.append("• NOTE: User's mood is improving - acknowledge positive progress")
        elif trajectory == "declining":
            instructions.append("• ⚠️  WARNING: User's mood is declining - be extra supportive and patient")
        elif trajectory == "volatile":
            instructions.append("• NOTE: Emotional state is fluctuating - adapt tone carefully")
        
        # Check for concerning patterns
        if len(user_emotions) >= 3:
            recent_3 = user_emotions[-3:]
            negative_count = sum(1 for e in recent_3 if e["emotion"] in negative_emotions)
            if negative_count >= 2:
                instructions.append("• ⚠️  ALERT: Multiple negative emotions detected in recent messages")
                instructions.append("• Consider: Asking if they need different type of help or support")
        
        return "\n".join(instructions)


# Global analyzer instance (lazy loading)
_analyzer_instance: Optional[NLPAnalyzer] = None


def get_analyzer() -> NLPAnalyzer:
    """Get or create global NLP analyzer instance."""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = NLPAnalyzer()
    return _analyzer_instance
