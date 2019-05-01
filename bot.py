import telegram
import networkx as nx
from telegram.ext import Updater
from telegram.ext import CommandHandler
from data import precalculation
from data import geometric_graph

def start(bot, update):
    global edge_list
    global G
    bot.send_message(chat_id = update.message.chat_id, text = "Hello!")
    edge_list, G = precalculation()


def authors(bot, update):
    global edge_list
    bot.send_message(chat_id = update.message.chat_id, text = "My creators are Maria Prat and Max Balsells (I dont know their official email yet)")


def nodes(bot, update):
	global G
	bot.send_message(chat_id = update.message.chat_id, text = G.number_of_nodes())

def edges(bot, update):
	global G
	bot.send_message(chat_id = update.message.chat_id, text = G.number_of_edges())


def graph(bot, update, args):
    try:
        x = int(args[0])
        global edge_list
        global G

        G = geometric_graph(edge_list, x, G)

        bot.send_message(chat_id=update.message.chat_id, text= "ok")

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')



TOKEN = open('token.txt').read().strip()

updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

edge_list = list()
G = nx.Graph()

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args = True))


updater.start_polling()