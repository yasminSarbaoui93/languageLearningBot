"""This file contains the functions to be called by the bot that are used to get a random word from the dictionary and ask the user to translate it
"""
import random
from repository.vocabulary import get_all_words, get_user_dictionary
from services.llm_service import translate_to_language
from bot.helpers import send_bot_response


def send_random_word(bot, message):
    """
    Function that sends a random word from the dictionary to the user to translate

    args:
    bot: the bot object to send the message
    message: the message object from the user
    """
    dictionary = get_user_dictionary(str(message.from_user.id))
    dictionary_id = dictionary.id
    base_language_code = dictionary.base_language_code
    user_known_words = get_all_words(dictionary_id)
    print(f"\nExtracting a random word from dictionary of dictionary_id: {dictionary_id} and telegramid: {message.from_user.id} containing {len(user_known_words)} words\n")
    if len(user_known_words) == 0:
        bot_message = "You don't have any words in your dictionary yet. Add some words first by writing /add!"
        send_bot_response(bot, message, [], base_language_code, bot_message)
        return
    else:
        bot_message = "Let's start! You can end the game at any time by writing <b>end</b>"
        send_bot_response(bot, message, [], base_language_code, bot_message)
        ask_to_translate_a_word(bot, message, user_known_words, base_language_code)
        

def ask_to_translate_a_word(bot, message, user_known_words, base_language_code):
    """
    Function that picks a random word from the user known words and asks the user to translate it

    args:
    bot: the bot object to send the message
    message: the message object from the user
    user_known_words: the list of words known by the user
    """
    random_word = random.choice(user_known_words)
    base_language_word = random_word[0]
    learning_language_word = random_word[1]
    bot_message = "Translate this word:"
    send_bot_response(bot, message, [], base_language_code, bot_message, base_language_word)
    bot.register_next_step_handler(message, lambda msg: check_response(msg, learning_language_word, bot, base_language_code, user_known_words))


def check_response(message, learning_language_word, bot, base_language_code, user_known_words):
    """
    Function that checks if the user response is correct or not

    args:
    message: the message object from the user
    learning_language_word: the correct translation of the word
    bot: the bot object to send the response
    """
    user_message = message.text.lower()
    if user_message == "end":
        send_bot_response(bot, message, [], base_language_code, "Ending the game! 🛑")
        return
    if user_message == learning_language_word.lower():
        send_bot_response(bot, message, [], base_language_code, "Correct!", "✅")
        # ask_to_translate_a_word(bot, message, user_known_words, base_language_code)
    else:
        send_bot_response(bot, message, [], base_language_code, "Incorrect! ❌\nThe translation is:", learning_language_word)
    ask_to_translate_a_word(bot, message, user_known_words, base_language_code)