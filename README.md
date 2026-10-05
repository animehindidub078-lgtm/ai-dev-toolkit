# AI Dev Toolkit

AI Dev Toolkit is a small command-line helper for common Python project tasks. It uses only the Python standard library and works on Windows, macOS, and Linux.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Getting started

Clone the repository, then run commands from its directory:

```console
python main.py --help
```

On Windows, `py main.py --help` works as well.

## Commands

### Check Python syntax

Parse a Python file without executing it. A successful check exits with status `0`; a syntax or file error exits with status `1` and explains the problem.

```console
python main.py check main.py
python main.py check path/to/your_script.py
```

### Get debugging tips

Pass a Python exception name or traceback message to see a concise debugging suggestion. The current tips cover common syntax, name, type, value, sequence, dictionary, attribute, file, import, and division errors.

```console
python main.py error "TypeError: unsupported operand type"
```

If the message does not match a known exception, the command lists the supported exception names and exits with status `1`.

### Generate a README starter

Provide a project title and short description. The generated Markdown is printed to standard output so you can review or redirect it to a file.

```console
python main.py readme "My Project" "A useful developer project."
python main.py readme "My Project" "A useful developer project." > README.generated.md
```

## Run the tests

The tests use Python's built-in `unittest` module:

```console
python -m unittest discover -s tests -v
```

## Contributing

Issues and pull requests are welcome. For a change:

1. Fork the repository and create a branch for your work.
2. Keep changes focused and explain the problem they solve.
3. Add or update tests for changed behavior.
4. Run `python -m unittest discover -s tests -v` and try the affected CLI command.
5. Open a pull request with a clear summary and any relevant context.

Please keep the project dependency-free unless a new dependency is necessary and its value is explained.

## Roadmap

- [ ] Add focused tips for more built-in Python exceptions.
- [ ] Add an optional output-file argument to the README generator.
- [ ] Improve syntax-check diagnostics while keeping checks safe and dependency-free.
- [ ] Add shell completion once command names and options stabilize.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
