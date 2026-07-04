import unittest

from src.bankops_kb import get_kb
from src.rag_engine import build_prompt, offline_answer, retrieve


class RagEngineTests(unittest.TestCase):
    def test_kb_has_public_source_metadata(self):
        kb = get_kb()
        self.assertGreaterEqual(len(kb), 7)
        for item in kb:
            self.assertIn("source_url", item)
            self.assertTrue(item["source_url"].startswith("https://"))
            self.assertIn("source_note", item)

    def test_retrieves_unauthorized_transaction_policy(self):
        results = retrieve("UPI fraud reported after 5 working days from SMS alert", top_k=3)
        ids = [item["id"] for item in results]
        self.assertIn("RBI-UT-001", ids)
        self.assertIn("RBI-UT-002", ids)

    def test_retrieves_beneficial_owner_policy(self):
        results = retrieve("Can we open a company account if beneficial owner is not verified?", top_k=3)
        ids = [item["id"] for item in results]
        self.assertIn("RBI-KYC-003", ids)

    def test_prompt_contains_guardrails_and_citations(self):
        passages = retrieve("unauthorized transaction after 7 working days", top_k=2)
        prompt = build_prompt("unauthorized transaction after 7 working days", passages, use_public_web=False)
        self.assertIn("Do not invent policy", prompt)
        self.assertIn("RBI-UT-001", prompt)
        self.assertIn("Return JSON", prompt)

    def test_offline_answer_returns_trace(self):
        passages = retrieve("card fraud complaint unresolved for 90 days", top_k=3)
        result = offline_answer("card fraud complaint unresolved for 90 days", passages)
        self.assertEqual(result["mode"], "offline_fallback")
        self.assertTrue(result["citations"])
        self.assertIn("retrieved", result["trace"])


if __name__ == "__main__":
    unittest.main()
