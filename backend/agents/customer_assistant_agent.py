"""Small, deterministic RAG assistant for product support and satisfaction.

It retrieves approved passages before answering. This keeps the demo useful
without inventing medical claims or requiring an external LLM/vector store.
The store is intentionally replaceable by a persistent embedding index later.
"""

from datetime import datetime, timezone
import os
import re
from typing import Any

import httpx

DOCUMENTS = [
    {"id": "safety-001", "title": "Sensitive skin guidance", "text": "Patch test new products. Introduce one active at a time. Stop use if burning, swelling, hives, or a persistent rash occurs."},
    {"id": "routine-001", "title": "Daily routine", "text": "Use a gentle cleanser, moisturizer, and broad-spectrum SPF 30 or higher each morning. Reapply sunscreen outdoors."},
    {"id": "retail-001", "title": "Returns and satisfaction", "text": "Keep order confirmation and product packaging. Return eligibility depends on the retailer policy shown at checkout."},
    {"id": "privacy-001", "title": "Privacy", "text": "A scan uses the digital twin only when the customer chooses to share it. Never put raw selfies or health details into a public ledger."},
]
FEEDBACK: list[dict[str, Any]] = []

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _openai_suggestion(question: str, context: str) -> str | None:
    if not OPENAI_API_KEY:
        return None
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful and safe skincare assistant. Use the retrieved documents "
                    "to answer the user's question, and then provide one concise, actionable "
                    "suggestion based on that output."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{question}\n\n"
                    f"Retrieved context:\n{context}\n\n"
                    "Reply with a clear answer and a short suggestion."
                ),
            },
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }
    try:
        response = httpx.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return None

def _extract_suggestions(text: str, limit: int = 3) -> list[str]:
    lines = [s.strip() for s in text.splitlines() if s.strip()]
    suggestions: list[str] = []
    for line in lines:
        if len(suggestions) >= limit:
            break
        if line.lower().startswith("suggestion") or line.lower().startswith("recommend") or line.endswith("."):
            suggestions.append(line.rstrip(". "))
        if not suggestions:
            candidates = [s.strip() for s in re.split(r"[\.\n]+", text) if s.strip()]
            suggestions = candidates[:limit]
    return suggestions


def _retrieve(question: str, limit: int = 3) -> list[dict[str, str]]:
    terms = set(re.findall(r"[a-z0-9]+", question.lower()))
    ranked = sorted(DOCUMENTS, key=lambda doc: len(terms & set(doc["text"].lower().split())), reverse=True)
    return ranked[:limit]


def answer(question: str, user_id: str | None = None, use_twin: bool = False, twin: Any = None) -> dict[str, Any]:
    question = question.strip()
    if not question:
        raise ValueError("question is required")
    sources = _retrieve(question)
    context_text = " ".join(doc["text"] for doc in sources)
    if any(word in question.lower() for word in ("diagnose", "prescription", "cure")):
        response = "I can provide product and routine guidance, but I cannot diagnose conditions or prescribe treatment. Please consult a qualified clinician. " + context_text
        suggestions = ["Consult a qualified clinician for diagnosis or prescription advice."]
    else:
        openai_response = _openai_suggestion(question, context_text)
        if openai_response:
            response = openai_response
        else:
            response = context_text or "I’m here to help with skincare guidance."
        suggestions = _extract_suggestions(response)
    if use_twin and twin and getattr(twin, "skincare_routine", None):
        response += " Your saved routine currently has " + str(len(twin.skincare_routine)) + " steps."
    if not suggestions:
        suggestions = [response]
    return {
        "answer": response,
        "suggestions": suggestions,
        "sources": [{"id": d["id"], "title": d["title"]} for d in sources],
        "used_twin": bool(use_twin and twin),
        "user_id": user_id,
    }


def record_feedback(user_id: str, rating: int, comment: str = "", topic: str = "assistant") -> dict[str, Any]:
    if rating < 1 or rating > 5:
        raise ValueError("rating must be between 1 and 5")
    item = {"user_id": user_id, "rating": rating, "comment": comment[:1000], "topic": topic, "created_at": datetime.now(timezone.utc).isoformat()}
    FEEDBACK.append(item)
    return item


def satisfaction_summary() -> dict[str, Any]:
    ratings = [item["rating"] for item in FEEDBACK]
    return {"responses": len(ratings), "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else None}
