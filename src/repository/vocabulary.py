"""
File containing the functions to interact with the CosmosDB database where the words are stored and retrieved from
"""
import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid
from services.detect_language import detect_language_code

"""
Creating connection to CosmosDB
"""
load_dotenv()
credential = DefaultAzureCredential()
cosmos_endpoint = os.getenv("COSMOS_ACCOUNT_URI")
if not cosmos_endpoint:
    raise ValueError("COSMOS_ACCOUNT_URI is not set")
cosmos_client = CosmosClient(cosmos_endpoint, credential=credential)
dictionary_database = cosmos_client.get_database_client("dictionary")
words_container = dictionary_database.get_container_client("words")
user_container = dictionary_database.get_container_client("users")


def get_or_create_user_id_in_DB(telegram_id: str, username: str, first_name: str, last_name: str | None) -> str:
    """
    Function to lookup a user in the database by its telegram_id or creates a new user if it does not exist yet

    args:
    username: If we need to create a new user, this is the username of the user.
    """
    telegram_id = str(telegram_id)
    query = "SELECT * FROM c WHERE c.telegram_id = @telegram_id AND c.partition_key = 'shared'"
    items = list(user_container.query_items(query, parameters=[dict(name="@telegram_id", value=telegram_id)]))
    if len(items) == 0:
        user_id = str(uuid.uuid4())
        user_container.create_item(body={
            "name": first_name,
            "surname": last_name,
            "telegram_id": telegram_id,
            "email": "",
            "id": user_id,
            "username": username,
            "partition_key": "shared"
        })
        return user_id    
    user_id = items[0]['id']
    return user_id


def get_all_words(user_id: str) -> list[list[str]]:
    """
    Function to get all the words from the dictionary of a user, given its unique telegram_id

    args:
    user_id: the user id to get the words for

    returns:
    words: a list of all the words in the dictionary for the user
    """
    items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = @user_id", parameters=[dict(name="@user_id", value=user_id)]))
    words = [[item['text'], item['translation']['text']] for item in items]
    return words


def save_word(user_id: str, text: str, translation: str):
    """
    Function to save a new word to the dictionary in CosmosDB

    args:
    text: the word in the native language
    translation: the translation of the word

    returns:
    boolean: a boolean indicating if the word has been saved or not
    """
    language_code = detect_language_code(text)
    translation_language_code = detect_language_code(translation)
    # Generate an id to store word in cosmos and check, if the generated unique id is already in use
    unique_id = str(uuid.uuid4())
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
        "user_id":user_id, 
        "language_code": language_code, 
        "text":text, 
        "translation": {
            "text": translation, 
            "language_code": translation_language_code
        }       
    })


def delete_word(user_id: str, text: str):
    """
    Function to delete a word from the dictionary in CosmosDB given the word and its translation

    args:
    text: the word to be deleted from the dictionary, in the native language or the learning language

    returns:
    binary: a boolean indicating if at least one word has been deleted or not
    """
    language_code = detect_language_code(text)

    if language_code == "en":
        query = "SELECT * FROM c WHERE c.user_id = @user_id AND c.text = @text"
        items = list(words_container.query_items(query, parameters=[dict(name="@text", value=text), dict(name="@user_id", value=user_id)]))
    else:
        query = "SELECT * FROM c WHERE c.user_id = @user_id AND c.translation.text = @text"
        items = list(words_container.query_items(query, parameters=[dict(name="@text", value=text), dict(name="@user_id", value=user_id)]))
    
    # Check if there are any words to delete
    if len(items) != 0:
        for item in items:
            words_container.delete_item(item, partition_key=item['user_id']) 
        return True
    else:
        # No words to delete found.
        return False