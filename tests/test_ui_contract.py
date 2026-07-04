from pathlib import Path
import unittest


class UiContractTests(unittest.TestCase):
    def setUp(self):
        self.html = Path("static/index.html").read_text(encoding="utf-8")

    def test_chat_first_layout_contract(self):
        required_markers = [
            "class=\"app-shell\"",
            "class=\"sidebar\"",
            "id=\"messageList\"",
            "id=\"composer\"",
            "id=\"sendButton\"",
            "id=\"sourceDrawer\"",
            "BankOps",
            "Assistant Mode",
            "KB Search",
        ]
        for marker in required_markers:
            self.assertIn(marker, self.html)

    def test_old_query_console_removed(self):
        forbidden_markers = [
            "RAG Query Console",
            "Grounded response",
            "class=\"grid\"",
            "id=\"answer\"",
        ]
        for marker in forbidden_markers:
            self.assertNotIn(marker, self.html)


if __name__ == "__main__":
    unittest.main()
