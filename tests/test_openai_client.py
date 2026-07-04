import unittest

from src.openai_client import build_responses_payload, extract_text


class OpenAIClientTests(unittest.TestCase):
    def test_payload_without_web_search(self):
        payload = build_responses_payload("Answer from context", model="gpt-4.1-mini", use_web=False)
        self.assertEqual(payload["model"], "gpt-4.1-mini")
        self.assertEqual(payload["input"], "Answer from context")
        self.assertNotIn("tools", payload)

    def test_payload_with_web_search(self):
        payload = build_responses_payload("Check public sources", model="gpt-4.1-mini", use_web=True)
        self.assertEqual(payload["tools"], [{"type": "web_search"}])
        self.assertEqual(payload["tool_choice"], "auto")

    def test_extract_text_from_output_text(self):
        self.assertEqual(extract_text({"output_text": "hello"}), "hello")

    def test_extract_text_from_output_content(self):
        response = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {"type": "output_text", "text": "first"},
                        {"type": "output_text", "text": " second"},
                    ],
                }
            ]
        }
        self.assertEqual(extract_text(response), "first second")


if __name__ == "__main__":
    unittest.main()
