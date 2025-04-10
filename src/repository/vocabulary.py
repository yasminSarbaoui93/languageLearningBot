"""
File containing the functions to interact with the CosmosDB database where the words are stored and retrieved from
"""
import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid
from .models import User, Word, Dictionary

"""
Creating connection to CosmosDB
"""
load_dotenv()
cosmos_endpoint = os.getenv("COSMOS_ACCOUNT_URI")
cosmos_key = os.getenv("COSMOS_ACCOUNT_KEY")
if not cosmos_endpoint or not cosmos_key:
    raise ValueError("COSMOS_ACCOUNT_URI and COSMOS_ACCOUNT_KEY must be set")
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
languagelearningDB = cosmos_client.get_database_client("dictionary")
words_container = languagelearningDB.get_container_client("words")
user_container = languagelearningDB.get_container_client("users")
dictionary_container = languagelearningDB.get_container_client("dictionaries")




def get_or_create_user(telegram_id: str, username: str, first_name: str, last_name: str | None) -> User:
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
    try:
        items = list(user_container.query_items(query, parameters=[dict(name="@telegram_id", value=telegram_id)]))
    except:
        print(f"An error occurred while querying the database")
        items = []
    if len(items) == 0:
        user_id = str(uuid.uuid4())
        new_user = User(user_id, first_name, str(last_name), username, "", telegram_id, "", "shared")
        user_container.create_item(body=new_user.__dict__)
        return new_user    
    db_user = items[0]
    user = User(db_user["id"], db_user["name"], db_user["surname"], db_user["username"], db_user["email"], db_user["telegram_id"], db_user["active_dictionary_id"], db_user["partition_key"])
    return user

def get_user_dictionary(telegram_id: str) -> Dictionary:
    """
    Function to get the dictionary in use by the user
    args:
    telegram_id: the telegram id of the user, user_message.from_user.id
    returns:
    dictionary: the dictionary in use by the user

    """
    telegram_id = str(telegram_id)
    query = "SELECT * FROM c WHERE c.telegram_id = @telegram_id AND c.partition_key = 'shared'"
    user = get_or_create_user(telegram_id, "", "", "")
    dictionary_id = user.active_dictionary_id
    if dictionary_id == "":
        raise Exception("No dictionary found for the user")
    items = list(dictionary_container.query_items(query="SELECT * FROM c WHERE c.id = @dictionary_id", parameters=[dict(name="@dictionary_id", value=dictionary_id)]))
    if len(items) == 0:
        raise Exception("No dictionary found for the user")
    db_dictionary = items[0]
    dictionary = Dictionary(db_dictionary["id"], db_dictionary["dictionary_name"], db_dictionary["base_language_code"], db_dictionary["learning_language_code"], db_dictionary["user_id"])
    return dictionary

def get_all_words(dictionary_id: str) -> list[list[str]]:
    """
    Function to get all the words from the dictionary of a user, given its unique telegram_id

    args:
    user_id: the user id to get the words for

    returns:
    words: a list of all the words in the dictionary for the user
    """
    items = list(words_container.query_items(query="SELECT * FROM c WHERE c.dictionary_id = @dictionary_id", parameters=[dict(name="@dictionary_id", value=dictionary_id)]))
    words = [[item['text'], item['translation']['text']] for item in items]
    return words


def save_word(dictionary, base_language_word: str, learning_language_word: str):
    """
    Function to save a new word to the dictionary in CosmosDB

    args:
    text: the word in the native language
    translation: the translation of the word

    returns:
    boolean: a boolean indicating if the word has been saved or not
    """
    base_language_code = dictionary.base_language_code
    learning_language_code = dictionary.learning_language_code
    dictionary_id = dictionary.id
    # Generate an id to store word in cosmos and check, if the generated unique id is already in use
    unique_id = str(uuid.uuid4())
    words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
    num_words_with_same_id = len(words_with_same_id)
    while num_words_with_same_id != 0:
        unique_id = str(uuid.uuid4())
        words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
        num_words_with_same_id = len(words_with_same_id)

    # Check, if the word is already in the dictionary
    duplicate_words = list(words_container.query_items(query="SELECT * FROM c WHERE c.dictionary_id = @dictionary_id AND c.base_language_word = @base_language_word AND c.learning_language_word = @learning_language_word", parameters=[dict(name="@base_language_word", value=base_language_word), dict(name="@learning_language_code", value=learning_language_word), dict(name="@dictionary_id", value=dictionary_id)]))
    if len(duplicate_words) != 0:
        raise Exception("Duplicate word found")
    
    # Save the word to the database
    new_word = Word(unique_id, dictionary_id, base_language_code, base_language_word, learning_language_code, learning_language_word)
    words_container.create_item(body=new_word.__dict__)


def delete_word(dictionary, word_to_be_deleted: str):
    """
    Function to delete a word from the dictionary in CosmosDB given the word and its translation

    args:
    text: the word to be deleted from the dictionary, in the native language or the learning language

    returns:
    binary: a boolean indicating if at least one word has been deleted or not
    """
    dictionary_id = dictionary.id
   
    query = "SELECT * FROM c WHERE c.dictionary_id = @dictionary_id AND c.base_language_word = @word_to_be_deleted"
    items = list(words_container.query_items(query, parameters=[dict(name="@base_language_word", value=word_to_be_deleted), dict(name="@dictionary_id", value=dictionary_id)]))
    
    if len(items) == 0:
        query = "SELECT * FROM c WHERE c.dictionary_id = @dictionary_id AND c.learning_language_word = @word_to_be_deleted"
        items = list(words_container.query_items(query, parameters=[dict(name="@learning_language_word", value=word_to_be_deleted), dict(name="@dictionary_id", value=dictionary_id)]))
    
    # Check if there are any words to delete
    if len(items) != 0:
        for item in items:
            words_container.delete_item(item, partition_key=item['dictionary_id']) 
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



# def extract_learning_language_code(user_id: str) -> str:
#     """
#     Function to extract the learning language of the user from the database

#     args:
#     user_id: the user id to get the learning language for

#     returns:
#     learning_language: the language the user wants to learn
#     """
#     user = user_container.read_item(item=user_id, partition_key="shared")
#     return user["learning_language"]