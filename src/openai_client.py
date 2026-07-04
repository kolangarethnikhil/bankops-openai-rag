"""OpenAI Responses API client using only Python standard library."""

from dataclasses import dataclass
import json
import os
import urllib.error
import urllib.request


RESPONSES_URL = "https://api.openai.com/v1/responses"


@dataclass(frozen=True)
class OpenAIConfig:
    api_key: str
    model: str = "gpt-4.1-mini"
    timeout_seconds: int = 45

    @staticmethod
    def from_env():
        return OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            timeout_seconds=int(os.getenv("OPENAI_TIMEOUT_SECONDS", "45")),
        )


def build_responses_payload(prompt, model="gpt-4.1-mini", use_web=False):
    payload = {
        "model": model,
        "input": prompt,
        "temperature": 0.2,
    }
    if use_web:
        payload["tools"] = [{"type": "web_search"}]
        payload["tool_choice"] = "auto"
    return payload


def extract_text(response):
    if isinstance(response.get("output_text"), str):
        return response["output_text"]

    chunks = []
    for output in response.get("output", []):
        for content in output.get("content", []):
            if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                chunks.append(content["text"])
    return "".join(chunks).strip()


def call_responses_api(prompt, config, use_web=False):
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY is not set")

    payload = build_responses_payload(prompt, model=config.model, use_web=use_web)
    request = urllib.request.Request(
        RESPONSES_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {body}") from exc
