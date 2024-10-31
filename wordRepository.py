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

dictionary_database = cosmos_client.get_database_client("dictionary")
words_container = dictionary_database.get_container_client("words")

#Function to import the list of words in a local array from cosmosDB given the user ID
def get_all_words(user_id):
    items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = @user_id", parameters=[dict(name="@user_id", value=user_id)]))
    #items = list(words_container.read_all_items(user_id))
    words = [item['translation']['text'] for item in items]
    print(words)
    return

#Function to save a new word to the CosmosDB - id generated locally with uuid and user_id hardcoded for now 
def save_word_to_cosmos(text, translation):
    unique_id = str(uuid.uuid4())
    language_code = detect_language_code(text)
    translation_language_code = detect_language_code(translation)

    words_container.create_item(body={
        "id":unique_id, 
        "user_id":"553fcaa0-2530-472c-9126-ffec24c62a6c", 
        "language_code": language_code, 
        "text":text, 
        "translation": {
            "text": translation, 
            "language_code": translation_language_code
        }
    })


#Function to delete a given word (native language and its translation) from cosmosDB
def delete_word_from_cosmos(text, translation):
    try:
        items = list(words_container.query_items(query="SELECT * FROM c WHERE c.text = @text AND c.translation.text = @translation", parameters=[dict(name="@text", value=text), dict(name="@translation", value=translation)]))
        for item in items:
            words_container.delete_item(item, partition_key=item['user_id']) 
        print("The word has been deleted from cosmosDB")
    except Exception as e:
        print("Word not found in the dictionary " + e)


