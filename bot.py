import telegram
from geopy.geocoders import Nominatim
import networkx as nx
from telegram.ext import Updater
from telegram.ext import CommandHandler
from staticmap import StaticMap, Line

from data import *

#user_data (edge_list, G, diccionari)

def start(bot, update, user_data):
    user_data['edge_list'], user_data['G'], user_data['diccionari'] = precalculation();
    bot.send_message(chat_id = update.message.chat_id, text = "Hello!")


def authors(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "My creators are Maria Prat and Max Balsells their emails are respectively maria.prat@est.fib.upc.edu and max.balsells.i@est.fib.upc.edu")


def nodes(bot, update, user_data):
    bot.send_message(chat_id = update.message.chat_id, text = user_data['G'].number_of_nodes())

def components(bot, update, user_data):
    bot.send_message(chat_id = update.message.chat_id, text = nx.number_connected_components(user_data['G']))

def edges(bot, update, user_data):
    bot.send_message(chat_id = update.message.chat_id, text = user_data['G'].number_of_edges())


def plotgraph(bot, update, user_data):
    fitxer = 'map.png'

    m = ploting(user_data['G'], user_data['diccionari'])
    image = m.render(zoom = 12)
    image.save(fitxer)

    bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
    os.remove(fitxer)


def graph(bot, update, args, user_data):
    try:
        x = int(args[0])

        user_data['G'] = geometric_graph(user_data['edge_list'], x, user_data['G'])
        bot.send_message(chat_id=update.message.chat_id, text= "ok")

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')

def route(bot, update, args, user_data):
    try:
        x = " ".join(args)

        fitxer = 'map1.png'

        m = ruta(x, user_data['G'], user_data['diccionari'])
        image = m.render(zoom = 12)
        image.save(fitxer)

        bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
        bot.send_message(chat_id=update.message.chat_id, text= "ok")
        #os.remove(fitxer) whyyyyy

    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


TOKEN = open('token.txt').read().strip()

updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args = True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args = True, pass_user_data=True))


updater.start_polling()