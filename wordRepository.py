import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

#Creating connection to CosmosDB
load_dotenv()
credential = DefaultAzureCredential()
cosmos_endpoint = os.getenv("COSMOS_ACCOUNT_URI")
cosmos_client = CosmosClient(cosmos_endpoint, credential=credential)


#Function to import the list of words in a local array from cosmosDB
#in this moment, it's just importing all the words, need to add import words relevant to the user
def get_words():
    database = cosmos_client.get_database_client("dictionary")
    container = database.get_container_client("words")
    items = list(container.read_all_items())
    words = [item['translation']['text'] for item in items]
    print(words)
    return


def save_word_to_cosmos(english_term, german_term):
    database = cosmos_client.get_database_client("dictionary")
    container = database.get_container_client("words")
    container.create_item(body={"user_id":"553fcaa0-2530-472c-9126-ffec24c62a6c", "language_code": "en", "text":english_term, "translation": {"text": german_term, "language_code": "de"}})