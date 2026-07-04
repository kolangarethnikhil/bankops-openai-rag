# BankOps OpenAI RAG Assistant

No-npm hackathon prototype for a Banking Operations RAG assistant.

It uses synthetic Indian banking operations KBs derived from public RBI regulatory information and answers with Markdown, citations, risk level, and next action. Technical retrieval trace stays in the API payload for FlowProof-style evaluation, but the user UI only shows the answer and source chips. It can call the OpenAI Responses API from the Python backend when `OPENAI_API_KEY` is configured.

## Why this is safe

- No Broadcom data.
- No HCLTech confidential data.
- No real bank customer data.
- No scraped client KBs.
- The included KBs are synthetic summaries with public source URLs.

## Run

```powershell
cd "C:\Hackathon\Banking Operations RAG assistant\bankops-openai-rag"
python app.py
```

Open:

```text
http://127.0.0.1:8787
```

## Enable OpenAI

Create or edit `.env` in the project root:

```text
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
PORT=8787
```

Then run:

```powershell
python app.py
```

The `.env` file is ignored by git, so the real API key does not get committed. If `OPENAI_API_KEY` is not set, the app runs in deterministic offline fallback mode.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Public source basis

- RBI Customer Protection circular on limiting liability for unauthorised electronic banking transactions:
  `https://www.rbi.org.in/commonman/English/Scripts/Notification.aspx?Id=2336`
- RBI Master Direction - Know Your Customer Direction, 2016:
  `https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=11566`

## Demo positioning

This is the target assistant. FlowProof can then evaluate the backend trace separately while the main demo remains a normal chatbot experience.
