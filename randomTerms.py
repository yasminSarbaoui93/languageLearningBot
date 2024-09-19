#This file contains the functions that are used to get a random word from the dictionary and ask the user to translate it
import random
import os
import pandas as pd


#read csv file with panda
german_words = pd.read_csv('TermsList.csv',sep=';')
test_random_word = random.choice(german_words['English'])


#Function that gets the translation of a word taken from the csv dictionary
def get_translation(word):
    index = german_words[german_words['English'] == word].index[0]
    translation = german_words.at[index, 'German']
    return translation


#Function that checks if the user response is correct or not
def check_response(message, translation, bot):
    if message.text.lower() == translation.lower():
        bot.reply_to(message, "Correct! ✅")
    else:
        bot.reply_to(message, "Incorrect! ❌")

# Function that asks the user to translate a random word from the dictionary
def send_random_word(bot, message):
    random_word = random.choice(german_words['English'])
    translation = get_translation(random_word)
    bot.reply_to(message, f"Translate this word: {random_word}")
    bot.register_next_step_handler(message, lambda msg: check_response(msg, translation, bot))