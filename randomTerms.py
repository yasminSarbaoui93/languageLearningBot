#This file contains the functions that are used to get a random word from the dictionary and ask 
#the user to translate it
import random

#Function that gets the translation of a word taken from the dictionary
def get_translation(word, german_words):
    translation = german_words.get(word)
    return translation

#Function that checks if the user response is correct or not
def check_response(message, translation, bot):
    print("User response: " + message.text)
    if message.text == translation:
        bot.reply_to(message, "Correct! ✅")
    else:
        bot.reply_to(message, "Incorrect! ❌")

# Function that asks the user to translate a random word from the dictionary
def send_random_word(bot, message, german_words):
    random_word = random.choice(list(german_words.keys()))
    translation = get_translation(random_word, german_words)
    print("Random word: " + random_word)
    bot.reply_to(message, f"Translate this word: {random_word}")
    #bot.register_next_step_handler(message, check_response(translation))
    bot.register_next_step_handler(message, lambda msg: check_response(msg, translation, bot)) #Check better lambda function?
