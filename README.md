# German Vocabulary Bot

A Telegram bot that helps you learn German.

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
AZURE_RESOURCE_GROUP="<YOUR_AZURE_RESOURCE_GROUP_NAME>"
COSMOS_ACCOUNT_NAME="<YOUR_COSMOSDB_ACCOUNT_NAME>"
COSMOS_ACCOUNT_URI="<YOUR_COSMOSDB_ACCOUNT_URI>"
LANGUAGESTUDIO_KEY="<YOUR_AZURE_LANGUAGESTUDIO_KEY>"
LANGUAGESTUDIO_ENDPOINT="<YOUR_AZURE_LANGUAGESTUDIO_ENDPOINT>"

```

Start the bot with the following command.

```bash
python src/app.py
```

## Testing

Run the unit tests with the following command.

```bash
python -m unittest
```

# APPENDIX

**Create Language Studio Resource**
Link to create the resource: https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics

**Create CosmosDB**
