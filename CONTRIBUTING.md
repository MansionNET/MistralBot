# Contributing to MistralBot

Thank you for your interest in contributing to MistralBot! We appreciate your help in making this AI-powered IRC bot even better.

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When you create a bug report, include:

- A clear and descriptive title
- Detailed steps to reproduce the problem
- Example messages that trigger the issue
- Error messages and logs
- Your Python version and operating system
- Whether you're using a custom configuration

### Suggesting Enhancements

We love new ideas! When suggesting enhancements:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Explain why this enhancement would be useful
- Include examples of how it would be used
- Note any potential impacts on rate limiting or API usage

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs or configuration, update the documentation
4. Ensure your code follows our style guidelines
5. Make sure your commits are clean and well-described
6. Issue the pull request

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment:
```bash
cp .env.example .env
```

5. Add your Mistral AI API key to `.env`

## Code Style Guidelines

We follow strict Python best practices:

### General Rules
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Keep functions focused and modular
- Maximum line length: 100 characters
- Use type hints for function arguments and returns

### Documentation
- All functions must have docstrings
- Use Google-style docstring format
- Include examples in docstrings where helpful
- Comment complex logic or business rules

### Example Function Structure:
```python
def process_message(self, sender: str, message: str) -> Optional[str]:
    """
    Process an incoming IRC message and generate a response.

    Args:
        sender: The nickname of the message sender
        message: The content of the message

    Returns:
        Optional[str]: The response message or None if no response needed
    
    Raises:
        RateLimitError: If the user has exceeded their quota
    """
    # Implementation
```

## Commit Messages

Follow these guidelines for commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- First line should be under 72 characters
- Reference issues and pull requests liberally
- Consider starting the commit message with an applicable emoji:
  - 🎨 `:art:` when improving format/structure
  - 🐛 `:bug:` when fixing a bug
  - ✨ `:sparkles:` when adding a new feature
  - 📝 `:memo:` when writing docs

Example:
```
✨ Add custom prompt template support

- Implement template manager class
- Add configuration options for custom templates
- Update documentation with template examples

Fixes #123
```

## Testing

When adding new features:

1. Test basic functionality
   - Command parsing
   - Rate limiting
   - Error handling

2. Test edge cases
   - Long messages
   - Special characters
   - Invalid inputs

3. Test rate limiting
   - Per-user limits
   - Global limits
   - Cooldown periods

4. Test error handling
   - API failures
   - Network issues
   - Invalid configurations

## Documentation Updates

When making changes, remember to:

1. Update the README.md if you:
   - Add new features
   - Change configuration options
   - Modify rate limits
   - Add new dependencies

2. Update inline documentation:
   - Function docstrings
   - Class documentation
   - Complex logic explanations

3. Update example configurations

## Questions?

Feel free to:
- Open an issue with questions
- Join our IRC channel for discussion
- Contact the maintainers directly

Remember: No contribution is too small! Even fixing typos helps.
