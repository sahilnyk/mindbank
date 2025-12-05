# MindBank

Extracts memories from conversations and rewrites responses with different personalities.

---

## The Classic Problem

Ever notice how AI chatbots forget everything you tell them? You mention you're vegetarian on Monday → they suggest steak recipes on Tuesday. You say you hate morning meetings → they schedule 9am calls. You tell them about your cat Luna → they act like they never heard of her.

Why? Because they don't have memory. Every conversation starts from zero.

---

## The Solution → MindBank

Instead of forgetting everything, this system:

1. **Reads your chat history** (30 messages)
2. **Extracts what matters** (preferences, emotions, facts)
3. **Stores it in structured format** (JSON with confidence scores)
4. **Uses that context** when generating responses
5. **Transforms tone** based on personality you pick

**Example flow:**

Messages contain:
- "I'm vegetarian and allergic to peanuts"
- "I work best late at night"
- "My cat Luna keeps distracting me"

You ask: "What should I eat for dinner?"

System response:
> "Since you're vegetarian and allergic to peanuts, try chickpea curry or lentil soup. Batch cook on weekends when Luna's napping."

It actually remembers your context.

---

## Tech Stack

**Backend:**
- FastAPI → handles API requests
- spaCy → extracts entities (names, places, dates)
- Regex patterns → catches explicit preferences
- Python 3.10+ → everything runs on this

**Frontend:**
- Vanilla JavaScript → no framework, just raw JS
- HTML/CSS → single page with 3 tabs
- Dark theme → easier on the eyes

**Why no React/Vue?** Because edit → refresh is faster than edit → build → refresh. Also smaller bundle size.

**Note:** OpenAI integration exists but not active right now (rate limits + API policy stuff). Deterministic mode (regex + spaCy) works fine though.

---

## How It Works

```
Step 1: Load 30 messages
        ↓
Step 2: Extract patterns (regex + spaCy NER)
        ↓
Step 3: Store as {preferences, emotions, facts}
        ↓
Step 4: User asks a question
        ↓
Step 5: Generate base response (topic-aware)
        ↓
Step 6: Apply personality transformation
        ↓
Step 7: Show before/after comparison
```

---

## The Three Tabs

**Tab 1: Memory Extraction**
- Load 30 sample messages (or add your own)
- Click "Extract Memories"
- See preferences, emotions, and facts pulled out
- Each item has confidence score (0-100%)

**Tab 2: Personality Engine**
- Type any text (or use suggestions)
- Pick a personality: Calm Mentor / Witty Friend / Therapist
- See how the same text transforms with different tones
- Shows original → transformed side-by-side

**Tab 3: Agent Response**
- Ask a question
- System uses extracted memory to personalize answer
- Pick personality for the response
- See before/after: generic version → personalized version

---

## Folder Structure

```
MindBank/
├── backend/app/
│   ├── extraction.py      # regex + spaCy memory mining
│   ├── personality.py     # tone transformation logic
│   ├── llm_client.py      # OpenAI wrapper (not used currently)
│   └── validators.py      # checks JSON structure
├── frontend/
│   ├── index.html         # 3-tab interface
│   ├── script.js          # handles clicks + API calls
│   ├── style.css          # dark theme styling
│   └── 30_messages.json   # sample conversation data
├── schema/
│   └── memory_schema.json # defines valid memory format
├── tests/                 # pytest unit tests
└── main.py                # FastAPI server + routes
```

**Why this structure?**

Each file = one job. Want to change extraction logic? → edit `extraction.py`. Add a new personality? → edit `personality.py`. Swap LLM provider later? → edit `llm_client.py`. Nothing else breaks.

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

Three buckets:
- **Preferences** → work style, food habits, communication style
- **Emotions** → recurring feelings (stress, excitement, etc.)
- **Facts** → hard data (names, places, dates, allergies)

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

Same info → three different vibes.

---

## What Gets Extracted

**Preferences (18+ patterns):**
- vegetarian, vegan, plant-based
- works late, early bird
- hates meetings, prefers async
- allergic to X
- has cat/dog named Y
- introvert/extrovert
- coffee/tea person
- exercise habits
- reading preferences
- remote work, work from home

**Emotions (7 keywords):**
- stress, anxious, overwhelmed
- excited, happy
- tired, burned out
- confused, uncertain
- appreciation, grateful

**Facts (via spaCy):**
- Names (people, pets)
- Places (cities, countries)
- Dates (March 15, next week)
- Organizations (companies)
- Products (brands, apps)

---

## Running Locally

```bash
git clone <your-repo>
cd MindBank
pip install -r requirements.txt
python -m spacy download en_core_web_sm

uvicorn main:app --reload --port 8000
```

Open → `http://localhost:8000`

---

## API Endpoints

**POST /extract**
Send messages → get structured memory

**POST /rewrite**
Send text + personality → get transformed version

**POST /generate-response**
Send memory + question + personality → get personalized answer

Check the code for exact request/response formats.

---

## Deploying (Render Free Tier)

1. Push code to GitHub
2. Connect repo to Render
3. Set build command:
```bash
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```
4. Set start command:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```
5. Deploy

Done. No complicated configs.

---

## Testing

```bash
pytest tests/ -v
```

Tests cover:
- Memory extraction accuracy
- Personality transformations
- API response validation
- Error handling
- Fallback behavior

---

## Technical Details

**FastAPI** → fast, has auto docs, async support

**Vanilla JS** → no build step, edit and refresh instantly

**spaCy** → entity recognition without GPU, works offline

**Regex patterns** → catch explicit statements ("I'm vegetarian")

**Strategy pattern** → each personality is isolated, easy to add new ones

**Dual mode** → works without OpenAI (deterministic), can switch to LLM later

---

## The Core Idea

Problem: AI forgets everything → Solution: extract and store memories

Problem: AI sounds robotic → Solution: personality transformation

Problem: responses feel generic → Solution: use memory context

This system does all three.