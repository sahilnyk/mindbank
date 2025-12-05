# MindBank

AI that actually remembers stuff about you and responds like a human, not a robot.

---

## The Problem

Chatbots forget everything. You tell them you're vegetarian on Monday, they suggest steak on Tuesday. Annoying.

## What I Built

This system reads your chat history, extracts what matters (your preferences, emotions, facts), and uses that to give responses that actually make sense for YOU.

**Quick example:**

You mention in chats:
- "I'm vegetarian and allergic to peanuts"
- "I work best late at night"
- "My cat Luna keeps distracting me"

You ask: "What should I eat for dinner?"

**Normal chatbot:** "Try pasta or salad."

**This thing:** "Since you're vegetarian and allergic to peanuts, try chickpea curry or lentil soup. Batch cook on weekends when Luna's napping."

It actually remembers your context.

---

## How It Works

```
Step 1: Memory Extraction
User messages → Extract patterns → Store as structured data
                     ↓
          [Regex + spaCy NER]
                     ↓
     {preferences, emotions, facts}

Step 2: Generate Response  
User question → Match topic → Pull relevant memory → Generate answer
                     ↓
          [Work? Food? Social?]
                     ↓
          Context-aware response

Step 3: Add Personality
Base response → Apply personality style → Final output
                     ↓
          [Mentor / Friend / Therapist]
                     ↓
          Same info, different vibe
```

---

## Project Structure

```
ta-ai-engineer/
├── backend/app/
│   ├── extraction.py      # pulls memories from messages
│   ├── personality.py     # changes tone (mentor/friend/therapist)
│   ├── llm_client.py      # OpenAI wrapper with fallback
│   └── validators.py      # checks data structure
├── frontend/
│   ├── index.html         # the UI
│   ├── script.js          # handles clicks and API calls
│   ├── style.css          # dark theme
│   └── 30_messages.json   # sample data for testing
├── schema/
│   └── memory_schema.json # defines what valid memory looks like
├── tests/                 # unit tests
└── main.py                # FastAPI server
```

**Why this structure?**

Each file does ONE thing. Want to swap OpenAI for Claude? Just edit `llm_client.py`. Want to add a new personality? Just edit `personality.py`. Nothing breaks because everything's separated.

**Two modes:**
- **With OpenAI key:** Uses GPT for smart extraction
- **Without key:** Falls back to regex + spaCy (still works, just less smart)

This way you can demo it without spending money on API calls.

---

## Running It

```bash
# clone and install
git clone <repo-url>
cd ta-ai-engineer
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# optional: add OpenAI key
echo "OPENAI_API_KEY=sk-..." > .env

# run
uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000` and you're good.

---

## Memory Structure

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

Three buckets:
- **Preferences** - work style, food habits, communication preferences
- **Emotions** - recurring feelings like stress, excitement
- **Facts** - names, places, dates, allergies

---

## The Personalities

Same content, different vibes:

**Input:** "I need to have a difficult conversation."

**Calm Mentor:**
> "Direct communication builds trust, even when uncomfortable. Prepare your points but stay flexible. Most difficult conversations go better than we think. Trust the process."

**Witty Friend:**  
> "Yo, direct communication builds trust even when it's uncomfortable. Prep your points but stay flexible. Most tough convos go better than expected. Trust me on this!"

**Therapist:**
> "Thank you for sharing this. Direct communication builds trust, even when uncomfortable. Prepare your points but stay flexible. Most difficult conversations go better than we anticipate. How are you taking care of yourself through this?"

---

## API Endpoints

**POST /extract** - Extract memories from messages
**POST /generate-response** - Get personalized answer
**POST /rewrite** - Transform text with personality

Check the code for request/response examples.

---

## Tech Choices

**Why FastAPI?** Fast, async, automatic docs.

**Why vanilla JS?** No build step. Edit and refresh. Done.

**Why spaCy?** Good NER without needing GPU or cloud.

**Why dual-mode?** Works without API keys. Cheaper. More reliable.

---

## What It Can Extract

- 18+ preference patterns (vegetarian, works late, hates meetings, etc.)
- 7 emotional keywords (stress, excited, tired, etc.)
- Named entities (people, places, dates, organizations)
- Confidence scores for everything
- Source tracking (which message said what)

---

## Deploy

**Render:**
```bash
# Build: pip install -r requirements.txt && python -m spacy download en_core_web_sm
# Start: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Railway:**
```bash
railway init && railway up
```

**Docker:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt && python -m spacy download en_core_web_sm
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Testing

```bash
pytest tests/ -v
```

Tests cover extraction accuracy, personality transforms, API responses, and fallback behavior.

---

## The Point

Most AI tries to sound smart. This one tries to sound like someone who actually knows you.

Memory + personality = natural conversation.

Built as a technical assessment to show how companion AI should work.