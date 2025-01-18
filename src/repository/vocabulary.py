"""
File containing the functions to interact with the CosmosDB database where the words are stored and retrieved from
"""
import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid
from services.detect_language import detect_language_code
from .models import User, Word

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


def get_or_create_user_id(telegram_id: str, username: str, first_name: str, last_name: str | None) -> str:
    """
    Function to lookup a user in the database by its telegram_id or creates a new user if it does not exist yet

    args:
    telegram_id: the telegram id of the user, user_message.from_user.id
    username: the name the user should get in case it doesn't exist 
    first_name: the first name of the user
    last_name: the last name of the user

    returns:
    user_id: the unique id of the user in the database
    """
    telegram_id = str(telegram_id)
    query = "SELECT * FROM c WHERE c.telegram_id = @telegram_id AND c.partition_key = 'shared'"
    items = list(user_container.query_items(query, parameters=[dict(name="@telegram_id", value=telegram_id)]))
    if len(items) == 0:
        user_id = str(uuid.uuid4())
        new_user = User(user_id, first_name, str(last_name), username, "", "", "", telegram_id, "shared")
        user_container.create_item(body=new_user.__dict__)
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
    new_word = Word(unique_id, user_id, language_code, text, translation, translation_language_code)
    words_container.create_item(body=new_word.__dict__)


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
    

def save_user_base_and_learning_languages(user_id: str, base_language: str, learning_language: str):
    """
    Function to add the base language and learning language to the user in the database

    args:
    base_language: the base language of the user
    learning_language: the language the user wants to learn
    """
    user = user_container.read_item(item=user_id, partition_key="shared")
    user_container.upsert_item(body=user)
    updated_user = User(user_id, user["name"], user["surname"], user["username"],user["email"], base_language, learning_language, user["telegram_id"], user["partition_key"])
    user_container.upsert_item(body=updated_user.__dict__)

def extract_learning_language_code(user_id: str) -> str:
    """
    Function to extract the learning language of the user from the database

    args:
    user_id: the user id to get the learning language for

    returns:
    learning_language: the language the user wants to learn
    """
    user = user_container.read_item(item=user_id, partition_key="shared")
    return user["learning_language"]