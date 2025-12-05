# MindBank

Extracts memories from chat history and transforms responses with different personalities. That's it.

---

## What This Actually Does

Takes 30 messages, pulls out:
- Preferences (work style, food habits, communication)
- Emotions (stress, excitement, whatever you're feeling)
- Facts (names, places, dates, allergies)

Then takes any response and rewrites it in 3 different tones.

**Example:**

Messages say:
- "I'm vegetarian and allergic to peanuts"
- "I work best late at night"
- "My cat Luna keeps distracting me"

You ask: "What should I eat for dinner?"

System knows your context and says:
> "Since you're vegetarian and allergic to peanuts, try chickpea curry or lentil soup. Batch cook on weekends when Luna's napping."

---

## How It Works

```
1. Load 30 messages
        ↓
2. Run extraction (regex + spaCy)
        ↓
3. Get {preferences, emotions, facts}
        ↓
4. Ask a question
        ↓
5. System generates base response
        ↓
6. Pick a personality (mentor/friend/therapist)
        ↓
7. See before/after transformation
```

**Only deterministic mode works right now** - no OpenAI integration because of rate limits and API policy issues. But that's fine, regex + spaCy does the job.

---

## Folder Setup

```
ta-ai-engineer/
├── backend/app/
│   ├── extraction.py      # mines memories with regex + spaCy
│   ├── personality.py     # transforms text tone
│   ├── llm_client.py      # OpenAI wrapper (not used currently)
│   └── validators.py      # JSON structure checks
├── frontend/
│   ├── index.html         # 3-tab UI
│   ├── script.js          # handles API calls
│   ├── style.css          # dark theme
│   └── 30_messages.json   # sample messages
├── schema/
│   └── memory_schema.json # memory format definition
├── tests/                 # pytest tests
└── main.py                # FastAPI server
```

**Why split it like this?**

Change extraction logic? Edit one file. Add a personality? Edit one file. Swap the LLM provider later? Edit one file. Nothing breaks.

---

## Running Locally

```bash
git clone <repo>
cd ta-ai-engineer
pip install -r requirements.txt
python -m spacy download en_core_web_sm

uvicorn main:app --reload --port 8000
```

Go to `http://localhost:8000`

Three tabs:
1. Memory Extraction - Load messages, see what it pulls out
2. Personality Engine - Type text, see 3 transformations
3. Agent Response - Ask questions, get personalized answers

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

Confidence scores tell you how reliable each extraction is.

---

## Personality Examples

Input: "I need to have a difficult conversation."

**Calm Mentor:**
> "Here's what I've observed: Direct communication builds trust, even when uncomfortable. Prepare your points but stay flexible. Trust the process - you're on the right path."

**Witty Friend:**  
> "Yo, listen up! Direct communication builds trust even when uncomfortable. Prep your points but stay flexible. Most tough convos go better than expected. Trust me on this!"

**Therapist:**
> "I appreciate you opening up. Direct communication builds trust, even when uncomfortable. Prepare your points but stay flexible. How are you taking care of yourself through this?"

Same content, different energy.

---

## What Gets Extracted

Patterns it catches:
- vegetarian, vegan, plant-based
- works late, early bird
- hates meetings, prefers async
- allergic to X
- has cat/dog named Y
- introvert/extrovert
- coffee/tea lover
- exercise habits
- reading preferences

Emotions:
- stress, anxious, overwhelmed
- excited, happy
- tired, burned out
- confused, uncertain

Plus spaCy pulls out names, places, dates, organizations.

---

## APIs

**POST /extract**  
Send messages, get structured memory back.

**POST /rewrite**  
Send text + personality, get transformed version.

**POST /generate-response**  
Send memory + question + personality, get personalized answer.

Look at the code for exact request/response formats.

---

## Deploying on Render

Free tier works fine.

**Build command:**
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

**Start command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

That's it. Push to GitHub, connect to Render, done.

---

## Testing

```bash
pytest tests/ -v
```

Tests memory extraction accuracy, personality transformations, API responses, and error handling.

---

## Technical Notes

Uses FastAPI because it's fast and has auto docs.

Uses vanilla JS because no build step means I can edit and refresh instantly.

Uses spaCy for entity recognition - works offline, doesn't need GPU.

Regex patterns handle explicit preferences, spaCy catches entities, confidence scores tell you what's reliable.

Strategy pattern for personalities means adding new ones is just creating a new class.

---

## The Point

Assignment was: extract memories from 30 messages, transform response tones, show before/after.

This does exactly that. Plus it uses the extracted memory to personalize responses based on context.

Built as a technical assessment.