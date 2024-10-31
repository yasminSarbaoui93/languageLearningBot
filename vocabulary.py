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
    words = [[item['text'], item['translation']['text']] for item in items]
    #words = [item['translation']['text'] for item in items]
    return words


#Function to save a new word to the CosmosDB - id generated locally with uuid and user_id hardcoded for now 
#If an element with the same id already exists for all the partition keys then I create a new id with uuid
#If there is a duplicate, the word will not be saved
def save_word(text, translation):
    text = text.lower()
    translation = translation.lower()
    unique_id = str(uuid.uuid4())
    language_code = detect_language_code(text)
    translation_language_code = detect_language_code(translation)

    words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
    num_words_with_same_id = len(words_with_same_id)
    while num_words_with_same_id != 0:
        unique_id = str(uuid.uuid4())

    duplicate_words = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = '553fcaa0-2530-472c-9126-ffec24c62a6c' AND c.text = @text AND c.translation.text = @translation", parameters=[dict(name="@text", value=text), dict(name="@translation", value=translation)]))
    if len(duplicate_words) != 0:
        return "The word already exists"
    else:
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
        return "The word has been added to the dictionary"


#Function to delete a given word (native language and its translation) from cosmosDB
def delete_word(text, translation):
    text = text.lower()
    translation = translation.lower()
    try:
        items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = '553fcaa0-2530-472c-9126-ffec24c62a6c' AND c.text = @text AND c.translation.text = @translation", parameters=[dict(name="@text", value=text), dict(name="@translation", value=translation)]))
        for item in items:
            words_container.delete_item(item, partition_key=item['user_id']) 
        return "The word has been deleted from the dictionary"
    except Exception as e:
        print("Word not found in the CosmosDB dictionary " + str(e))
        return "The word is not in the dictionary"


