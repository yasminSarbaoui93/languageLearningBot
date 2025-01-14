"""
File containing the functions to interact with the CosmosDB database where the words are stored and retrieved from
"""
import os
from dotenv import load_dotenv
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential
import uuid
from languageDetection import detect_language_code

"""
Creating connection to CosmosDB
"""
load_dotenv()
credential = DefaultAzureCredential()
cosmos_endpoint = os.getenv("COSMOS_ACCOUNT_URI")
cosmos_client = CosmosClient(cosmos_endpoint, credential=credential)
dictionary_database = cosmos_client.get_database_client("dictionary")
words_container = dictionary_database.get_container_client("words")


def get_all_words(user_id):
    """
    Function to get all the words from the dictionary for a given user

    args:
    user_id: the user id to get the words for

    returns:
    words: a list of all the words in the dictionary for the user
    """
    items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = @user_id", parameters=[dict(name="@user_id", value=user_id)]))
    words = [[item['text'], item['translation']['text']] for item in items]
    #words = [item['translation']['text'] for item in items]
    return words


def save_word(text, translation):
    """
    Function to save a new word to the dictionary in CosmosDB

    args:
    text: the word in the native language
    translation: the translation of the word

    returns:
    message: a message indicating if the word has been added or if it already exists
    """
    text = text.lower()
    translation = translation.lower()
    unique_id = str(uuid.uuid4())
    language_code = detect_language_code(text)
    translation_language_code = detect_language_code(translation)
    
    words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
    num_words_with_same_id = len(words_with_same_id)
    while num_words_with_same_id != 0:
        unique_id = str(uuid.uuid4())
        words_with_same_id = list(words_container.query_items(query="SELECT * FROM c WHERE c.id = @id", parameters=[dict(name="@id", value=unique_id)], enable_cross_partition_query=True))
        num_words_with_same_id = len(words_with_same_id)

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


def delete_word(text, translation):
    """
    Function to delete a word from the dictionary in CosmosDB given the word and its translation

    args:
    text: the word in the native language
    translation: the translation of the word

    returns:
    binary: a boolean indicating if the word has been deleted or not
    """
    text = text.lower()
    translation = translation.lower()
    try:
        items = list(words_container.query_items(query="SELECT * FROM c WHERE c.user_id = '553fcaa0-2530-472c-9126-ffec24c62a6c' AND c.text = @text AND c.translation.text = @translation", parameters=[dict(name="@text", value=text), dict(name="@translation", value=translation)]))
        if len(items) != 0:
            print(items)
            for item in items:
                words_container.delete_item(item, partition_key=item['user_id']) 
            return True
        else:
            return False
    except Exception as e:
        print("An error occurred " + str(e))
        return False