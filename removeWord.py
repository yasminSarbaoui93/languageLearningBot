"""
This file contains the function to add a new word to the dictionary
"""
import os
from vocabulary import delete_word

nativelanguage_word = ""
translation = ""


def remove_word(user_message, bot):
    """
    Function to add a new word to the dictionary, to be called from telegram_bot.py

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    _ask_for_nativelanguage_word(user_message, bot)    


def _ask_for_nativelanguage_word(user_message, bot):
    """
    Function to register the word to be added to the dictionary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    bot.reply_to(user_message, f"Type the english word you want to remove to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_translation(user_message, bot))


def _ask_for_translation(user_message, bot):
    """
    Function to register the translation of the word to be added to the dictionary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    global nativelanguage_word
    nativelanguage_word = user_message.text
    bot.reply_to(
        user_message, f"Type the German translation of the word {nativelanguage_word}"
    )
    bot.register_next_step_handler(user_message, lambda user_message: _delete_word(user_message, bot))    


def _delete_word(user_message, bot):    
    """
    Function to delete the word from the dictionary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    global nativelanguage_word, translation
    translation = user_message.text
    delete_result = delete_word(nativelanguage_word, translation)
    if delete_result:
        bot_response = f"The word <b>'{nativelanguage_word}'</b> and its translation <b>'{translation}'</b> have been removed from the dictionary"
    else:
        bot_response = f"The word <b>'{nativelanguage_word}'</b> and its translation <b>'{translation}'</b> could not be found in the dictionary"
    nativelanguage_word = ""
    translation = ""
    bot.reply_to(user_message, bot_response)