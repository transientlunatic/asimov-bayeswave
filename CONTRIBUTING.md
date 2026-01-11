# Contributing to asimov-bayeswave

Thank you for your interest in contributing to asimov-bayeswave! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository on GitHub

2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/asimov-bayeswave.git
   cd asimov-bayeswave
   ```

3. Run the development setup script:
   ```bash
   ./setup_dev.sh --venv
   ```

   Or manually install:
   ```bash
   pip install -e ".[docs,test]"
   pip install pre-commit
   pre-commit install
   ```

4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

### Code Style

- Follow PEP 8 style guidelines
- Use Black for code formatting (max line length: 100)
- Use isort for import sorting
- Add type hints where appropriate
- Write clear, descriptive docstrings (NumPy style)

### Pre-commit Hooks

The repository uses pre-commit hooks to ensure code quality. These will run automatically on commit:

- black: Code formatting
- isort: Import sorting
- flake8: Linting
- Various file checks (trailing whitespace, etc.)

To run manually:
```bash
pre-commit run --all-files
```

### Testing

All new code should include tests. We use pytest for testing.

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=asimov_bayeswave --cov-report=html
```

### Documentation

Update documentation for any new features or API changes:

1. Update docstrings in the code
2. Update relevant .rst files in `docs/source/`
3. Build and review documentation locally:
   ```bash
   cd docs
   make html
   open build/html/index.html  # or your browser
   ```

## Submitting Changes

1. Ensure all tests pass:
   ```bash
   pytest
   ```

2. Ensure code is properly formatted:
   ```bash
   black asimov_bayeswave tests
   isort asimov_bayeswave tests
   flake8 asimov_bayeswave tests
   ```

3. Commit your changes with clear, descriptive messages:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

4. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a Pull Request on GitHub

### Pull Request Guidelines

Your PR should:

- Have a clear title and description
- Reference any related issues
- Include tests for new functionality
- Update documentation as needed
- Pass all CI checks
- Follow the project's code style

## Reporting Issues

When reporting issues, please include:

- A clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Your environment:
  - OS and version
  - Python version
  - asimov version
  - asimov-bayeswave version

## Code Review Process

1. All submissions require review
2. Reviewers may request changes
3. Once approved, a maintainer will merge your PR

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag -a v0.x.x -m "Release v0.x.x"`
4. Push tag: `git push origin v0.x.x`
5. Create GitHub release
6. GitHub Actions will automatically publish to PyPI

## Questions?

Feel free to open an issue for questions or discussion.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
