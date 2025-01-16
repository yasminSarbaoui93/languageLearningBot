"""This file contains the function to be called by the bot to add a new word to the dictionary"""
import os
from src.repository.vocabulary import save_word

nativelanguage_word = ""
translation = ""


def add_word_to_dictionary(user_message, bot):
    """
    Function to add a new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    _ask_for_original_word(user_message, bot)    


def _ask_for_original_word(user_message, bot):
    """
    Function to ask the user for the word to be added to the dictionary
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    #bot.reply_to(user_message, f"Type the english word you want to add to the dictionary")
    bot.send_message(user_message.chat.id, f"Type the english word you want to add to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_translated_word(user_message, bot))


def _ask_for_translated_word(user_message, bot):
    """
    Function to ask the user for the translation of the word to be added to the dictionary
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    global nativelanguage_word
    nativelanguage_word = user_message.text
    #bot.reply_to(user_message, f"Type the German translation of the word {nativelanguage_word}")
    bot.send_message(user_message.chat.id, f"Type the German translation of the word {nativelanguage_word}")
    bot.register_next_step_handler(user_message, lambda user_message: _save_word_to_db(user_message, bot))    


def _save_word_to_db(user_message, bot):
    """
    Function to save the new word to the dictionary in CosmosDB
    
    args:
    user_message: the message object from the user
    bot: the bot object to send the message
    """
    global nativelanguage_word, translation
    translation = user_message.text
    
    try:
        save_word(nativelanguage_word, translation)
        bot_response = f"The word <b>{nativelanguage_word}</b> has been added to the dictionary"
    except Exception as e:
        print(f"An error occurred: {e}")
        bot_response = f"Sorry, an error occurred while trying to save the word."



    nativelanguage_word = ""
    translation = ""
    print(f"chat id= {user_message.chat.id}")
    print(f"user id= {user_message.from_user.id}")
    print(f"username= {user_message.from_user.username}")
    print(f"name= {user_message.from_user.first_name}")
    print(f"last name= {user_message.from_user.last_name}")
    print(f"number= {user_message.from_user.phone_number}")


    bot.send_message(user_message.chat.id, bot_response, parse_mode='HTML')
