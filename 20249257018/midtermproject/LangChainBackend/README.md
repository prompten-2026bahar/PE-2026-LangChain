# Swift Analysis Backend

## Run

```bash
cd /Users/ahmetbugraozcan/Desktop/langchain/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export LLM_PROVIDER=gemini
export GOOGLE_API_KEY=your_key
uvicorn app.main:app --reload
```

## Provider Selection

Choose the active model provider in `backend/.env`:

```env
LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b
LLM_TIMEOUT_SECONDS=240
LLM_MAX_RETRIES=3
GROQ_API_KEY=your_groq_key
```

or:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
LLM_TIMEOUT_SECONDS=240
LLM_MAX_RETRIES=3
GOOGLE_API_KEY=your_gemini_key
```

## Endpoints

- `POST /analyze`: Stateless clean code review that returns structured JSON.
- `POST /self-heal`: Runs up to 3 self-healing build attempts and returns the final code.
- `WS /ws/self-heal`: Streams thought and observation events for the SwiftUI dashboard.
