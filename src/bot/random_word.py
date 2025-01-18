"""This file contains the functions to be called by the bot that are used to get a random word from the dictionary and ask the user to translate it
"""
import random
from src.repository.vocabulary import get_all_words, get_or_create_user
from src.services.get_llm_response import text_in_base_language


def send_random_word(bot, message):
    """
    Function that sends a random word from the dictionary to the user to translate

    args:
    bot: the bot object to send the message
    message: the message object from the user
    """
    user = get_or_create_user(str(message.from_user.id), message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    user_id = user.id
    base_language_code = user.base_language
    user_known_words = get_all_words(user_id)
    print(f"\nExtracting a random word from dictionary of userid: {user_id} and telegramid: {message.from_user.id} containing {len(user_known_words)} words\n")
    if len(user_known_words) == 0:
        bot_message_english = "You don't have any words in your dictionary yet. Add some words first by writing /add!"
        bot_message = text_in_base_language(base_language_code, bot_message_english)
        bot.reply_to(message,bot_message, parse_mode='HTML')
        return
    else:
        random_word = random.choice(user_known_words)
        base_language_word = random_word[0]
        learning_language_word = random_word[1]
        bot_message_english = "Translate this word:"
        bot_message = f"{text_in_base_language(base_language_code, bot_message_english)}: <b>{base_language_word}</b>"
        bot.send_message(message.chat.id, bot_message, parse_mode='HTML')
        bot.register_next_step_handler(message, lambda msg: check_response(msg, learning_language_word, bot, base_language_code))


def check_response(message, learning_language_word, bot, base_language_code):
    """
    Function that checks if the user response is correct or not

    args:
    message: the message object from the user
    learning_language_word: the correct translation of the word
    bot: the bot object to send the response
    """
    if message.text == learning_language_word:
        bot_message = text_in_base_language(base_language_code, "Correct!")
        bot.send_message(message.chat.id, f"{bot_message} ✅")
    else:
        bot_message = text_in_base_language(base_language_code, "Incorrect! ❌\nThe translation is:")
        bot.send_message(message.chat.id, f"{bot_message} <b>{learning_language_word}</b>", parse_mode='HTML')