#This file contains the function to add a new word to the dictionary
import pandas as pd
import os
from vocabulary import save_word

nativelanguage_word = ""
translation = ""

# Function to add a new word to the dictionary, to be called from telegram_bot.py
def add_word_to_dictionary(user_message, bot):
    _ask_for_original_word(user_message, bot)    

# Function to register the word to be added to the dictionary
def _ask_for_original_word(user_message, bot):
    bot.reply_to(user_message, f"Type the english word you want to add to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_translated_word(user_message, bot))

# Function to register the translation of the word to be added to the dictionary
def _ask_for_translated_word(user_message, bot):
    # Save english term
    global nativelanguage_word
    nativelanguage_word = user_message.text

    # Ask for the translation
    bot.reply_to(
        user_message, f"Type the German translation of the word {nativelanguage_word}"
    )
    bot.register_next_step_handler(user_message, lambda user_message: _save_word_to_db(user_message, bot))    

# Function to save the new word locally from the user text, save the pair with word and translation both to the csv and to cosmosDB
def _save_word_to_db(user_message, bot):    
    global nativelanguage_word, translation
    translation = user_message.text
    saveword_result = save_word(nativelanguage_word, translation)
    nativelanguage_word = ""
    translation = ""
    bot.reply_to(user_message, saveword_result)
