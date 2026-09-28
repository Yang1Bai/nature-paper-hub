import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("checker", Path(__file__).resolve().parents[1] / "scripts/check_journal_urls.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class URLHealthTests(unittest.TestCase):
    def test_real_errors_remain_errors(self):
        for status in (0, 404, 410, 500, 503):
            self.assertEqual(checker.classify(status), "failed")

    def test_access_denial_is_not_healthy(self):
        for status in (401, 403, 429):
            self.assertEqual(checker.classify(status), "unverified")
        self.assertEqual(checker.classify(200), "ok")
