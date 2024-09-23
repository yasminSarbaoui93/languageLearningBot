#This file contains the function to add a new word to the dictionary
import pandas as pd
import os

english_term = ""
german_term = ""

# Function to add a new word to the dictionary, to be called from telegram_bot.py
def add_word(user_message, bot):
    ask_for_original_word(user_message, bot)    

# Function to register the word to be added to the dictionary
def ask_for_original_word(user_message, bot):
    bot.reply_to(user_message, f"Type the english word you want to add to the dictionary")
    bot.register_next_step_handler(user_message, lambda user_message: ask_for_translated_word(user_message, bot))

# Function to register the translation of the word to be added to the dictionary
def ask_for_translated_word(user_message, bot):
    # Save english term
    global english_term
    english_term = user_message.text

    # Ask for the translation
    bot.reply_to(
        user_message, f"Type the German translation of the word {english_term}"
    )
    bot.register_next_step_handler(user_message, lambda user_message: save_word(user_message, bot))    

# Function to save the new word to the csv
def save_word(user_message, bot):
    # Save german term
    global english_term, german_term
    german_term = user_message.text

    # Define and save full new word
    new_word = pd.DataFrame({"English": [english_term], "German": [german_term]})
    save_word_to_csv_file(new_word)

    # Reset global variables
    english_term = ""
    german_term = ""
        
    bot.reply_to(user_message, "The word has been added to the dictionary")

# Function to save the new word to the csv file
def save_word_to_csv_file(new_word):
    if os.path.exists("TermsList.csv"):
        terms_data = pd.read_csv("TermsList.csv", sep=";")
        terms_data = pd.concat([terms_data, new_word], ignore_index=True)
    else:
        terms_data = new_word
    terms_data.to_csv("TermsList.csv", sep=";", index=False)
