import telegram
import os
from geopy.geocoders import Nominatim
import networkx as nx
from telegram.ext import Updater
from telegram.ext import CommandHandler
from staticmap import StaticMap, Line

from data import *

def message (bot, update, s):
    bot.send_message(chat_id = update.message.chat_id, text = s)
        

def is_int(x):
    try: 
        int(x)
        return True
    except ValueError: 
        return False


def start(bot, update, user_data):
    name =  update.message.chat.first_name
    text = "Hello, %s! Do you need something? I'm deBOTed to you." % (name)
    message(bot, update, text)
    

def authors(bot, update):
    message1 = "My creators are Maria Prat and Max Balsells. \n"
    message2 = "Their emails are respectively maria.prat@est.fib.upc.edu and max.balsells.i@est.fib.upc.edu. "
    message(bot, update, str(message1 + message2))
    

def helpp(bot, update):
    initial = "This bot helps you to use Bicing in Barcelona. \n"
    start = "Use /start to get a welcome message. \n"
    authors = "Use /authors to get information about my authors. \n"
    graph = "Use /graph <distance> to initialize a new graph with up-to-date data. Two stations will be connected the distance between them is less than <distance> (in meters). \n"
    nodes = "Use /nodes to get the number of stations in the current graph. \n"
    edges = "Use /edges to get the number of connections between stations in the current graph. \n"
    components = "Use /components to get the number of connected components in the current graph. \n"
    plotgraph = "Use /plotgraph to create a map with all the stations and connections between them. \n"
    route = "Use /route <origin>, <destiny> to create a map with the faster route between <origin> and <destiny>. \n"
    text = initial + start + authors + graph + nodes + edges + components + plotgraph + route
    message(bot, update, text)


def nodes(bot, update, user_data):
    if 'G' in user_data: message(bot, update, user_data['G'].number_of_nodes())
    else: message(bot, update, "You must first construct the geometric graph")

def components(bot, update, user_data):
    if 'G' in user_data: message(bot, update, nx.number_connected_components(user_data['G']))
    else: message(bot, update, "You must first construct the geometric graph")

def edges(bot, update, user_data):
    if 'G' in user_data: message(bot, update, user_data['G'].number_of_edges())
    else: message(bot, update, "You must first construct the geometric graph")

def plotgraph(bot, update, user_data):
    if 'G' in user_data:
        fitxer = "plotgraph_" + str(update.message.chat_id) + ".png"

        m = ploting(user_data['G'], user_data['position'])
        image = m.render(zoom = 12)
        image.save(fitxer)

        bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
        os.remove(fitxer)

    else: message(bot, update, "You must first construct the geometric graph")


def graph(bot, update, args, user_data): # CAUTION:: small distances make it eternaly slow
    try:
        if (len(args) == 0): args.append(1000)
        if (not is_int(args[0])): message(bot, update, "You should introduce a number")
        elif (int(args[0]) <= 0): message(bot, update, "You should introduce a positive number")

        else:
            user_data['G'], user_data['position'], user_data['bicing'], user_data['bikes'] = geometric_graph(int(args[0]))
            message(bot, update, "Graph constructed successfully")

    except Exception as e:
        print(e)
        message (bot, update, "Unexpected error. You can report the error to the authors via mail")
    
def route(bot, update, args, user_data):
    if 'G' in user_data:
        try:
            m, time = unchecked_route(" ".join(args), user_data['G'], user_data['position'])

            if (time == -1):
                bot.send_message(chat_id=update.message.chat_id, text= m)
            else:
                fitxer = "route_" + str(update.message.chat_id) + ".png"
                image = m.render(zoom = 12)
                image.save(fitxer)

                bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
                message (bot, update, "If you follow this rute you will arrive at your destination in {} minutes".format(time))
                os.remove(fitxer)
            
        except Exception as e:
            print(e)
            message (bot, update, "Unexpected error. You can report the error to the authors via mail")
    
    else: message(bot, update, "You must first construct the geometric graph")

def valid_route(bot, update, args, user_data):
    if 'G' in user_data:
        try:
            m, time = true_route(" ".join(args), user_data['G'], user_data['position'])

            if (time == -1):
                bot.send_message(chat_id=update.message.chat_id, text= m)
            else:
                fitxer = "valid_route_" + str(update.message.chat_id) + ".png"
                image = m.render(zoom = 12)
                image.save(fitxer)

                bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
                bot.send_message(chat_id=update.message.chat_id, text= "If you follow this rute you will arrive at your destination in {} minutes".format(time))
                os.remove(fitxer)

        except Exception as e:
            print(e)
            message (bot, update, "Unexpected error. You can report the error to the authors via mail")
    
    else: message(bot, update, "You must first construct the geometric graph")

def distribute(bot, update, args, user_data):
    if 'G' in user_data:
        try:
            if (len(args) < 2): message(bot, update, "You should introduce two numbers")
            elif (not is_int(args[0] or not is_int(arg[1]))): message(bot, update, "You should introduce two numbers")
            elif (int(args[0]) < 0 or int(args[1]) < 0): message(bot, update, "You should introduce two non negative numbers")

            else:
                cost, information = distribution(int(args[0]), int(args[1]), user_data['G'], user_data['bicing'], user_data['bikes'])
                if (cost > 0): message(bot, update, "Total cost of transferring bicycles: {} km".format(cost))
                message(bot, update, information)

        except Exception as e:
            print(e)
            message (bot, update, "Unexpected error. You can report the error to the authors via mail")
    
    else: message(bot, update, "You must first construct the geometric graph")


TOKEN = open('token.txt').read().strip()

updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', helpp))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args = True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args = True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('valid_route', valid_route, pass_args = True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('distribute', distribute, pass_args = True, pass_user_data=True))


updater.start_polling()
