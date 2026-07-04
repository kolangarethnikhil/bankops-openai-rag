from pathlib import Path
import unittest


class UiContractTests(unittest.TestCase):
    def setUp(self):
        self.html = Path("static/index.html").read_text(encoding="utf-8")

    def test_normal_chat_layout_contract(self):
        required_markers = [
            'id="appShell"',
            'class="sidebar"',
            'id="messageList"',
            'id="composer"',
            'id="messageInput"',
            'id="sendButton"',
            'function renderMarkdown',
            'class="source-chip"',
            'BankOps Assistant',
        ]
        for marker in required_markers:
            self.assertIn(marker, self.html)

    def test_technical_and_aria_admin_ui_removed(self):
        forbidden_markers = [
            'RAG Query Console',
            'Grounded response',
            'id="sourceDrawer"',
            'Trace JSON',
            'View structured trace',
            'Retrieval Trace',
            'Assistant Mode',
            'KB Search',
            'Refresh KB Index',
            'Rebuild Synonyms',
            'View Bot Memory',
            'Training Stats',
            'Train ARIA',
        ]
        for marker in forbidden_markers:
            self.assertNotIn(marker, self.html)


if __name__ == "__main__":
    unittest.main()
