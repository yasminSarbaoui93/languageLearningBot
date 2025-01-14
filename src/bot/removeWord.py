"""
This file contains the function to add a new word to the dictionary
"""
import os
from src.repository.vocabulary import delete_word

word_to_be_deleted = ""
translation = ""


def remove_word(user_message, bot):
    """
    Function to add a new word to the dictionary, to be called from telegram_bot.py

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    _ask_for_word_to_be_deleted(user_message, bot)    


def _ask_for_word_to_be_deleted(user_message, bot):
    """
    Function to register the word to be deleted from the dictionary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    bot.reply_to(user_message, f"Type the word you want to remove to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _delete_word(user_message, bot))


def _delete_word(user_message, bot):    
    """
    Function to delete the word from the dictionary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    global word_to_be_deleted 
    word_to_be_deleted = user_message.text
    delete_result = delete_word(word_to_be_deleted)
    if delete_result:
        bot_response = f"The word <b>{word_to_be_deleted}</b> has been removed from the dictionary"
    else:
        bot_response = f"The word <b>{word_to_be_deleted}</b> and its translation could not be found in the dictionary"
    bot.send_message(user_message.chat.id, bot_response, parse_mode='HTML')
    word_to_be_deleted = ""
    translation = ""
