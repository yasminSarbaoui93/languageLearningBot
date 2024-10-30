# German Vocabulary Bot

A Telegram bot that helps you learn German vocabulary.

## Getting Started

If you don't have a virtual environment (a `.env` folder) yet, create one with the following command.

```bash
python -m venv .venv

# or if you are on macOS

python3 -m venv .venv
```

Open the command line and activate the virtual environment.

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with the following contents.

```
API_TOKEN="<TELEGRAM API TOKEN>"
OPENAI_API_KEY="<YOUR_API_KEY>"
AZURE_RESOURCE_GROUP="<>"
COSMOS_ACCOUNT_NAME="<>"
COSMOS_ACCOUNT_URI="<>"
COSMOS_ACCOUNT_KEY="<>"

```

Start the bot with the following command.

```bash
python telegram_bot.py
```
