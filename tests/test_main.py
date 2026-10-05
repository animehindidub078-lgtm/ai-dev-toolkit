"""Tests for the command-line helpers."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import main


class CheckFileTests(unittest.TestCase):
    def test_accepts_valid_python(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid.py"
            path.write_text("print('hello')\n", encoding="utf-8")
            ok, message = main.check_file(path)
        self.assertTrue(ok)
        self.assertIn("Syntax OK", message)

    def test_reports_invalid_python_location(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.py"
            path.write_text("if True print('oops')\n", encoding="utf-8")
            ok, message = main.check_file(path)
        self.assertFalse(ok)
        self.assertIn("Syntax error", message)
        self.assertIn("line 1", message)

    def test_reports_missing_file(self):
        ok, message = main.check_file(Path("definitely-missing-ai-dev-toolkit.py"))
        self.assertFalse(ok)
        self.assertIn("File not found", message)


class ErrorTipTests(unittest.TestCase):
    def test_finds_exception_case_insensitively(self):
        result = main.find_error_tip("TypeError: unsupported operand type")
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "TypeError")
        self.assertIn("types", result[1])

    def test_unknown_error_has_no_match(self):
        self.assertIsNone(main.find_error_tip("mysterious issue"))


class ReadmeTests(unittest.TestCase):
    def test_generates_starter_markdown(self):
        readme = main.make_readme("My Project", "A useful developer project.")
        self.assertTrue(readme.startswith("# My Project\n"))
        self.assertIn("A useful developer project.", readme)
        self.assertIn("## License", readme)


class CliTests(unittest.TestCase):
    def test_check_command_succeeds(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main.main(["check", str(Path(__file__))])
        self.assertEqual(status, 0)
        self.assertIn("Syntax OK", output.getvalue())

    def test_check_command_fails_for_missing_file(self):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            status = main.main(["check", "missing-file.py"])
        self.assertEqual(status, 1)
        self.assertIn("File not found", output.getvalue())

    def test_error_command_succeeds_for_known_exception(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main.main(["error", "TypeError: bad operands"])
        self.assertEqual(status, 0)
        self.assertIn("TypeError", output.getvalue())

    def test_error_command_fails_for_unknown_exception(self):
        output = io.StringIO()
        with contextlib.redirect_stderr(output):
            status = main.main(["error", "unknown problem"])
        self.assertEqual(status, 1)
        self.assertIn("Known types", output.getvalue())

    def test_readme_command_prints_markdown(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = main.main(["readme", "My Project", "A useful project."])
        self.assertEqual(status, 0)
        self.assertTrue(output.getvalue().startswith("# My Project\n"))


if __name__ == "__main__":
    unittest.main()
