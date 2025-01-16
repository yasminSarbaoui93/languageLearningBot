"""
File containing the functions to interact with the CosmosDB database where the words are stored and retrieved from
"""
import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid
from src.services.languageDetection import detect_language_code

"""
Creating connection to CosmosDB
"""
load_dotenv()
credential = DefaultAzureCredential()
cosmos_endpoint = os.getenv("COSMOS_ACCOUNT_URI")
cosmos_client = CosmosClient(cosmos_endpoint, credential=credential)
dictionary_database = cosmos_client.get_database_client("dictionary")
words_container = dictionary_database.get_container_client("words")
user_container = dictionary_database.get_container_client("users")


def get_all_words(first_name, last_name, telegram_id, username):
    """
    Function to get all the words from the dictionary for a given user

    args:
    user_id: the user id to get the words for

    returns:
    words: a list of all the words in the dictionary for the user
    """
    user_id = _extract_user_id_from_cosmos(first_name, last_name, telegram_id, username)
    
    items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = @user_id", parameters=[dict(name="@user_id", value=user_id)]))
    words = [[item['text'], item['translation']['text']] for item in items]
    #words = [item['translation']['text'] for item in items]
    return words

def _extract_user_id_from_cosmos(first_name, last_name, telegram_id, username):
    """
    search query to check if there is a user with the given user_id on cosmos db

    args:
    first_name: the first name of the user
    last_name: the last name of the user
    telegram_id: the telegram id of the user
    username: the username of the user

    returns:
    user_id: the id of the user object in cosmos db
    """
    query = "SELECT * FROM c WHERE c.telegram_id = @telegram_id"
    parameters = [dict(name="@telegram_id", value=telegram_id)]
    items = list(user_container.query_items(query, parameters))
    
    if len(items) == 0:
        #create a new item in cosmos DB in the list users with partition_key = "shared", name = message.from_user.first_name, surname = message.from_user.last_name, user_id = message.from_user.id, email = ""
        user_container.create_item(body={
            "name": first_name,
            "surname": last_name,
            "telegram_id": telegram_id,
            "email": "",
            "username": username,
            "partition_key": "shared"
        })
        items = list(user_container.query_items(query, parameters))
    user_id = items[0]['id']
    return user_id
    
    


def save_word(text, translation):
    """
    Function to save a new word to the dictionary in CosmosDB

    args:
    text: the word in the native language
    translation: the translation of the word

    returns:
    boolean: a boolean indicating if the word has been saved or not
    """
    text = text.lower()
    translation = translation.lower()
    unique_id = str(uuid.uuid4())
    language_code = detect_language_code(text)
    translation_language_code = detect_language_code(translation)
    
    # Check, if the generated unique id is already in use
    words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
    num_words_with_same_id = len(words_with_same_id)
    while num_words_with_same_id != 0:
        unique_id = str(uuid.uuid4())
        words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
        num_words_with_same_id = len(words_with_same_id)

    # Check, if the word is already in the dictionary
    duplicate_words = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = '553fcaa0-2530-472c-9126-ffec24c62a6c' AND c.text = @text AND c.translation.text = @translation", parameters=[dict(name="@text", value=text), dict(name="@translation", value=translation)]))
    if len(duplicate_words) != 0:
        raise Exception("Duplicate word found")
    
    # Save the word to the database
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


def delete_word(text):
    """
    Function to delete a word from the dictionary in CosmosDB given the word and its translation

    args:
    text: the word to be deleted from the dictionary, in the native language or the learning language

    returns:
    binary: a boolean indicating if at least one word has been deleted or not
    """
    text = text.lower()
    language_code = detect_language_code(text)

    if language_code == "en":
        items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = '553fcaa0-2530-472c-9126-ffec24c62a6c' AND c.text = @text", parameters=[dict(name="@text", value=text)]))
    else:
        items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = '553fcaa0-2530-472c-9126-ffec24c62a6c' AND c.translation.text = @text", parameters=[dict(name="@text", value=text)]))
    
    # Check if there are any words to delete
    if len(items) != 0:
        for item in items:
            words_container.delete_item(item, partition_key=item['user_id']) 
        return True
    else:
        # No words to delete found.
        return False
