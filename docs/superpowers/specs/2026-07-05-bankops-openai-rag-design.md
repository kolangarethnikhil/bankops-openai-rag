# BankOps OpenAI RAG Design

## Goal

Build a no-npm Banking Operations RAG assistant that uses synthetic Indian banking operations KBs derived from public RBI-style regulatory information and can call the OpenAI Responses API from a Python backend.

## Constraints

- No npm or npx.
- No client data, no Broadcom data, no HCLTech confidential content.
- OpenAI API key must stay server-side in `OPENAI_API_KEY`.
- The app must work in offline fallback mode when no API key is configured.
- The KB must be synthetic, but every KB item should include public source URLs and source notes.

## Architecture

- `src/bankops_kb.py` stores synthetic KB records and public source metadata.
- `src/rag_engine.py` retrieves KB records and builds grounded answer prompts.
- `src/openai_client.py` calls the OpenAI Responses API with optional hosted web search.
- `app.py` serves the static UI and `/api/ask`.
- `static/index.html` provides the demo UI.

## Demo Flow

1. User asks an Indian banking operations question.
2. Backend retrieves the top KB snippets.
3. If `OPENAI_API_KEY` exists, backend asks OpenAI to answer only from retrieved KB context.
4. If public web check is enabled, backend asks OpenAI to use hosted web search for public web verification.
5. If no API key exists, backend returns a deterministic fallback answer with citations and trace data.

## Safety Positioning

The product is safe for a hackathon demo because it uses synthetic KBs from public regulatory facts. It does not use real customer records, internal project knowledge, private bank policies, or scraped client data.
