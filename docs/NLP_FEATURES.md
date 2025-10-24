# 🧠 AI Brain NLP Features

## Enhanced Memory with NLP Analysis

The AI Brain now includes sophisticated NLP analysis using **spaCy** and **RoBERTa** to enrich every conversation with semantic metadata and emotional context tracking.

## 🔬 NLP Capabilities

### 1. **Named Entity Recognition (NER)**
Automatically extracts and categorizes entities:
- **PERSON**: Names of people (e.g., "Mark", "John Smith")
- **ORG**: Organizations (e.g., "Apple", "Google")
- **GPE**: Geopolitical entities (e.g., "California", "New York")
- **DATE**: Temporal expressions (e.g., "yesterday", "three days")
- **PRODUCT**: Products mentioned
- And more...

### 2. **Sentiment Analysis (RoBERTa)**
Uses Twitter-tuned RoBERTa for accurate sentiment detection:
- **Positive**: Happy, excited, satisfied expressions
- **Negative**: Frustrated, sad, angry expressions  
- **Neutral**: Factual, informational statements
- **Confidence Score**: 0-100% accuracy

### 3. **Emotional Context Tracking** 🎭 **NEW**
Tracks emotional state throughout conversations:
- **User Emotions**: Separate tracking of user sentiment (`user_emotion`, `user_emotion_score`)
- **Bot Emotions**: Tracks assistant's tone (`bot_emotion`, `bot_emotion_score`)
- **Emotional Trajectory**: Analyzes how emotions shift over time
- **Context-Aware Prompts**: Includes emotional state in LLM prompts
- **Tone Adjustment**: Recommends response tone based on user emotion

**Example Emotional Context in Prompts:**
```
EMOTIONAL CONTEXT:
User's recent emotional state: negative (confidence: 94%)
Your recent tone: neutral (confidence: 50%)
User emotions have shifted: positive → negative → negative
```

### 4. **Keyword Extraction**
Identifies most important words using:
- Part-of-speech tagging
- Lemmatization
- Stop word filtering
- Frequency analysis

### 5. **Topic Identification**
Discovers conversation themes through:
- Noun chunk analysis
- Entity clustering
- Semantic grouping

### 6. **Intent Detection**
Classifies user intent:
- **Question**: Information seeking
- **Statement**: Factual declarations
- **Command**: Action requests
- **Expression**: Emotional statements

### 7. **Linguistic Features**
Analyzes text structure:
- POS distribution
- Question detection
- Negation presence
- Average word length

## 📊 Metadata Enrichment

Every message is automatically tagged with:

```python
{
    # Sentiment & Emotion (role-specific)
    "user_emotion": "positive",        # For user messages
    "user_emotion_score": 0.99,
    "bot_emotion": "neutral",          # For assistant messages
    "bot_emotion_score": 0.50,
    
    # Intent
    "intent": "question",
    
    # Content analysis
    "keywords": "ai, machine, learning, python",
    "topics": "artificial intelligence, data science",
    "entity_count": 3,
    "entities_person": "Mark, Sarah",
    "entities_org": "Apple, Google",
    
    # Structure
    "word_count": 42,
    "sentence_count": 3,
    "has_question": true,
    "has_negation": false,
    
    # Standard
    "role": "user",
    "timestamp": "2025-10-24T..."
}
```

## 🎯 Benefits

### **Better Memory Retrieval**
- Find messages by sentiment: "Show me frustrated conversations"
- Filter by entities: "What did I say about Apple?"
- Search by intent: "Find all my questions"

### **Context-Aware Responses**
- AI adapts tone based on your sentiment
- References past topics and entities naturally
- Understands follow-up questions better
- Responds empathetically to user emotions

### **Emotional Intelligence** 🎭 **NEW**
- Tracks user emotional journey throughout conversations
- Detects emotional shifts (e.g., excitement → frustration)
- Adjusts response tone based on detected emotions
- Provides emotional context to LLM for empathetic responses

### **Advanced Analytics**
- Track sentiment trends over time
- Analyze conversation patterns
- Identify recurring topics
- Measure engagement
- Monitor emotional trajectory

## 🚀 Usage

### Automatic Enrichment (Default)
```python
# NLP analysis happens automatically
memory.add_memory(
    content="I love working with AI!",
    memory_type="conversation",
    enable_nlp=True  # Default
)
```

### Query by Metadata
```python
# Find all positive messages
memories = memory.retrieve_memories(
    query="happy moments",
    memory_type="conversation",
    sentiment="positive"
)

# Find questions about Python
memories = memory.retrieve_memories(
    query="Python programming",
    intent="question"
)
```

### Analyze Any Text
```python
from ai_brain.nlp_analyzer import NLPAnalyzer

analyzer = NLPAnalyzer()
analysis = analyzer.analyze_text("Your text here")

print(f"Sentiment: {analysis['sentiment']['label']}")
print(f"Keywords: {analysis['keywords']}")
print(f"Entities: {analysis['entities']}")
```

### Access Emotional Context 🎭 **NEW**
```python
from ai_brain.memory import MemoryStore
from ai_brain.nlp_analyzer import get_analyzer

memory = MemoryStore()
analyzer = get_analyzer()

# Get recent conversation history
history = memory.get_conversation_history(n_recent=10)

# Generate emotional context summary
emotional_context = analyzer.get_emotional_context_summary(history)
print(emotional_context)
# Output: "User's recent emotional state: negative (confidence: 94%)
#          Your recent tone: neutral (confidence: 50%)
#          User emotions have shifted: positive → negative → negative"

# Check if tone adjustment is needed
should_adjust, suggestion = analyzer.should_adjust_tone("negative", 0.94)
if should_adjust:
    print(f"Recommendation: {suggestion}")
    # Output: "User is experiencing negative emotions. Consider being more supportive..."
```

## 🎭 Emotional Context in Action

### How It Works

1. **Message Analysis**: Every user and bot message is analyzed for sentiment
2. **Separate Tracking**: User emotions and bot tone are tracked independently
3. **Storage**: Emotions stored as `user_emotion`/`bot_emotion` with confidence scores
4. **Context Building**: Recent emotional history is summarized before generating responses
5. **Prompt Enhancement**: Emotional context is included in LLM prompts

### Example Flow

```python
# User sends message
user_message = "I'm really frustrated with this bug!"

# System analyzes emotion
# Result: negative (confidence: 94%)

# Message stored with metadata
memory.add_memory(
    content=user_message,
    metadata={
        "role": "user",
        "user_emotion": "negative",
        "user_emotion_score": 0.94,
        ...
    },
    enable_nlp=True
)

# Before generating response, retrieve emotional context
history = memory.get_conversation_history(n_recent=10)
emotional_summary = analyzer.get_emotional_context_summary(history)

# LLM receives prompt with emotional context:
# """
# EMOTIONAL CONTEXT:
# User's recent emotional state: negative (confidence: 94%)
# User emotions have shifted: neutral → positive → negative
# 
# User message: I'm really frustrated with this bug!
# """

# Bot responds empathetically
bot_response = "I understand your frustration. Let's debug this together..."

# Bot response is also analyzed
# Result: neutral (confidence: 51%)

# Both are stored for future context
```

## 🧪 Testing

Run the NLP test suite:
```bash
python test_nlp.py
```

This demonstrates:
- Sentiment detection on various inputs
- Entity extraction examples
- Keyword identification
- Intent classification
- Metadata generation

Test emotional tracking:
```bash
python test_emotional_tracking.py
```

Test full integration:
```bash
python test_full_emotional_integration.py
```

## ⚙️ Configuration

### spaCy Models

**Small** (Default): `en_core_web_sm`
- Fast, 12MB
- Good for general use

**Medium**: `en_core_web_md`
- Better accuracy
- Includes word vectors

**Large**: `en_core_web_lg`
- Best accuracy
- 540MB, slower

Install larger models:
```bash
python -m spacy download en_core_web_md
```
```

### Analyze Any Text
```python
from ai_brain.nlp_analyzer import NLPAnalyzer

analyzer = NLPAnalyzer()
analysis = analyzer.analyze_text("Your text here")

print(f"Sentiment: {analysis['sentiment']['label']}")
print(f"Keywords: {analysis['keywords']}")
print(f"Entities: {analysis['entities']}")
```

## 🧪 Testing

Run the NLP test suite:
```bash
python test_nlp.py
```

This demonstrates:
- Sentiment detection on various inputs
- Entity extraction examples
- Keyword identification
- Intent classification
- Metadata generation

## ⚙️ Configuration

### spaCy Models

**Small** (Default): `en_core_web_sm`
- Fast, 12MB
- Good for general use

**Medium**: `en_core_web_md`
- Better accuracy
- Includes word vectors

**Large**: `en_core_web_lg`
- Best accuracy
- 540MB, slower

Install larger models:
```bash
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg
```

### Sentiment Model

Uses `cardiffnlp/twitter-roberta-base-sentiment-latest`:
- Trained on 124M tweets
- Optimized for conversational text
- Runs on M4 GPU automatically

## 🎨 Advanced Use Cases

### 1. **Mood Tracking**
```python
# Find how sentiment changed over time
recent_messages = memory.get_conversation_history(n_recent=50)
sentiments = [msg['metadata']['sentiment'] for msg in recent_messages]
```

### 2. **Entity Relationship Mapping**
```python
# Find all conversations mentioning specific entities
apple_convos = [
    m for m in memories 
    if 'entities_org' in m['metadata'] 
    and 'Apple' in m['metadata']['entities_org']
]
```

### 3. **Question Answering History**
```python
# Find all unanswered questions
questions = [
    m for m in memories
    if m['metadata'].get('intent') == 'question'
]
```

### 4. **Topic Clustering**
```python
# Group conversations by topics
from collections import Counter
topics = []
for m in memories:
    if 'topics' in m['metadata']:
        topics.extend(m['metadata']['topics'].split(', '))

topic_freq = Counter(topics)
print("Most discussed topics:", topic_freq.most_common(10))
```

## 🔧 Performance

On M4 Pro:
- **spaCy NER**: ~10-20ms per message
- **RoBERTa Sentiment**: ~50-100ms per message (GPU)
- **Total Enrichment**: ~100-150ms per message

Memory overhead: ~200MB (models loaded once)

## 📚 Technical Details

### Pipeline Architecture
```
User Input
    ↓
spaCy Processing
    ├─ Tokenization
    ├─ POS Tagging
    ├─ Dependency Parsing
    ├─ NER
    └─ Noun Chunking
    ↓
RoBERTa Sentiment
    └─ Classification
    ↓
Metadata Creation
    ↓
Vector Embedding
    ↓
ChromaDB Storage
```

### Dependencies
- `spacy>=3.7.0`: Core NLP
- `transformers>=4.30.0`: RoBERTa
- `torch>=2.0.0`: ML backend

## 🐛 Troubleshooting

**Issue**: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

**Issue**: Slow sentiment analysis
- Check GPU is being used (MPS on M4)
- Reduce batch size if memory limited

**Issue**: Too much metadata
- Disable NLP: `enable_nlp=False`
- Or filter specific fields

## 🎓 Learn More

- [spaCy Documentation](https://spacy.io)
- [RoBERTa Paper](https://arxiv.org/abs/1907.11692)
- [Named Entity Recognition Guide](https://spacy.io/usage/linguistic-features#named-entities)
