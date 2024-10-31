#This file contains the function to add a new word to the dictionary
import pandas as pd
import os
from wordRepository import delete_word_from_cosmos

nativelanguage_word = ""
translation = ""

# Function to add a new word to the dictionary, to be called from telegram_bot.py
def remove_word(user_message, bot):
    _ask_for_nativelanguage_word(user_message, bot)    


# Function to register the word to be added to the dictionary
def _ask_for_nativelanguage_word(user_message, bot):
    bot.reply_to(user_message, f"Type the english word you want to remove to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: _ask_for_translation(user_message, bot))


# Function to register the translation of the word to be added to the dictionary
def _ask_for_translation(user_message, bot):
    global nativelanguage_word
    nativelanguage_word = user_message.text
    bot.reply_to(
        user_message, f"Type the German translation of the word {nativelanguage_word}"
    )
    bot.register_next_step_handler(user_message, lambda user_message: _delete_word(user_message, bot))    


# Function to save the new word locally from the user text, save the pair with word and translation both to the csv and to cosmosDB
def _delete_word(user_message, bot):    
    global nativelanguage_word, translation
    translation = user_message.text
    _delete_word_from_csv_file(nativelanguage_word, translation)
    delete_word_from_cosmos(nativelanguage_word, translation)
    nativelanguage_word = ""
    translation = ""
    bot.reply_to(user_message, "The word has been deleted from your dictionary")


csv_name = "TermsList.csv"
#Function that, given new_word as input, it searches the pair in the csv file and deletes it
def _delete_word_from_csv_file(word_to_delete):
    word_to_delete = pd.DataFrame({"English": [nativelanguage_word], "German": [translation]})
    if os.path.exists(csv_name):
        terms_data = pd.read_csv(csv_name, sep=";")
        index = terms_data.index[(terms_data['English'] == word_to_delete['English'][0]) & (terms_data['German'] == word_to_delete['German'][0])].tolist()
        terms_data = terms_data.drop(index)
        terms_data.to_csv(csv_name, sep=";", index=False)
    else:
        print("The word is not in the dictionary")





