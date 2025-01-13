#This file contains the functions that are used to get a random word from the dictionary and ask the user to translate it
import random
import os
import pandas as pd
from vocabulary import get_all_words
from dotenv import load_dotenv


load_dotenv()
user_id = os.getenv("USER_ID")
german_words = get_all_words(user_id)


#Function that checks if the user response is correct or not
def check_response(message, learning_language_word, bot):
    if message.text.lower() == learning_language_word.lower():
        bot.reply_to(message, "Correct! ✅")
    else:
        bot.reply_to(message, f"Incorrect! ❌\nThe correct translation is: <b>{learning_language_word}</b>", parse_mode='HTML')

# Function that asks the user to translate a random word from the dictionary
def send_random_word(bot, message):
    random_word = random.choice(german_words)
    native_language_word = random_word[0]
    learning_language_word = random_word[1]
    bot.reply_to(message, f"Translate this word: {native_language_word}")
    bot.register_next_step_handler(message, lambda msg: check_response(msg, learning_language_word, bot))