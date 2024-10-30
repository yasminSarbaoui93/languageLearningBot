from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

load_dotenv()
cosmos_endpoint = os.getenv("COSMOS_ENDPOINT")
cosmos_key = os.getenv("COSMOS_KEY")
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)

#create a function to import the list of words in a local array from cosmosDB
def get_words():
    database = cosmos_client.get_database_client("dictionary")
    container = database.get_container_client("words")
    items = list(container.read_all_items())
    words = []
    for item in items:
        words.append(item)
    print(words)
    return


