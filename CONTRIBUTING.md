# Contributing to ragatui

Thank you for your interest in contributing to ragatui! This document provides guidelines and information for contributors.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/hapticPaper/ragatui.git
cd ragatui
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e ".[dev]"
```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **mypy** for type checking

Run the formatters and linters:
```bash
# Format code
black ragatui/ tests/ examples/

# Check linting
ruff check ragatui/ tests/ examples/

# Type checking
mypy ragatui/
```

## Testing

Run tests with pytest:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=ragatui --cov-report=html

# Run specific test file
pytest tests/test_decorators.py -v
```

## Project Structure

```
ragatui/
├── ragatui/              # Main package
│   ├── core/            # Core components (state, registry, app)
│   ├── decorators/      # Decorator implementations
│   ├── widgets/         # TUI widgets
│   ├── llm/             # LLM integration
│   ├── rag/             # RAG database integration
│   └── utils/           # Utility functions
├── tests/               # Test suite
├── examples/            # Example scripts
└── docs/                # Documentation (future)
```

## Adding New Features

### Adding a New Decorator

1. Add the decorator function to `ragatui/decorators/tui_decorators.py`
2. Register any widgets in the `ExecutionState`
3. Add tests to `tests/test_decorators.py`
4. Add an example to `examples/`
5. Update the README

### Adding a New Widget

1. Create widget class in `ragatui/widgets/`
2. Inherit from appropriate Textual widget base class
3. Add to `ragatui/widgets/__init__.py`
4. Add tests if applicable
5. Document usage in README

### Adding LLM Provider Support

1. Create provider class in `ragatui/llm/providers.py`
2. Inherit from `LLMProvider` abstract base class
3. Implement required methods
4. Add to provider factory function
5. Add tests and examples

## Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/my-feature`
3. **Make your changes** following the code style guidelines
4. **Add tests** for new functionality
5. **Run tests and linters** to ensure everything passes
6. **Update documentation** (README, docstrings, etc.)
7. **Commit your changes**: `git commit -m "Add my feature"`
8. **Push to your fork**: `git push origin feature/my-feature`
9. **Open a Pull Request** with a clear description

### PR Checklist

- [ ] Code follows the project style guidelines
- [ ] Tests added for new functionality
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Commits have clear messages
- [ ] PR has a clear description

## Code Review

All submissions require review. We aim to:
- Review PRs within 48 hours
- Provide constructive feedback
- Collaborate on improvements

## Types of Contributions

### Bug Reports

Open an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)

### Feature Requests

Open an issue with:
- Clear description of the feature
- Use cases and benefits
- Proposed implementation (optional)

### Documentation

Documentation improvements are always welcome:
- Fix typos
- Clarify explanations
- Add examples
- Improve API documentation

### Examples

New examples showing ragatui usage:
- Should be self-contained
- Include comments explaining key concepts
- Follow the code style
- Be added to the `examples/` directory

## Design Principles

When contributing, keep these principles in mind:

1. **Minimal API Surface**: Keep decorators and APIs simple and intuitive
2. **Modularity**: Components should be loosely coupled
3. **Extensibility**: Users should be able to extend and customize
4. **Performance**: Don't block the main execution
5. **Documentation**: Code should be well-documented

## Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and experiences
- Collaborate constructively

## Questions?

If you have questions:
1. Check existing issues and discussions
2. Open a new discussion
3. Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Acknowledgments

Thank you to all contributors who help make ragatui better!
