# MindBank

Memory-aware AI that actually remembers who you are and responds like a real person, not a search engine.

A production system that extracts user memories from conversations and generates personalized responses with different personality styles. Built to demonstrate how companion AI should work.

---

## What This Actually Does

**The Problem:** Most chatbots forget everything between conversations. They don't remember if you're vegetarian, hate morning meetings, or have a cat named Luna.

**What I Built:** A system that mines your chat history for preferences, emotional patterns, and facts - then uses that context to generate responses that feel like they're from someone who actually knows you.

### Real Example

Let's say the system reads these 30 messages from you:
- "I'm vegetarian and allergic to peanuts"
- "I hate morning meetings that kill my flow"
- "I work best late at night"
- "My cat Luna keeps distracting me"

Now you ask: "What should I eat for dinner?"

**Generic chatbot:**
> "Try pasta or salad for a healthy dinner."

**This system:**
> "Since you're vegetarian and need to avoid peanuts, try a chickpea curry with rice or a lentil soup. Planning meals ahead reduces stress - batch cook on weekends when Luna's napping."

See the difference? It actually remembers your context.

---

## How It's Built

```
mindbank/
├── backend/app/          # Core logic separated by function
│   ├── extraction.py     # Mines memories from conversations
│   ├── personality.py    # Transforms tone (mentor vs friend vs therapist)
│   ├── llm_client.py     # OpenAI integration with smart fallback
│   └── validators.py     # Makes sure data follows the right structure
├── frontend/             # Plain JavaScript, no React/Vue nonsense
│   ├── index.html        # Single page interface
│   ├── script.js         # Handles API calls and UI updates
│   ├── style.css         # Dark theme with minimal design
│   └── 30_messages.json  # Sample conversation for testing
├── schema/               # JSON validation rules
├── tests/                # Unit tests for each piece
└── main.py               # FastAPI server that ties everything together
```

### Why I Structured It This Way

**Modular Backend**

Each file does one thing. If you want to swap the extraction logic from regex patterns to a machine learning model, you only touch `extraction.py`. Same with swapping OpenAI for a local LLM - just change `llm_client.py`.

**Dual-Mode Operation**

```python
if use_llm and llm_available():
    result = llm_client.extract()  # Uses OpenAI
else:
    result = extractor.extract()    # Falls back to regex + spaCy
```

Why both? Because you can demo this without an API key. Also, if OpenAI rate-limits you or goes down, the system keeps working. Plus it's way cheaper for high-volume usage.

**Memory Gets Stored Like This**

```json
{
  "preferences": [
    {"category": "food", "value": "vegetarian", "confidence": 0.95}
  ],
  "emotional_patterns": [
    {"pattern": "stress", "confidence": 0.80}
  ],
  "facts": [
    {"fact_type": "location", "value": "Berlin"}
  ]
}
```

Three types of memory:
- **Preferences** - How you like to work, communicate, what you eat
- **Emotions** - Recurring feelings like stress or appreciation
- **Facts** - Hard data like names, places, dates, allergies

**Personality Engine Uses Strategy Pattern**

```python
class PersonalityEngine:
    personalities = {
        "calm_mentor": CalmMentorStrategy(),
        "witty_friend": WittyFriendStrategy(),
        "therapist": TherapistStrategy()
    }
```

Want to add a sarcastic personality? Just create a new strategy class. The rest of the code doesn't need to change. Each personality is isolated and testable.

---

## Getting It Running

**What you need:**
- Python 3.10 or newer
- pip installed

**Setup:**

```bash
# Clone the repo
git clone <your-repo-url>
cd ta-ai-engineer

# Install dependencies
pip install -r requirements.txt

# Download spaCy's English model
python -m spacy download en_core_web_sm

# Optional: Add OpenAI key for LLM mode
echo "OPENAI_API_KEY=sk-..." > .env
```

**Start the server:**

```bash
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000` in your browser. That's it.

---

## How The System Works

### Step 1: Memory Extraction

```
Your messages → Extractor → Structured memory
                    ↓
    [Regex patterns + spaCy entity recognition]
                    ↓
        {preferences, emotions, facts}
```

The extractor uses two techniques:
- **Regex patterns** catch explicit statements like "I'm vegetarian"
- **spaCy NER** pulls out entities - names, places, dates, organizations
- Everything gets a confidence score so you know how reliable it is
- Duplicates are automatically removed

### Step 2: Response Generation

```
Your question + Memory → Base response
                             ↓
                    [Detects what you're asking about]
                             ↓
                    Tailored advice
```

Here's the flow:

```python
# You ask: "Should I work tonight?"
# Memory has: {"work_style": "late night"}

# System detects this is about work
if "work" in question:
    context = extract_work_preferences(memory)
    response = work_advice_template + context

# Output includes your preference:
"Given that you work best late at night, 
tackle it tonight when you're most productive."
```

### Step 3: Personality Transform

```
Base response → Personality strategy → Final output
                        ↓
            [Calm Mentor / Witty Friend / Therapist]
```

Same content, three different tones:

| Personality | What It Does |
|-------------|--------------|
| **Calm Mentor** | Adds wisdom framing and patience reminders |
| **Witty Friend** | Casual language with humor |
| **Therapist** | Validation phrases and reflective questions |

---

## Why Plain JavaScript?

No React, no Vue, no build step. Just vanilla JS. Here's why:

- **Instant changes** - Edit the code and refresh. No waiting for webpack.
- **Fast deployment** - No complicated build configs to debug.
- **Total control** - No framework telling you how to structure things.
- **Tiny bundle** - Loads in under 100ms.

The UI uses a dark theme with a monospace font (Cascadia Code). Minimal colors, clear hierarchy. Gets out of your way so you can focus on the functionality.

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Test just extraction
pytest tests/test_extraction.py -v

# Check coverage
pytest --cov=backend tests/
```

What's covered:
- Memory extraction accuracy
- Personality transformations work correctly
- API endpoints return proper responses
- Schema validation catches bad data
- LLM fallback triggers when it should

---

## API Endpoints

### Extract Memories

`POST /extract`

Send conversation history, get structured memory back.

**Request:**
```json
{
  "messages": [
    {"index": 0, "role": "user", "content": "I prefer async work"}
  ],
  "use_llm": false
}
```

**Response:**
```json
{
  "success": true,
  "memory": {
    "preferences": [...],
    "emotional_patterns": [...],
    "facts": [...]
  },
  "method": "deterministic"
}
```

### Generate Response

`POST /generate-response`

Ask a question, get a memory-aware answer with personality.

**Request:**
```json
{
  "memory": {...},
  "user_message": "Should I work tonight?",
  "personality": "calm_mentor",
  "use_llm": false
}
```

**Response:**
```json
{
  "base_response": "Structure your work around...",
  "personalized_response": "Let me share... [mentor tone]",
  "personality": "calm_mentor",
  "method": "deterministic"
}
```

### Rewrite Text

`POST /rewrite`

Transform any text with a personality style.

**Request:**
```json
{
  "text": "You should take a break",
  "personality": "witty_friend",
  "use_llm": false
}
```

---

## What It Can Do

**Memory Extraction:**
- 18+ preference patterns for work style, food, communication
- 7 emotional keywords like stress, excitement, confusion
- Named entity recognition for people, places, dates
- Confidence scores from 0.0 to 1.0
- Source tracking so you know which messages gave which info

**Personality Engine:**
- 3 distinct personalities with unique tones
- Topic-aware responses for work, food, health, social situations
- Weaves memory context naturally into answers
- 3-4 response templates per topic for variety
- Works with or without LLM

**Production Features:**
- Proper error handling with graceful fallbacks
- Input validation using Pydantic
- Logging to debug LLM vs deterministic modes
- Health check endpoints for monitoring
- CORS enabled for flexible frontend setup

---

## Configuration

**Environment variables:**

```bash
# Optional - turns on LLM mode
OPENAI_API_KEY=sk-proj-...

# Optional - change server port
PORT=8000
```

**Adding new patterns:**

Want to detect coffee addiction?

```python
# In backend/app/extraction.py
self.patterns["coffee_addict"] = re.compile(
    r"\b(need coffee|coffee first)\b", re.IGNORECASE
)
```

**Adding new personalities:**

Want a sarcastic mode?

```python
# In backend/app/personality.py
class SarcasticStrategy(RewriteStrategy):
    def rewrite(self, text):
        return f"Oh sure, {text.lower()}. That'll work out great."
```

---

## Deploying This

**On Render (easiest):**

Build command:
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

Start command:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**On Railway:**

```bash
railway init
railway up
```

**With Docker:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && python -m spacy download en_core_web_sm
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## What You Can Learn From This

If you're studying the code, pay attention to:

1. **Memory as state** - How extracted context changes what the system says
2. **Strategy pattern** - Swappable personality implementations
3. **Graceful degradation** - LLM fails, system keeps working
4. **Structured extraction** - Combining regex with NER
5. **Clean API design** - Clear contracts between frontend and backend

This demonstrates:
- Building companion AI systems
- Managing conversation state
- Personality-driven responses
- Production-ready Python architecture
- Frontend-backend integration without frameworks

---

## Example Outputs

**Memory extraction from 30 messages:**

```
Preferences (8)
├─ [work_style] works late (85%)
├─ [work_style] hates meetings (85%)
├─ [communication] prefer text (85%)
├─ [food] vegetarian (95%)
└─ [lifestyle] has cat named Luna (90%)

Emotional Patterns (5)
├─ stress (80%)
├─ appreciation (80%)
└─ overthinking (80%)

Facts (12)
├─ [location] Berlin (88%)
├─ [date] March 15 (88%)
├─ [person] Max (88%)
└─ [health] allergic to peanuts (88%)
```

**Same input, three personalities:**

Input: "I need to have a difficult conversation with someone."

**Calm Mentor:**
> "Here's what I've observed: Direct communication builds trust, even when it's uncomfortable. Prepare your main points beforehand, but stay flexible in the moment. Most difficult conversations go better than we anticipate. Trust the process - you're on the right path."

**Witty Friend:**
> "Yo, listen up! Direct communication builds trust, even when it's uncomfortable. Prepare your main points beforehand, but stay flexible in the moment. Most difficult conversations go better than we anticipate. Trust me on this one!"

**Therapist:**
> "I appreciate you opening up about this. Direct communication builds trust, even when it's uncomfortable. Prepare your main points beforehand, but stay flexible in the moment. Most difficult conversations go better than we anticipate. How are you taking care of yourself through this?"

---

## Future Ideas

Not accepting contributions since this is a technical assessment, but here are directions you could take it:

- Vector database for semantic memory search
- Multi-user support with isolated memory stores
- Voice input and output
- Memory decay where older memories fade
- Conflict resolution when preferences contradict

---

## The Philosophy

The best AI doesn't try to sound smart. It tries to sound like someone who actually knows you.

This project is about memory plus personality equals natural interaction. Instead of treating every conversation as new, we build context over time. Instead of one robotic tone, we adapt to what you need in that moment.

The result? Responses that feel less like talking to a search engine and more like texting a friend who remembers what you told them last week.

---

Built as a technical demonstration of companion AI principles.

"Making AI that remembers you're vegetarian beats making AI that knows every fact about vegetables"