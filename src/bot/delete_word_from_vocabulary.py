"""
This file contains the functions to be called by the bot to add a new word to the user's vocabulary
"""
import os
from src.repository.vocabulary import delete_word, get_or_create_user
from src.services.get_llm_response import translate_sentence_with_llm

def remove_word(user_message, bot):
    """
    Function to add a new word to the user's vocabulary, to be called from telegram_bot.py

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    _ask_for_word_to_be_deleted(user_message, bot)    


def _ask_for_word_to_be_deleted(user_message, bot):
    """
    Function to register the word to be deleted from the user's vocabulary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    user = get_or_create_user(str(user_message.from_user.id), user_message.from_user.username, user_message.from_user.first_name, user_message.from_user.last_name)
    base_language_code = user.base_language

    bot_message = f"Type the word you want to remove from your vocabulary"
    if base_language_code != "en":
        bot_message = translate_sentence_with_llm(bot_message, base_language_code)
    bot.send_message(user_message.chat.id, bot_message)
    bot.register_next_step_handler(user_message, lambda user_message: _delete_word(user_message, bot, user))


def _delete_word(user_message, bot, user):    
    """
    Function to delete the word from the user's vocabulary

    args:
    user_message: the message object from the user
    bot: the bot object to send messages to the user
    """
    word_to_be_deleted = user_message.text
    bot_message = ""
    user_id = user.id
    base_language_code = user.base_language
    try:
        words_deleted = delete_word(user_id, word_to_be_deleted)
        if words_deleted:
            bot_message = f"The word <b>{word_to_be_deleted}</b> has been removed from your vocabulary"
            if base_language_code != "en":
                bot_message = translate_sentence_with_llm(bot_message, user.base_language)
        else:
            bot_message = f"The word <b>{word_to_be_deleted}</b> could not be found in your vocabulary"
            if base_language_code != "en":
                bot_message = translate_sentence_with_llm(bot_message, user.base_language)
    except Exception as e:
        print(f"An error occurred: {e}")
        bot_message = f"An error occurred while trying to remove the word <b>{word_to_be_deleted}</b> from your vocabulary."
        if base_language_code != "en":
            bot_message = translate_sentence_with_llm(bot_message, user.base_language)
    
    bot.send_message(user_message.chat.id, bot_message, parse_mode='HTML')