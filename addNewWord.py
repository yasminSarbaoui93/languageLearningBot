"""This file contains the function to add a new word to the dictionary"""
import os
from vocabulary import save_word

nativelanguage_word = ""
translation = ""


def add_word_to_dictionary(user_message, bot):
    """
    Function to add a new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    _ask_for_original_word(user_message, bot)    


def _ask_for_original_word(user_message, bot):
    """
    Function to ask the user for the word to be added to the dictionary
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    bot.reply_to(user_message, f"Type the english word you want to add to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_translated_word(user_message, bot))


def _ask_for_translated_word(user_message, bot):
    """
    Function to ask the user for the translation of the word to be added to the dictionary
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    global nativelanguage_word
    nativelanguage_word = user_message.text
    bot.reply_to(
        user_message, f"Type the German translation of the word {nativelanguage_word}"
    )
    bot.register_next_step_handler(user_message, lambda user_message: _save_word_to_db(user_message, bot))    


def _save_word_to_db(user_message, bot):
    """
    Function to save the new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    global nativelanguage_word, translation
    translation = user_message.text
    saveword_result = save_word(nativelanguage_word, translation)
    nativelanguage_word = ""
    translation = ""
    bot.reply_to(user_message, saveword_result)