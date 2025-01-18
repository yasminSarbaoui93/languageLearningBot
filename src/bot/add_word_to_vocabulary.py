"""This file contains the function to be called by the bot to add a new word to the dictionary"""
from src.repository.vocabulary import save_word
from src.repository.vocabulary import get_or_create_user
from src.services.get_llm_response import llm_response, translate_sentence_with_llm
from src.services.detect_language import language_name_from_code

def add_word_to_dictionary(user_message, bot):
    """
    Function to add a new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    _ask_for_base_language_word(user_message, bot)    


def _ask_for_base_language_word(user_message, bot):
    """
    Function to ask the user for the word to be added to the dictionary
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    user = get_or_create_user(str(user_message.from_user.id), user_message.from_user.username, user_message.from_user.first_name, user_message.from_user.last_name)
    base_language_code = user.base_language
    base_language_name = language_name_from_code(base_language_code)
    bot_message_in_base_language = f"Type the word you want to add to the dictionary in your base language, <b>{base_language_name}</b>"
    if base_language_code != "en":
        bot_message_in_base_language = translate_sentence_with_llm(bot_message_in_base_language, base_language_code)

    bot.send_message(user_message.chat.id, bot_message_in_base_language, parse_mode='HTML')
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_learning_language_word(user_message, bot, user))


def _ask_for_learning_language_word(user_message, bot, user):
    """
    Function to ask the user for the translation in the learning language of the word to be added to the dictionary. This function I add because I prefer to put my own translation instead of the dictionary one (e.g. some might prefer using some dialect words instead of the official ones)
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    base_language_word = user_message.text
    base_language_code = user.base_language
    learning_language_name = language_name_from_code(user.learning_language)
    bot_message_in_base_language = f"Type the translation of the word {base_language_word} in the language you are learning, <b>{learning_language_name}</b>"
    if base_language_code != "en":
        bot_message_in_base_language = translate_sentence_with_llm(bot_message_in_base_language, base_language_code)
    bot.send_message(user_message.chat.id, bot_message_in_base_language, parse_mode='HTML')
    bot.register_next_step_handler(user_message, lambda user_message: _save_word_to_db(user_message, bot, base_language_word, base_language_code))    


def _save_word_to_db(user_message, bot, base_language_word, base_language_code):
    """
    Function to save the new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    learning_language_word = user_message.text
    user = get_or_create_user(str(user_message.from_user.id), user_message.from_user.username, user_message.from_user.first_name, user_message.from_user.last_name)
    user_id = user.id
    try:
        save_word(user_id, base_language_word, learning_language_word)
        bot_response_in_base_language = f"The word <b>{base_language_word}</b> = <b>{learning_language_word}</b> has been added to the dictionary"
        if base_language_code != "en":
            bot_response_in_base_language = translate_sentence_with_llm(bot_response_in_base_language, base_language_code)
        print(f"The word {base_language_word} = {learning_language_word} has been added to the dictionary for user {user_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
        bot_response_in_base_language = "The world could not be added to the dictionary"
        if base_language_code != "en":
            bot_response_in_base_language = translate_sentence_with_llm(bot_response_in_base_language, base_language_code)
    bot.send_message(user_message.chat.id, bot_response_in_base_language, parse_mode='HTML')
