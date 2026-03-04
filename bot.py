import telebot

bot = telebot.TeleBot("8445389309:AAHAbg6ahLCp-WVyYnYkOaO6cnWphspAJAE")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Test bot ishlayapti ✅")

bot.polling()