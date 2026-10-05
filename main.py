"""Small, dependency-free helpers for Python projects."""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path


ERROR_TIPS: tuple[tuple[str, str], ...] = (
    (
        "SyntaxError",
        "Check the line named in the traceback for a missing colon, unmatched bracket, or misspelled keyword. Strings must have matching quotes.",
    ),
    (
        "IndentationError",
        "Python uses indentation to define code blocks. Use consistent spaces (four per level is conventional) and avoid mixing tabs and spaces.",
    ),
    (
        "NameError",
        "Check the spelling and capitalization of the name. Make sure it is defined before use and is in scope.",
    ),
    (
        "TypeError",
        "Check the types of the values in the failing operation. Convert values explicitly when needed, and check the function's expected arguments.",
    ),
    (
        "ValueError",
        "The value has the right type but an invalid value. Check the input format and validate it before converting or using it.",
    ),
    (
        "IndexError",
        "The requested list or sequence index is out of range. Check its length and remember that Python indexes start at zero.",
    ),
    (
        "KeyError",
        "The dictionary does not contain that key. Check the key spelling or use dict.get() when a key may be absent.",
    ),
    (
        "AttributeError",
        "The object does not have that attribute. Check the object's type, the attribute spelling, and whether the value is None.",
    ),
    (
        "FileNotFoundError",
        "Check the file path and current working directory. Use an absolute path or confirm that the file exists where the program expects it.",
    ),
    (
        "ImportError",
        "Check the import name and module path. Confirm the dependency is installed in the same Python environment running the program.",
    ),
    (
        "ModuleNotFoundError",
        "Check the module name and active Python environment. Install the missing package there if it is an external dependency.",
    ),
    (
        "ZeroDivisionError",
        "Check the divisor before dividing. Handle zero explicitly if it is a valid input.",
    ),
)


def check_file(path: Path) -> tuple[bool, str]:
    """Parse a Python file and return (success, human-readable message)."""
    if not path.exists():
        return False, f"File not found: {path}"
    if not path.is_file():
        return False, f"Not a file: {path}"
    try:
        source = path.read_text(encoding="utf-8-sig")
    except UnicodeError as exc:
        return False, f"Could not read {path} as UTF-8: {exc}"
    except OSError as exc:
        return False, f"Could not read {path}: {exc}"

    try:
        ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        location = f"line {exc.lineno}" if exc.lineno is not None else "unknown line"
        if exc.offset is not None:
            location += f", column {exc.offset}"
        detail = exc.msg or "invalid syntax"
        return False, f"Syntax error in {path} ({location}): {detail}"
    return True, f"Syntax OK: {path}"


def find_error_tip(message: str) -> tuple[str, str] | None:
    """Find a known Python exception name in an error message."""
    normalized = message.strip().casefold()
    for name, tip in ERROR_TIPS:
        if name.casefold() in normalized:
            return name, tip
    return None


def make_readme(title: str, description: str) -> str:
    """Create a small Markdown README from a project title and description."""
    safe_title = title.strip()
    safe_description = description.strip()
    return (
        f"# {safe_title}\n\n"
        f"{safe_description}\n\n"
        "## Getting started\n\n"
        "Add setup and usage instructions here.\n\n"
        "## License\n\n"
        "This project is licensed under the MIT License.\n"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-dev-toolkit",
        description="Small, dependency-free helpers for Python projects.",
        epilog=(
            "Examples:\n"
            "  python main.py check main.py\n"
            '  python main.py error "TypeError: unsupported operand type"\n'
            '  python main.py readme "My Project" "A useful developer project."'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(dest="command", required=True)

    check_parser = commands.add_parser(
        "check", help="check a Python file for syntax errors"
    )
    check_parser.add_argument("file", type=Path, help="Python source file to check")

    error_parser = commands.add_parser(
        "error", help="show debugging tips for a Python error message"
    )
    error_parser.add_argument("message", help="exception name or error message")

    readme_parser = commands.add_parser(
        "readme", help="print a starter README in Markdown"
    )
    readme_parser.add_argument("title", help="project title")
    readme_parser.add_argument("description", help="short project description")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "check":
        ok, message = check_file(args.file)
        stream = sys.stdout if ok else sys.stderr
        print(message, file=stream)
        return 0 if ok else 1

    if args.command == "error":
        match = find_error_tip(args.message)
        if match is None:
            known = ", ".join(name for name, _ in ERROR_TIPS)
            print(
                "No specific tip found. Include the exception name (for example, "
                f"TypeError). Known types: {known}.",
                file=sys.stderr,
            )
            return 1
        name, tip = match
        print(f"{name}: {tip}")
        return 0

    if args.command == "readme":
        if not args.title.strip() or not args.description.strip():
            parser.error("title and description must not be blank")
        print(make_readme(args.title, args.description), end="")
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
