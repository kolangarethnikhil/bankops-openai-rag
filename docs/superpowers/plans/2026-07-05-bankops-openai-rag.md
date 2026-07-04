# BankOps OpenAI RAG Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local no-npm Python + static HTML BankOps RAG assistant with synthetic public-source Indian banking KBs and server-side OpenAI API support.

**Architecture:** A small Python HTTP server owns API-key handling, retrieval, prompt construction, OpenAI calls, and static file serving. The frontend is a single static dashboard that calls `/api/ask`.

**Tech Stack:** Python standard library, `unittest`, HTML/CSS/JavaScript, OpenAI Responses API over HTTPS via `urllib.request`.

## Global Constraints

- No npm or npx.
- No confidential client, HCLTech, Broadcom, or real bank customer data.
- `OPENAI_API_KEY` is read only by Python backend.
- App must run without third-party Python packages.
- Offline fallback must work without an API key.

---

### Task 1: Retrieval Engine

**Files:**
- Create: `src/bankops_kb.py`
- Create: `src/rag_engine.py`
- Test: `tests/test_rag_engine.py`

**Interfaces:**
- Produces: `get_kb() -> list[dict]`
- Produces: `retrieve(question: str, top_k: int = 4) -> list[dict]`
- Produces: `build_prompt(question: str, passages: list[dict], use_public_web: bool) -> str`
- Produces: `offline_answer(question: str, passages: list[dict]) -> dict`

- [ ] Write failing retrieval tests.
- [ ] Run `python -m unittest tests.test_rag_engine -v` and verify module import failure.
- [ ] Implement KB and retrieval.
- [ ] Run retrieval tests and verify pass.

### Task 2: OpenAI Client

**Files:**
- Create: `src/openai_client.py`
- Test: `tests/test_openai_client.py`

**Interfaces:**
- Produces: `OpenAIConfig`
- Produces: `build_responses_payload(prompt: str, model: str, use_web: bool) -> dict`
- Produces: `extract_text(response: dict) -> str`

- [ ] Write failing OpenAI payload tests.
- [ ] Run `python -m unittest tests.test_openai_client -v` and verify module import failure.
- [ ] Implement payload construction and text extraction.
- [ ] Run OpenAI tests and verify pass.

### Task 3: HTTP App and UI

**Files:**
- Create: `app.py`
- Create: `static/index.html`
- Create: `README.md`
- Create: `.gitignore`

**Interfaces:**
- Produces: `GET /`
- Produces: `GET /api/kb`
- Produces: `POST /api/ask`

- [ ] Implement server endpoints.
- [ ] Implement static dashboard.
- [ ] Run full unit tests.
- [ ] Run a local smoke test against `/api/ask`.
- [ ] Initialize local git repo and commit.
