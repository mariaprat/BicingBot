import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hello!")

def authors(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "My creators are Maria Prat and Max Balsells (I dont know their official email yet)")

def graf(bot, update):
	distance = int(input())
	

# declara una constant amb el access token que llegeix de token.txt
TOKEN = open('token.txt').read().strip()

# crea objectes per treballar amb Telegram
updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

# indica que quan el bot rebi la comanda /start s'executi la funció start
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('graf', graf))

# engega el bot
updater.start_polling()