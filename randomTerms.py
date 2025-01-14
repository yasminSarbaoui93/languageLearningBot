"""This file contains the functions that are used to get a random word from the dictionary and ask the user to translate it
"""
import random
import os
import pandas as pd
from vocabulary import get_all_words
from dotenv import load_dotenv


load_dotenv()
user_id = os.getenv("USER_ID")
german_words = get_all_words(user_id)


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


def send_random_word(bot, message):
    """
    Function that sends a random word from the dictionary to the user to translate

    args:
    bot: the bot object to send the message
    message: the message object from the user
    """
    random_word = random.choice(german_words)
    native_language_word = random_word[0]
    learning_language_word = random_word[1]
    bot.reply_to(message, f"Translate this word: {native_language_word}")
    bot.register_next_step_handler(message, lambda msg: check_response(msg, learning_language_word, bot))