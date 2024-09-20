import pandas as pd
import os


english_term = ""
german_term = ""


def add_word(message, bot):
    bot.reply_to(message, f"Type the english word you want to add to the dictionary")
    bot_reply = bot.register_next_step_handler(message, lambda msg: register_word(msg, bot))
    #bot.reply_to(bot_reply, "The word has been added to the dictionary")


def register_word(user_message, bot):
    # check if english term is empty
    if english_term == "":
        english_term = user_message.text
        bot.reply_to(
            user_message, f"Type the German translation of the word {english_term}"
        )
        bot.register_next_step_handler(user_message, lambda msg: register_word(msg))
    else:
        german_term = user_message.text
        new_word = pd.DataFrame({"English": [english_term], "German": [german_term]})
        english_term = ""
        german_term = ""
        save_word(new_word)


def save_word(new_word):
    if os.path.exists("TermsList.csv"):
        terms_data = pd.read_csv("TermsList.csv", sep=";")
        terms_data = terms_data.append(new_word, ignore_index=True)
    else:
        terms_data = new_word
    terms_data.to_csv("TermsList.csv", sep=";", index=False)
