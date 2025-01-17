"""This file contains the functions to be called by the bot that are used to get a random word from the dictionary and ask the user to translate it
"""
import random
import os
import pandas as pd
from src.repository.vocabulary import get_all_words, get_or_create_user_id_in_DB


def send_random_word(bot, message):
    """
    Function that sends a random word from the dictionary to the user to translate

    args:
    bot: the bot object to send the message
    message: the message object from the user
    """
    global user_known_words
    user_id = get_or_create_user_id_in_DB(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    user_known_words = get_all_words(user_id)
    random_word = random.choice(user_known_words)
    base_language_word = random_word[0]
    learning_language_word = random_word[1]
    bot.reply_to(message, f"Translate this word: {base_language_word}")
    bot.register_next_step_handler(message, lambda msg: check_response(msg, learning_language_word, bot))


def check_response(message, learning_language_word, bot):
    """
    Function that checks if the user response is correct or not

    args:
    message: the message object from the user
    learning_language_word: the correct translation of the word
    bot: the bot object to send the response
    """
    if message.text.lower() == learning_language_word.lower():
        bot.reply_to(message, "Correct! ✅")
    else:
        bot.reply_to(message, f"Incorrect! ❌\nThe correct translation is: <b>{learning_language_word}</b>", parse_mode='HTML')