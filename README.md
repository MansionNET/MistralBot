# MistralBot

A sophisticated IRC bot powered by Mistral AI that provides intelligent chat assistance and code help. MistralBot brings the power of large language models to IRC channels through a simple interface.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)

## IRC Server Details

Join us on MansionNET IRC to chat with us, test the bot, and play some trivia! 

🌐 **Server:** irc.inthemansion.com  
🔒 **Port:** 6697 (SSL)  
📝 **Channel:** #opers, #general, #welcome, #devs (and many others)

## Features

- AI-powered chat assistance using Mistral AI
- Code explanation and generation
- Built-in rate limiting and user quotas
- SSL/TLS support for secure IRC connections
- Customizable prompt templates
- Smart message handling for IRC message length limits
- Debug logging

## Requirements

- Python 3.8 or higher
- Mistral AI API key ([Get one here](https://mistral.ai))
- `requests` and `python-dotenv` libraries
- SSL-enabled IRC server

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MansionNET/mistralbot.git
cd mistralbot
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` and add your Mistral AI API key:
```env
MISTRAL_API_KEY=your_api_key_here
```

## Usage

Start the bot:
```bash
python mistralbot.py
```

### Available Commands

In any channel where the bot is present:

- `!ask <question>` - Ask a general question to the AI
  - Example: `!ask What is the capital of France?`
  - Example: `!ask Can you explain quantum computing?`

- `!code <question>` - Get programming help with code examples
  - Example: `!code How do I read a file in Python?`
  - Example: `!code Write a simple web server`

- `!help` - Display available commands and usage information

## Configuration

The bot can be configured through environment variables or by editing the code:

### Environment Variables
- `MISTRAL_API_KEY` (required): Your Mistral AI API key

### Code Configuration
- IRC Server settings
  - Server address
  - Port
  - Nickname
  - Channels to join

- Rate Limiting
  - Requests per minute (default: 10)
  - Requests per day (default: 1000)
  - Per-user daily limit (default: 50)

- Prompt Templates
  - Default conversation template
  - Code explanation template
  - Custom templates can be added

## Rate Limits

To prevent abuse and ensure fair usage, MistralBot implements several rate limits:

- Global limits:
  - 10 requests per minute
  - 1000 requests per day

- Per-user limits:
  - 50 requests per day
  - 3-second cooldown between commands

## Prompt Templates

MistralBot uses customizable prompt templates for different types of queries:

```python
prompt_templates = {
    "default": "You are a helpful assistant. Provide clear, direct responses without unnecessary detail. Question: {query}",
    "code": "You are a programming teacher. First give a ONE-SENTENCE explanation. Then after 'CODE:', show simple, practical code examples with minimal comments. Keep both explanation and code concise. Question: {query}",
    "explain": "Explain this concept in 2-3 short, clear sentences: {query}"
}
```

You can modify these templates or add new ones to customize the bot's responses.

## API Usage

MistralBot uses the Mistral AI API with the following configuration:

- Model: mistral-tiny
- Max tokens: 300
- Temperature: 0.7

Please review [Mistral AI's pricing](https://mistral.ai/pricing/) and terms of service before deployment.

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code style
- Pull request process
- Development setup
- Testing requirements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

Never share your Mistral AI API key or commit it to version control. Always use environment variables or secure configuration management.

## Project Status

This project is actively maintained. For support:

- Open an issue for bugs or feature requests
- Check existing issues before creating new ones
- Follow the contribution guidelines when submitting code

## Acknowledgments

- Mistral AI for providing the language model API
- The IRC community for continued support
- All contributors to the project
