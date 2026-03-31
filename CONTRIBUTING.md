# Contributing to Password Strength & Security Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing.

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- pip or conda

### Setup Development Environment
```bash
git clone https://github.com/YOUR-USERNAME/password-analyzer.git
cd password-analyzer
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running Tests
```bash
python app.py
# Visit http://127.0.0.1:5000
```

## How to Contribute

### Reporting Bugs
1. Check if the bug is already reported in Issues
2. Include:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, browser)

### Suggesting Features
1. Check existing Issues and PRs
2. Describe the feature and why it's valuable
3. Provide examples of how it would work

### Code Contributions
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature/your-feature`
6. Open a Pull Request

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Commit Message Guidelines

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes

**Example:**
```
feat: Add password history tracking

- Implement local storage for analyzed passwords
- Add export as CSV functionality
- Include timestamp for each analysis
```

## Testing

Before submitting a PR:
1. Test the application locally
2. Try edge cases (very long passwords, special characters, etc.)
3. Verify no console errors in browser DevTools
4. Ensure API responses handle errors gracefully

## Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Comment complex cryptographic logic
- Include examples for new features

## Review Process

- Maintainers will review your PR
- Feedback may be requested
- Once approved, your PR will be merged
- Your contribution will be acknowledged

## Questions?

Feel free to open an issue with the label `question`.

---

## Areas for Contribution

We're actively looking for contributors in these areas:

- [ ] Password history tracking
- [ ] Offline mode with cached breach database
- [ ] Multi-language support
- [ ] Browser extension version
- [ ] Mobile app version
- [ ] Additional entropy metrics
- [ ] Performance optimizations
- [ ] UI/UX improvements
- [ ] Additional security checks
- [ ] Integration with password managers

Thank you for contributing to better password security! 🔐
