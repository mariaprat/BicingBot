import networkx as nx
import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
from staticmap import StaticMap, CircleMarker, Line

def precalculation():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    
    diccionari = dict()
    G = nx.Graph()
    edge_list = list()

    for i in bicing.itertuples():
        diccionari[i.Index] = (i.lon, i.lat)
        G.add_node(i.Index)
        for j in bicing[bicing.index > i.Index].itertuples():
            edge_list.append((haversine((i.lat, i.lon), (j.lat, j.lon)), i.Index, j.Index))

    edge_list.sort()
    
    return edge_list, G, diccionari

def geometric_graph(edge_list, d, F):
    G = nx.Graph()
    G.add_nodes_from(F.nodes)
    
    i = 0
    while edge_list[i][0] < d/1000:
        i = i + 1
        G.add_edge(edge_list[i][1], edge_list[i][2], weight = edge_list[i][0])

    return G

def ploting(G, diccionari):
    m = StaticMap(400, 500)
    
    for i in G.nodes():
        m.add_marker(CircleMarker(diccionari[i], 'red', 1))

    for j in G.edges():
        coord1 = diccionari[j[0]]
        coord2 = diccionari[j[1]]

        m.add_line(Line((coord1, coord2), 'blue', 2))

    
    return m

def addressesTOcoordinates(addresses):
    try:
        geolocator = Nominatim(user_agent="bicing_bot")
        address1, address2 = addresses.split(',')
        location1 = geolocator.geocode(address1 + ', Barcelona')
        location2 = geolocator.geocode(address2 + ', Barcelona')
        return (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)
    except:
        return None

def ruta(addresses, F, diccionari):
    coordinates = addressesTOcoordinates(addresses)
    ratio = 10/4

    G = nx.Graph()
    for i in F.edges:
        coord1 = (diccionari[i[0]][1], diccionari[i[0]][0])
        coord2 = (diccionari[i[1]][1], diccionari[i[1]][0])

        G.add_edge(i[0], i[1], weight = haversine(coord1, coord2))

    G.add_node(-1) #start
    G.add_node(0)  #terminal

    diccionari[-1] = (coordinates[0][1], coordinates[0][0])
    diccionari[0] = (coordinates[1][1], coordinates[1][0])

    coords = coordinates[0]
    coordt = coordinates[1]
    
    G.add_edge(-1, 0, weight = ratio*haversine(coords, coordt))

    for a in G.nodes():
        if (a > 0):
            coord = (diccionari[a][1], diccionari[a][0])
             
            G.add_edge(0, a, weight = ratio*haversine(coords, coord))
            G.add_edge(-1, a, weight = ratio*haversine(coordt, coord))


    path = nx.dijkstra_path(G,-1,0)
    
    m = StaticMap(400, 500)

    last = int(-1)
    path[0] = 0
    path[len(path)-1] = -1

    for i in path:
        m.add_marker(CircleMarker(diccionari[i], 'red', 1))

        if (i != 0):
            coord1 = diccionari[last]
            coord2 = diccionari[i]

            if i == path[1] or i == -1:
                m.add_line(Line((coord1, coord2), 'green', 2))

            else:
                m.add_line(Line((coord1, coord2), 'blue', 2))
        
        last = i
        
      
    return m




