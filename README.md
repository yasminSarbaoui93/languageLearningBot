# Chatbot to support learning new languages

A Telegram bot that helps you learn German.


## Infrastructure
For this application we are using [Telebot](https://pytba.readthedocs.io/en/latest/) to build a chatbot that helps people learn new languages through their unique vocabulary.
The component of this application are:
- Telebot 
- OpenAI - gpt-4o
- Azure container registry
- Azure Container Apps
- Cosmos DB

Here's a guide on how to first setup all these resources:

### Telegram Bot

You need to obtain a telegram BOT API **TOKEN**.

To do so, open Telegram from your phone or laptop
Search for the account @**BotFather**

Start a new chat and type the following command: **/newbot**

The bot will respond asking you to chose a Name and then a username for your bot. For this project I have used germanLessons as name and germanLesson_bot as username

After this, the botfather will respond with your **access token**. Save this information

### Resource Group
Create a new resource group for all the resources we will be creating
```bash
az login
az group create --name <resource-group-name> --location <resource-group-location>
```

### Cosmos DB
Create a new Cosmos DB resource to store the users' vocabularies
```bash
az cosmosdb create --name <cosmosdb-account-name> --resource-group <resource-group-name> --locations regionName=<resource-group-location>
```

Create the database "dictionary"
```bash
az cosmosdb sql database create \
  --account-name <cosmosdb-account-name> \
  --name dictionary \
  --resource-group <resource-group-name>
```

Create the "users" container with "shared" partition key in order to store the users that are using the telebot to learn the language
```bash
az cosmosdb sql container create \
  --account-name <cosmosdb-account-name> \
  --database-name dictionary \
  --name users \
  --partition-key-path "/shared" \
  --resource-group <resource-group-name>
```

Create the "words" container with partition key "user" in order to store the users vocabulary and to partition it by user
```
az cosmosdb sql container create \
  --account-name <cosmosdb-account-name> \
  --database-name dictionary \
  --name words \
  --partition-key-path "/user_id" \
  --resource-group <resource-group-name>
```

For this application, we will ebable connection to cosmos DB from all networks and enable the connection string instead of RBAC
To achieve so, run the following command (they might take a while to execute, so don't worry)
```
  az resource update \
    --resource-type "Microsoft.DocumentDB/databaseAccounts" \
    --resource-group <resource-group-name> \
    --name <cosmosdb-account-name> \
    --set properties.disableLocalAuth=false \
    --set properties.publicNetworkAccess=Enabled
```
Following, we need to add a tag to our cosmos DB account
```bash
az resource update \
  --resource-group <your-resource-group> \
  --resource-type "Microsoft.DocumentDB/databaseAccounts" \
  --name <your-cosmosdb-account-name> \
  --set tags.SecurityControl="Ignore"
  ```

### Language service
Create a new language service resource
https://learn.microsoft.com/en-us/azure/ai-services/language-service/language-studio

### LLM
For this repo we are using OpenAI, gpt-4o. Feel free to chose what best suits you

### Docker
Make sure to install docker on your machine

### Azure Container Registry resource
We will use Azure Container Registry to store the image that will be used by Azure Container Apps
```bash
az acr create --resource-group <resource-group-name> --name <container-registry-name> --sku Basic --location <resource-location>
az acr login --name <container-registry-name>
```

### Container App
First we need to create a container app environment
```bash
az containerapp env create \
  --name <container-app-environment> \
  --resource-group <resource-group-name> \
  --location <resource-location>
```
Obtain Azure Container Registry credentials, username and password will be needed in the following step
```bash
az acr update -n <container-registry-name> --admin-enabled true
az acr credential show --name acrlanguagelearningbot --query "username" -o tsv
az acr credential show --name acrlanguagelearningbot --query "passwords[0].value" -o tsv
```
Create the Container App resource
```bash
az containerapp create \
  --name <container-app-name> \
  --resource-group <resource-group-name> \
  --environment <container-app-environment> \
  --registry-server <container-registry-name>.azurecr.io \
  --registry-username <container-registry-username> \
  --registry-password <container-registry-password>
```






## Getting Started with the Language Learning Bot APP

If you don't have a virtual environment (a `.env` folder) yet, create one with the following command.

```bash
python -m venv .venv

# or if you are on macOS
python3 -m venv .venv
```

Open the command line and activate the virtual environment.

```bash
source .venv/bin/activate
```

Install the requirements listed in the requirements.txt file
```bash
pip install -r requirements.txt
```

Create a `.env` file with the following contents.

```
API_TOKEN="<TELEGRAM API TOKEN>"
OPENAI_API_KEY="<YOUR_API_KEY>"
AZURE_RESOURCE_GROUP="<YOUR_AZURE_RESOURCE_GROUP_NAME>"
COSMOS_ACCOUNT_NAME="<YOUR_COSMOSDB_ACCOUNT_NAME>"
COSMOS_ACCOUNT_URI="<YOUR_COSMOSDB_ACCOUNT_URI>"
COSMOS_ACCOUNT_KEY="<YOUR_COSMOSDB_KEY>" #primary or seconday key, NOT the connection string
LANGUAGESTUDIO_KEY="<YOUR_AZURE_LANGUAGESTUDIO_KEY>"
LANGUAGESTUDIO_ENDPOINT="<YOUR_AZURE_LANGUAGESTUDIO_ENDPOINT>"

```

> **_NOTE:_**  For this application we enabled connections to **Cosmos DB** from all networks and enabled connection string instead of RBAC. In case this is not enabled on your end, go on the infrastructure section to see how to achieve this


## Run the bot locally
Start the bot locally with the following command.

```bash
python src/app.py
```

## Containerize the app using docker and test running container locally
Open docker

Build and tag the image
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t <your-image-name> .
```
> **_NOTE:_** you can consider naming the image already how you would tag it, in order to skip a repeatable step later. Example: `docker buildx build --platform linux/amd64,linux/arm64 -t acrlanguagelearningbot.azurecr.io/languagelearningbot:v0.1.1 . 

Run the image locally to test if the functinalities are working properly.
```bash
docker run --env-file .env <your-image-name>
```

## Deploy to the Cloud
Build and tag the image

```bash
docker tag <your-image-name> <your-acr-name>.azurecr.io/<your-image-name> #you can skip this step in case you named the image already as the tag
docker push <your-acr-name>.azurecr.io/<your-image-name>
```

Deploy to Azure Container Apps

```bash
az containerapp update \
  --name <your-app-name> \
  --resource-group <your-resource-group> \
  --image <your-acr-name>.azurecr.io/<your-image-name>:<new-tag> \
  --registry-login-server <your-acr-name>.azurecr.io \
  --registry-username <your-acr-username> \
  --registry-password <your-acr-password>
  ```

Test your app