"""Retrieval and grounded fallback logic for BankOps RAG."""

import re
from collections import Counter

from .bankops_kb import get_kb


STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "for", "of", "in", "on", "is", "are", "we",
    "can", "what", "should", "with", "from", "after", "before", "this", "that", "it",
    "be", "as", "by", "at", "if", "when", "how",
}


def tokenize(text):
    return [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in STOPWORDS and len(token) > 1]


def _score_item(question_tokens, question_text, item):
    searchable = " ".join([item["title"], " ".join(item["tags"]), item["text"]]).lower()
    item_tokens = Counter(tokenize(searchable))
    score = sum(item_tokens[token] for token in question_tokens)

    for tag in item["tags"]:
        if tag in question_text:
            score += 7

    if "working days" in question_text and item["id"] == "RBI-UT-002":
        score += 10
    if any(word in question_text for word in ["unauthorized", "unauthorised", "fraud", "upi"]) and item["id"].startswith("RBI-UT"):
        score += 8
    if any(word in question_text for word in ["beneficial", "owner", "company"]) and item["id"] == "RBI-KYC-003":
        score += 12
    if any(word in question_text for word in ["pep", "high risk", "source of funds"]) and item["id"] == "RBI-KYC-004":
        score += 10

    return score


def retrieve(question, top_k=4):
    """Return the top matching KB passages with deterministic scores."""
    question_text = question.lower()
    question_tokens = tokenize(question)
    scored = []
    for item in get_kb():
        score = _score_item(question_tokens, question_text, item)
        if score > 0:
            enriched = dict(item)
            enriched["score"] = score
            scored.append(enriched)
    scored.sort(key=lambda item: (-item["score"], item["id"]))
    return scored[:top_k]


def build_prompt(question, passages, use_public_web=False):
    context = "\n\n".join(
        f"[{item['id']}] {item['title']}\nRisk: {item['risk']}\nSource: {item['source_url']}\n{item['text']}"
        for item in passages
    )
    web_instruction = (
        "If the hosted web search tool is available, use it only to verify public RBI/NPCI-style facts. "
        "Do not use private forums, customer records, or unverifiable bank-specific claims."
        if use_public_web
        else "Do not use web search for this answer."
    )
    return f"""You are BankOps RAG Assistant for an HCLTech hackathon demo.

Rules:
- Answer only from the retrieved context below.
- Do not invent policy, amounts, timelines, or bank-specific rules.
- If context is insufficient, say escalation to a human policy owner is required.
- Cite KB IDs in every answer.
- Write the answer field in concise markdown with short headings and bullet points when useful.
- Return JSON with keys: answer, citations, risk, next_action, confidence, public_web_notes.

{web_instruction}

User question:
{question}

Retrieved context:
{context}

Return JSON only."""


def _risk_from_passages(passages):
    return "High" if any(item["risk"] == "High" for item in passages) else "Medium"


def offline_answer(question, passages):
    """Return a deterministic markdown answer when OpenAI is not configured."""
    if not passages:
        return {
            "mode": "offline_fallback",
            "answer": (
                "### Recommended action\n"
                "- I do not have enough grounded synthetic policy context to answer this safely.\n"
                "- Escalate to a human banking policy owner before advising the customer.\n"
                "\n### Why\n"
                "- Banking operations answers need a cited policy source for timelines, liability, or KYC decisions."
            ),
            "citations": [],
            "risk": "High",
            "next_action": "Escalate to human review",
            "confidence": "Low",
            "trace": {"question": question, "retrieved": []},
        }

    citations = [item["id"] for item in passages]
    if "RBI-UT-002" in citations:
        next_action = "Register complaint, classify reporting timeline, avoid final reimbursement promises, and escalate if unresolved or high risk."
        answer_points = [
            "Register the complaint immediately and capture transaction date, reporting date, channel, amount, and customer contact.",
            "Classify the liability window using the reporting timeline: within 3 working days, 4 to 7 working days, or beyond 7 working days.",
            "Do not promise final reimbursement until investigation and policy checks are complete.",
            "Escalate if the case is unresolved, high risk, or requires compliance review.",
        ]
    elif "RBI-KYC-003" in citations:
        next_action = "Pause activation until beneficial owner and authorized signatory evidence is verified."
        answer_points = [
            "Do not activate the business account while beneficial owner evidence is incomplete.",
            "Verify ownership, control, and authorized signatory details from acceptable documents.",
            "Escalate to KYC or compliance review if ownership remains unclear.",
        ]
    elif "RBI-KYC-004" in citations:
        next_action = "Route to enhanced due diligence and senior approval workflow."
        answer_points = [
            "Treat the case as higher risk and apply enhanced due diligence.",
            "Collect additional context such as customer profile, source of funds, and transaction purpose where required.",
            "Proceed only after the appropriate senior or compliance approval is recorded.",
        ]
    else:
        next_action = "Follow the cited source-backed steps and escalate if evidence is incomplete."
        answer_points = [item["text"] for item in passages[:2]]

    source_line = ", ".join(citations)
    answer = (
        "### Recommended action\n"
        + "\n".join(f"- {point}" for point in answer_points)
        + "\n\n### Sources used\n"
        + f"- {source_line}"
    )

    return {
        "mode": "offline_fallback",
        "answer": answer,
        "citations": citations,
        "risk": _risk_from_passages(passages),
        "next_action": next_action,
        "confidence": "Medium" if len(passages) >= 2 else "Low",
        "trace": {
            "question": question,
            "retrieved": [
                {"id": item["id"], "title": item["title"], "score": item["score"], "source_url": item["source_url"]}
                for item in passages
            ],
        },
    }
