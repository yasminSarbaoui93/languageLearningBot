"""This file contains the function to be called by the bot to add a new word to the dictionary"""
import os
from src.repository.vocabulary import save_word
from src.repository.vocabulary import get_all_words, get_or_create_user_id_in_DB


base_language_word = ""
learning_language_word = ""


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
    #bot.reply_to(user_message, f"Type the english word you want to add to the dictionary")
    bot.send_message(user_message.chat.id, f"Type the word you want to add to the dictionary in your <b>base language</b>", parse_mode='HTML')
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_learninig_language_word(user_message, bot))


def _ask_for_learninig_language_word(user_message, bot):
    """
    Function to ask the user for the translation in the larning language of the word to be added to the dictionary. This function I add because I prefer to put my own translation instead of the dictionary one (e.g. some might prefer using some dialect words instead of the official ones)
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    global base_language_word
    base_language_word = user_message.text
    #bot.reply_to(user_message, f"Type the German learning_language_word of the word {base_language_word}")
    bot.send_message(user_message.chat.id, f"Type the translation of the word {base_language_word} in the <b>language you are learning</b>", parse_mode='HTML')
    bot.register_next_step_handler(user_message, lambda user_message: _save_word_to_db(user_message, bot))    


def _save_word_to_db(user_message, bot):
    """
    Function to save the new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    global base_language_word, learning_language_word
    learning_language_word = user_message.text
    user_id = get_or_create_user_id_in_DB(str(user_message.from_user.id), user_message.from_user.username, user_message.from_user.first_name, user_message.from_user.last_name)
    try:
        save_word(user_id, base_language_word, learning_language_word)
        bot_response = f"The word <b>{base_language_word}</b> = <b>{learning_language_word}</b> has been added to the dictionary"
        print(f"The word {base_language_word} = {learning_language_word} has been added to the dictionary for user {user_id}")
    except Exception as e:
        print(f"An error occurred: {e}")
        bot_response = e
    base_language_word = ""
    learning_language_word = ""
    bot.send_message(user_message.chat.id, bot_response, parse_mode='HTML')
