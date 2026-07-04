import os
from pathlib import Path
import tempfile
import unittest

from app import load_env_file


class EnvConfigTests(unittest.TestCase):
    def test_load_env_file_sets_missing_values_without_overwriting_existing_env(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text(
                "# sample env\n"
                "BANKOPS_TEST_API_KEY=from-file\n"
                "BANKOPS_EXISTING=from-file\n"
                "BANKOPS_QUOTED=\"quoted value\"\n",
                encoding="utf-8",
            )

            os.environ.pop("BANKOPS_TEST_API_KEY", None)
            os.environ.pop("BANKOPS_QUOTED", None)
            os.environ["BANKOPS_EXISTING"] = "already-set"

            try:
                load_env_file(env_path)
                self.assertEqual(os.environ["BANKOPS_TEST_API_KEY"], "from-file")
                self.assertEqual(os.environ["BANKOPS_QUOTED"], "quoted value")
                self.assertEqual(os.environ["BANKOPS_EXISTING"], "already-set")
            finally:
                os.environ.pop("BANKOPS_TEST_API_KEY", None)
                os.environ.pop("BANKOPS_QUOTED", None)
                os.environ.pop("BANKOPS_EXISTING", None)

    def test_gitignore_keeps_real_env_file_out_of_git(self):
        ignore = Path(".gitignore").read_text(encoding="utf-8")
        self.assertIn(".env", ignore.splitlines())
        self.assertIn("!.env.example", ignore.splitlines())


if __name__ == "__main__":
    unittest.main()
