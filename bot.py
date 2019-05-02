import telegram
from geopy.geocoders import Nominatim
import networkx as nx
from telegram.ext import Updater
from telegram.ext import CommandHandler
from data import precalculation
from data import geometric_graph
from data import ploting
from data import ruta
from data import addressesTOcoordinates
from staticmap import StaticMap, Line


def start(bot, update):
    global edge_list
    global G
    global diccionari
    edge_list, G, diccionari = precalculation()
    bot.send_message(chat_id = update.message.chat_id, text = "Hello!")


def authors(bot, update):
    global edge_list
    bot.send_message(chat_id = update.message.chat_id, text = "My creators are Maria Prat and Max Balsells (I dont know their official email yet)")


def nodes(bot, update):
    global G
    bot.send_message(chat_id = update.message.chat_id, text = G.number_of_nodes())

def components(bot, update):
    global G
    bot.send_message(chat_id = update.message.chat_id, text = nx.number_connected_components(G))

def edges(bot, update):
    global G
    bot.send_message(chat_id = update.message.chat_id, text = G.number_of_edges())


def plotgraph(bot, update):
    global G
    global diccionari
    global edge_list

    fitxer = 'map.png'

    m = ploting(G, diccionari)
    image = m.render(zoom = 12)
    image.save(fitxer)


    bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
    os.remove(fitxer)


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

def route(bot, update, args):
    try:
        x = " ".join(args)
        
        global edge_list
        global G

        fitxer = 'map1.png'

        m = ruta(x, G, diccionari)
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

edge_list = list()
G = nx.Graph()
diccionari = dict()

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph))
dispatcher.add_handler(CommandHandler('components', components))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args = True))
dispatcher.add_handler(CommandHandler('route', route, pass_args = True))


updater.start_polling()