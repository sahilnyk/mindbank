# MindBank

Memory extraction and personality transformation system for AI conversations.

---

## The Problem

AI chatbots treat every conversation like it's the first time. You tell them you're vegetarian → they forget by next message. You mention you work late at night → they don't remember when you ask for schedule advice. You say your cat Luna distracts you → gone from their memory.

Why? Because they don't store context. Each interaction starts from scratch.

---

## My Approach

Built a system that:

**1. Extracts memory from conversations**
- Reads 30+ messages from user
- Pulls out preferences (work style, food habits, communication)
- Identifies emotional patterns (stress, excitement, burnout)
- Captures facts (names, places, dates, allergies)
- Stores everything in structured JSON with confidence scores

**2. Transforms responses with personality**
- Takes generic text
- Applies one of three tones: Calm Mentor / Witty Friend / Therapist
- Shows before/after comparison
- Same content → different vibe

**3. Generates memory-aware responses**
- User asks a question
- System checks extracted memory
- Weaves relevant context into answer
- Applies personality transformation
- Result: personalized response that actually remembers stuff

**Example:**

Memory contains:
- vegetarian + allergic to peanuts
- works best late at night
- has cat named Luna

User asks: "What should I eat for dinner?"

Response:
> "Since you're vegetarian and allergic to peanuts, try chickpea curry or lentil soup. Batch cook on weekends when Luna's napping so you have meals ready for late work nights."

It remembers. It connects dots. It personalizes.

---

## How It Works

```
User loads 30 messages
        ↓
System extracts patterns (regex + spaCy)
        ↓
Stores {preferences, emotions, facts}
        ↓
User asks question
        ↓
System generates base response
        ↓
Applies personality transformation
        ↓
Shows before/after comparison
```

**Three tabs handle this workflow:**

### Tab 1: Memory Extraction
- Load 30 sample messages (or add your own manually)
- Click "Extract Memories"
- System runs regex patterns + spaCy NER
- Displays extracted preferences, emotions, facts
- Each item shows confidence score (85%, 90%, 95%)
- Source tracking: which messages provided which info

### Tab 2: Personality Engine
- Type any text (or use suggestion buttons)
- Pick personality: Calm Mentor / Witty Friend / Therapist
- Click transform
- See original vs transformed side-by-side
- Demonstrates how tone changes while keeping content

### Tab 3: Agent Response
- First extract memory from Tab 1
- Enter your question
- Pick response personality
- System generates base answer using memory context
- Applies personality transformation
- Shows three versions: your question → generic response → personalized response

---

## Folder Structure

```
MindBank/
├── backend/app/
│   ├── extraction.py      # regex patterns + spaCy NER
│   ├── personality.py     # tone transformation strategies
│   ├── llm_client.py      # OpenAI wrapper (inactive)
│   └── validators.py      # JSON schema validation
├── frontend/
│   ├── index.html         # 3-tab interface
│   ├── script.js          # API calls + UI logic
│   ├── style.css          # dark theme
│   └── 30_messages.json   # sample conversation
├── schema/
│   └── memory_schema.json # memory format rules
├── tests/                 # pytest unit tests
└── main.py                # FastAPI server
```

**Why this structure?**

Modularity. Each file = one responsibility.

- Change extraction logic? → edit `extraction.py`
- Add new personality? → edit `personality.py`
- Swap LLM provider? → edit `llm_client.py`
- Update UI? → edit frontend files

Nothing breaks because everything's isolated.

**extraction.py** → 18+ regex patterns catch explicit preferences ("I'm vegetarian", "I work late"). spaCy NER pulls entities (names, places, dates). Confidence scoring weights reliability. Deduplication prevents memory bloat.

**personality.py** → Strategy pattern. Three classes: CalmMentorStrategy, WittyFriendStrategy, TherapistStrategy. Each transforms text differently. Adding new personality = create new strategy class.

**validators.py** → Checks extracted memory matches JSON schema. Makes sure preferences have categories, emotions have patterns, facts have types. Prevents bad data.

**llm_client.py** → OpenAI integration exists but not active (rate limits + API policies). Deterministic mode (regex + spaCy) handles everything currently. Can switch to LLM mode later without touching other code.

**main.py** → FastAPI routes. /extract → memory extraction. /rewrite → personality transform. /generate-response → memory-aware answers. Health checks, error handling, CORS enabled.

---

## Tech Stack

**Backend:**
- FastAPI → async API server
- spaCy → entity recognition (works offline, no GPU needed)
- Regex → pattern matching for preferences
- Python 3.10+

**Frontend:**
- Vanilla JavaScript → no build step, just edit and refresh
- HTML/CSS → single page, 3 tabs
- Dark theme → minimalist design

**Why vanilla JS?** No webpack, no npm build, no framework overhead. Edit code → refresh browser → see changes. Fast development, small bundle.

**Current mode:** Deterministic only (regex + spaCy). OpenAI integration coded but inactive.

---

## Memory Format

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

Three buckets. Confidence scores. Source tracking.

---

## Personality Examples

Input: "I need to have a difficult conversation."

**Calm Mentor:**
> "Here's what I've observed: Direct communication builds trust, even when uncomfortable. Prepare your points but stay flexible. Trust the process - you're on the right path."

**Witty Friend:**
> "Yo, listen up! Direct communication builds trust even when uncomfortable. Prep your points but stay flexible. Most tough convos go better than expected. Trust me on this!"

**Therapist:**
> "I appreciate you opening up. Direct communication builds trust, even when uncomfortable. Prepare your points but stay flexible. How are you taking care of yourself through this?"

Same core advice → three different tones.

---

## Running Locally

```bash
git clone <repo-url>
cd MindBank
pip install -r requirements.txt
python -m spacy download en_core_web_sm

uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000`

---

## Deploying on Render

Free tier works.

Build command:
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

Start command:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Push to GitHub → connect to Render → deploy. Done.

---

## Testing

```bash
pytest tests/ -v
```

Covers extraction accuracy, personality transforms, API validation, error handling.

---

## What Gets Extracted

**Preferences:** vegetarian, works late, hates meetings, prefers async, has pet, introvert/extrovert, coffee person, exercises, reads

**Emotions:** stress, excitement, tiredness, confusion, appreciation

**Facts:** names, places, dates, organizations, allergies

All with confidence scores and source tracking.

---

## Core Concept

Problem: AI forgets context → Solution: extract and store memories

Problem: AI sounds robotic → Solution: personality transformation

Problem: generic responses → Solution: memory-aware generation

MindBank does all three.