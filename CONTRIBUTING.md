# Contributing to Sens Prism

Thank you for your interest in contributing to Sens Prism! This document outlines how to get started.

## Code of Conduct

We are committed to providing a welcoming and inspiring community. Please review our Code of Conduct before participating.

All contributors must:
- Be respectful and inclusive
- Provide constructive feedback
- Focus on what's best for the community
- Show empathy toward others

## Getting Started

### Prerequisites

- Python 3.9+ (for Python SDK development)
- Node.js 16+ and npm (for TypeScript SDK development)
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/prism.git`
3. Add upstream remote: `git remote add upstream https://github.com/ecri0/prism.git`
4. Create a branch: `git checkout -b feature/your-feature`

### Python SDK Development

```bash
cd sdk/python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
black . && isort . && ruff check .

# Type checking
mypy sens
```

### TypeScript SDK Development

```bash
cd sdk/typescript

# Install dependencies
npm install

# Build
npm run build

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format
```

## Making Changes

### Create a Feature Branch

```bash
git checkout -b feature/your-feature
```

### Follow Code Style

- **Python**: Black (100-char lines), isort, type hints
- **TypeScript**: ESLint, Prettier, strict mode

```bash
# Auto-format Python
black sens && isort sens

# Auto-format TypeScript
npm run format
```

### Write Tests

All changes must include tests:

**Python**:
```python
import pytest
from sens import SensClient
from sens.exceptions import SensValidationError

def test_client_initialization():
    """Test that client initializes correctly."""
    client = SensClient(api_key="sens_sk_test123")
    assert client.api_key == "sens_sk_test123"

def test_missing_api_key_raises_error():
    """Test that missing API key raises error."""
    with pytest.raises(SensValidationError):
        SensClient()
```

**TypeScript**:
```typescript
import { SensClient } from "../src/client";
import { SensValidationError } from "../src/exceptions";

describe("SensClient", () => {
  test("initializes with API key", () => {
    const client = new SensClient({ apiKey: "sens_sk_test123" });
    expect(client).toBeDefined();
  });

  test("throws error when API key is missing", () => {
    expect(() => {
      new SensClient({});
    }).toThrow(SensValidationError);
  });
});
```

### Run Tests

```bash
# Python
pytest tests/ -v

# TypeScript
npm test
```

### Write Documentation

If adding a feature, document it:
- Update README if it's a major feature
- Add docstrings to functions
- Update the CHANGELOG.md

## Documentation Contributions

Documentation improvements are welcome! This includes:
- API documentation
- Usage examples
- Use case guides
- Tutorials
- Fixes for typos or clarity

Documentation is in Markdown in the `docs/` directory.

### Documentation Guidelines

- Use clear, simple language
- Include code examples where helpful
- Link to related documentation
- Keep line length under 100 characters

## Submitting Changes

### Commit Messages

Follow conventional commits:

```
feat: add batch upload support
fix: correct rate limit error handling
docs: update authentication guide
test: add tests for context rail
```

Format:
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `style`, `chore`

### Push and Create Pull Request

```bash
git push origin feature/your-feature
```

Then create a Pull Request on GitHub with:
1. Clear title describing the change
2. Description of what changed and why
3. Reference to any related issues
4. Confirmation that tests pass

## Pull Request Process

1. **Automated checks must pass**:
   - Tests run and pass
   - Linting passes
   - Type checking passes

2. **Code review**: A maintainer will review your changes

3. **Address feedback**: Make requested changes and push updates

4. **Approval**: Once approved, your PR will be merged

## Areas We Need Help

We're especially interested in contributions for:

### Code
- Performance improvements
- Additional SDK languages (Java, Go, etc.)
- Better error messages
- Comprehensive test coverage

### Documentation
- Use case examples
- Integration guides
- Video tutorials
- Language-specific guides

### Community
- Issue triage and responses
- Example projects
- Blog posts
- Speaking at conferences

## Reporting Issues

Found a bug? Please open an issue with:

1. **Clear title**: What's the problem?
2. **Description**: What did you expect vs. what happened?
3. **Steps to reproduce**: How can we reproduce it?
4. **Environment**: Python/Node version, OS, SDK version
5. **Error logs**: Full error messages and stack traces
6. **Minimal example**: Smallest code that shows the issue

## Feature Requests

Have an idea? Open an issue with:

1. **Clear title**: What feature would you like?
2. **Description**: What problem does it solve?
3. **Example usage**: Show how it would be used
4. **Alternatives**: What workarounds exist now?

## Project Structure

```
prism/
├── docs/                          # Documentation
│   ├── getting-started.md
│   ├── concepts/
│   ├── api/
│   └── guides/
├── sdk/
│   ├── python/
│   │   ├── sens/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── exceptions.py
│   │   │   └── types.py
│   │   ├── tests/
│   │   ├── pyproject.toml
│   │   └── README.md
│   └── typescript/
│       ├── src/
│       │   ├── index.ts
│       │   ├── client.ts
│       │   ├── exceptions.ts
│       │   └── types.ts
│       ├── tests/
│       ├── package.json
│       └── README.md
├── examples/
│   ├── python/
│   └── typescript/
├── .github/
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── SECURITY.md
└── CONTRIBUTING.md
```

## Development Workflow

### For Small Changes
1. Fork → Create branch → Make changes → Push → PR

### For Large Features
1. Open issue to discuss approach
2. Get feedback from maintainers
3. Implement with regular commits
4. Submit PR with comprehensive tests
5. Iterate based on feedback

## Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and ideas
- **Email**: [dev@sens.ai](mailto:dev@sens.ai) for project inquiries

## License

By contributing, you agree that your contributions will be licensed under the Business Source License 1.1, converting to Apache License 2.0 on February 14, 2029.

## Appreciation

We deeply appreciate all contributions, from bug reports to code changes. Contributors are recognized in release notes and on our website.

Thank you for helping make Sens Prism better!

---

Questions? Contact [dev@sens.ai](mailto:dev@sens.ai)
