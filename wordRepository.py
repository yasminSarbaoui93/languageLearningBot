import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid
from languageDetection import detect_language_code

#Creating connection to CosmosDB
load_dotenv()
credential = DefaultAzureCredential()
cosmos_endpoint = os.getenv("COSMOS_ACCOUNT_URI")
cosmos_client = CosmosClient(cosmos_endpoint, credential=credential)


#Function to import the list of words in a local array from cosmosDB given the user ID
def get_all_words(user_id):
    database = cosmos_client.get_database_client("dictionary")
    container = database.get_container_client("words")
    items = list(container.query_items(query="SELECT * FROM c WHERE c.user_id = @user_id", parameters=[dict(name="@user_id", value=user_id)]))
    #items = list(container.read_all_items(user_id))
    words = [item['translation']['text'] for item in items]
    print(words)
    return

#Function to save a new word to the CosmosDB - id generated locally with uuid and user_id hardcoded for now 
def save_word_to_cosmos(text, translation):
    database = cosmos_client.get_database_client("dictionary")
    container = database.get_container_client("words")
    unique_id = str(uuid.uuid4())
    language_code = detect_language_code(text)
    translation_language_code = detect_language_code(translation)

    container.create_item(body={
        "id":unique_id, 
        "user_id":"553fcaa0-2530-472c-9126-ffec24c62a6c", 
        "language_code": language_code, 
        "text":text, 
        "translation": {
            "text": translation, 
            "language_code": translation_language_code
        }
    })
