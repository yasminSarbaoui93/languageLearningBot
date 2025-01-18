"""This file contains the functions to be called by the bot that are used to get a random word from the dictionary and ask the user to translate it
"""
import random
import os
import pandas as pd
from src.repository.vocabulary import get_all_words, get_or_create_user


def send_random_word(bot, message):
    """
    Function that sends a random word from the dictionary to the user to translate

    args:
    bot: the bot object to send the message
    message: the message object from the user
    """
    user = get_or_create_user(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    user_id = user.id
    user_known_words = get_all_words(user_id)
    print(f"\nExtracting a random word from dictionary of userid: {user_id} and telegramid: {message.from_user.id} containing {len(user_known_words)} words\n")
    if len(user_known_words) == 0:
        bot.reply_to(message, "You don't have any words in your dictionary yet. Add some words first by writing <b>/add</b>!", parse_mode='HTML')
        return
    else:
        random_word = random.choice(user_known_words)
        base_language_word = random_word[0]
        learning_language_word = random_word[1]
        bot.send_message(message.chat.id, f"Translate this word: <b>{base_language_word}</b>", parse_mode='HTML')
        bot.register_next_step_handler(message, lambda msg: check_response(msg, learning_language_word, bot))


def check_response(message, learning_language_word, bot):
    """
    Function that checks if the user response is correct or not

    args:
    message: the message object from the user
    learning_language_word: the correct translation of the word
    bot: the bot object to send the response
    """
    if message.text == learning_language_word:
        bot.send_message(message.chat.id, "Correct! ✅")
    else:
        bot.send_message(message.chat.id, f"Incorrect! ❌\nThe translation is: <b>{learning_language_word}</b>", parse_mode='HTML')