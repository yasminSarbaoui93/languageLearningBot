#This file contains the function to add a new word to the dictionary
import pandas as pd
import os
from wordRepository import save_word_to_cosmos

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

# Function to save the new word locally from the user text, save the pair with word and translation both to the csv and to cosmosDB
def _save_word(user_message, bot):    
    global source_word, translation
    translation = user_message.text
    new_word = pd.DataFrame({"English": [source_word], "German": [translation]})
    _save_word_to_csv_file(new_word)
    save_word_to_cosmos(source_word, translation)
    source_word = ""
    translation = ""
    bot.reply_to(user_message, "The word has been added to the dictionary")

# Function to save a word to a local csv file
csv_name = "TermsList.csv"
def _save_word_to_csv_file(new_word):
    if os.path.exists(csv_name):
        terms_data = pd.read_csv(csv_name, sep=";")
        terms_data = pd.concat([terms_data, new_word], ignore_index=True)
    else:
        terms_data = new_word
    terms_data.to_csv(csv_name, sep=";", index=False)

