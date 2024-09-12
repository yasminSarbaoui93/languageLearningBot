import random
from telegram_bot import german_words
import telebot

#Function that gets the translation of a word taken from the dictionary
def get_translation(word):
    translation = german_words.get(word)
    return translation

#Function that checks if the user response is correct or not
def check_response(message, translation):
    print("User response: " + message.text)
    if message.text == translation:
        bot.reply_to(message, "Correct! ✅")
    else:
        bot.reply_to(message, "Incorrect! ❌")

# Function that asks the user to translate a random word from the dictionary
#@bot.message_handler(commands=['random'])
def send_random_word(bot, message):
    random_word = random.choice(list(german_words.keys()))
    translation = get_translation(random_word)
    print("Random word: " + random_word)
    bot.reply_to(message, f"Translate this word: {random_word}")
    #bot.register_next_step_handler(message, check_response(translation))
    bot.register_next_step_handler(message, lambda msg: check_response(msg, translation)) #Check better lambda function?
