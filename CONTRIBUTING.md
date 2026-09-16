# Contributing to MarkItDown Studio IDE

Thank you for your interest in contributing to **MarkItDown Studio IDE**! We appreciate bug reports, feature suggestions, documentation improvements, and pull requests.

---

## Code of Conduct

All contributors and participants agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior to the project maintainers.

---

## How Can You Contribute?

### 1. Reporting Bugs
- Search existing issues to ensure the bug hasn't already been reported.
- Open a new issue using the **Bug Report** template.
- Include OS version, Python version, steps to reproduce, and sample files if possible.

### 2. Suggesting Enhancements
- Use the **Feature Request** template to propose new features or new document formats.
- Explain the motivation, use cases, and potential impact.

### 3. Submitting Pull Requests (PRs)
1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Set up the development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```
3. Follow the Test-Driven Development (TDD) workflow:
   - Add automated tests in `tests/unit/` or `tests/integration/` covering your changes.
   - Ensure all tests pass:
     ```bash
     pytest
     ```
4. Commit your changes with clear, descriptive commit messages (Conventional Commits encouraged).
5. Push to your fork and submit a Pull Request targeting `main`.

---

## Code Style & Standards

- **Python**: Follow PEP 8 guidelines. Keep functions modular and typed.
- **Frontend**: Clean Vanilla JavaScript and semantic HTML5. Avoid unnecessary external frameworks.
- **Internationalization**: When introducing new UI labels or texts, remember to update all locale files (`ui/locales/en-US.json`, `ui/locales/pt-BR.json`, `ui/locales/zh-CN.json`) and `ui/i18n.js`.
