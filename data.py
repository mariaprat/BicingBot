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


