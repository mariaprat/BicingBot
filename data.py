import networkx as nx
import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim

def precalculation():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    
    G = nx.Graph()
    edge_list = list()

    for i in bicing.itertuples(): 
        G.add_node(i.Index)
        for j in bicing[bicing.index > i.Index].itertuples():
    	    edge_list.append((haversine((i.lat, i.lon), (j.lat, j.lon)), i.Index, j.Index))

    edge_list.sort()

    return edge_list, G

def geometric_graph(edge_list, d, F):
	G = nx.Graph()
	G.add_nodes_from(F.nodes)

	i = 0
	while edge_list[i][0] < d/1000:
		i = i + 1
		G.add_edge(edge_list[i][1], edge_list[i][2], weight = edge_list[i][0])

	return G


#A = precalculation(G)
#G = geometric_graph(A, 500)

# This function constructs a geometic graph given the distance d
#def construct(G, d):




#def dijkstra(G):
    



