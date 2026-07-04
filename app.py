"""No-npm local server for BankOps OpenAI RAG Assistant."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path

from src.bankops_kb import get_kb
from src.openai_client import OpenAIConfig, call_responses_api, extract_text
from src.rag_engine import build_prompt, offline_answer, retrieve


ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"


def load_env_file(env_path):
    """Load KEY=VALUE pairs from a local .env file without overriding real env vars."""
    path = Path(env_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_env_file(ROOT / ".env")


def _json_response(handler, payload, status=200):
    body = json.dumps(payload, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _parse_json_body(handler):
    length = int(handler.headers.get("Content-Length", "0"))
    if length <= 0:
        return {}
    return json.loads(handler.rfile.read(length).decode("utf-8"))


class BankOpsHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/kb":
            _json_response(self, {"kb": get_kb()})
            return
        if self.path == "/" or self.path.startswith("/static/"):
            if self.path == "/":
                self.path = "/static/index.html"
            return super().do_GET()
        _json_response(self, {"error": "Not found"}, status=404)

    def do_POST(self):
        if self.path != "/api/ask":
            _json_response(self, {"error": "Not found"}, status=404)
            return
        try:
            payload = _parse_json_body(self)
            question = str(payload.get("question", "")).strip()
            use_web = bool(payload.get("useWeb", False))
            if not question:
                _json_response(self, {"error": "Question is required"}, status=400)
                return

            passages = retrieve(question, top_k=4)
            prompt = build_prompt(question, passages, use_public_web=use_web)
            config = OpenAIConfig.from_env()

            if not config.api_key:
                result = offline_answer(question, passages)
                result["api_status"] = "OPENAI_API_KEY not set. Returned deterministic fallback."
                _json_response(self, result)
                return

            raw_response = call_responses_api(prompt, config, use_web=use_web)
            text = extract_text(raw_response)
            parsed = _try_parse_json(text)
            result = {
                "mode": "openai_responses",
                "answer": parsed.get("answer", text),
                "citations": parsed.get("citations", [item["id"] for item in passages]),
                "risk": parsed.get("risk", "High" if any(item["risk"] == "High" for item in passages) else "Medium"),
                "next_action": parsed.get("next_action", "Review cited KB and escalate if evidence is incomplete."),
                "confidence": parsed.get("confidence", "Medium"),
                "public_web_notes": parsed.get("public_web_notes", ""),
                "api_status": f"OpenAI Responses API via {config.model}",
                "trace": {
                    "question": question,
                    "use_web": use_web,
                    "retrieved": [
                        {"id": item["id"], "title": item["title"], "score": item["score"], "source_url": item["source_url"]}
                        for item in passages
                    ],
                },
            }
            _json_response(self, result)
        except Exception as exc:
            _json_response(self, {"error": str(exc)}, status=500)

    def translate_path(self, path):
        if path.startswith("/static/"):
            relative = path.removeprefix("/static/")
            return str(STATIC / relative)
        return str(STATIC / "index.html")


def _try_parse_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                return {}
    return {}


def main():
    port = int(os.getenv("PORT", "8787"))
    server = ThreadingHTTPServer(("127.0.0.1", port), BankOpsHandler)
    print(f"BankOps OpenAI RAG running at http://127.0.0.1:{port}")
    print("Set OPENAI_API_KEY to enable OpenAI Responses API mode.")
    server.serve_forever()


if __name__ == "__main__":
    main()
