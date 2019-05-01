import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from data import precalculation
from data import geometric_graph

def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hello!")
    return precalculation()

def authors(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "My creators are Maria Prat and Max Balsells (I dont know their official email yet)")

def graf(bot, update, args):
	global edge_list
	distance = int(args[0])

	G = geometric_graph(edge_list)
	bot.send_message(chat_id = update.message.chat_id, text = "okay")

	return G


def nodes(bot, update):
	bot.send_message(chat_id = update.message.chat_id, text = G.number_of_nodes())



TOKEN = open('token.txt').read().strip()

updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

edge_list = dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('authors', authors))
G = dispatcher.add_handler(CommandHandler('graf', graf, pass_args = True))
dispatcher = dispatcher.add_handler(CommandHandler('nodes', nodes))


updater.start_polling()