#This file contains the function to add a new word to the dictionary
import pandas as pd
import os
from wordRepository import save_word_to_cosmos
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()
language_key = os.getenv("LANGUAGESTUDIO_KEY")
language_endpoint = os.getenv("LANGUAGESTUDIO_ENDPOINT")

# Function to authenticate the client to use the Azure Text Analytics API
def authenticate_client():
    ta_credential = AzureKeyCredential(language_key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=language_endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

source_word = ""
translation = ""

# Function to add a new word to the dictionary, to be called from telegram_bot.py
def add_word(user_message, bot):
    _ask_for_original_word(user_message, bot)    

# Function to register the word to be added to the dictionary
def _ask_for_original_word(user_message, bot):
    bot.reply_to(user_message, f"Type the english word you want to add to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_translated_word(user_message, bot))

# Function to register the translation of the word to be added to the dictionary
def _ask_for_translated_word(user_message, bot):
    # Save english term
    global source_word
    source_word = user_message.text

    # Ask for the translation
    bot.reply_to(
        user_message, f"Type the German translation of the word {source_word}"
    )
    bot.register_next_step_handler(user_message, lambda user_message: _save_word(user_message, bot))    

# Function to save the new word to the csv
def _save_word(user_message, bot):
    
    # Save translation
    global source_word, translation
    translation = user_message.text

    # Detect language of the source word and translation
    source_language_code = client.detect_language([source_word])[0].primary_language.iso6391_name
    translation_language_code = client.detect_language([translation])[0].primary_language.iso6391_name
  
    # Define and save full new word on csv file
    new_word = pd.DataFrame({"English": [source_word], "German": [translation]})
    _save_word_to_csv_file(new_word)

    # Save the new word to the CosmosDB
    save_word_to_cosmos(source_language_code, source_word, translation_language_code, translation)

    # Reset global variables
    source_word = ""
    translation = ""
        
    bot.reply_to(user_message, "The word has been added to the dictionary")

# Function to save the new word to the csv file
def _save_word_to_csv_file(new_word):
    if os.path.exists("TermsList.csv"):
        terms_data = pd.read_csv("TermsList.csv", sep=";")
        terms_data = pd.concat([terms_data, new_word], ignore_index=True)
    else:
        terms_data = new_word
    terms_data.to_csv("TermsList.csv", sep=";", index=False)
