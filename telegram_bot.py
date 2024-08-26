import os
import telebot
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! type /info to get more information")


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "This is a telegram bot created with python")

@bot.message_handler(commands=['bye'])
def send_info(message):
    bot.reply_to(message, "Goodbye! Have a nice day")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print("Message received:" + message.text)
    bot.reply_to(message, message.text)

print("Bot is running")
bot.polling()