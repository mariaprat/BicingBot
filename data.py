import networkx as nx
import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim

def precalculation():
    url = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    bicing = DataFrame.from_records(pd.read_json(url)['data']['stations'], index='station_id')
    
    edge_list = list()

    for i in bicing.itertuples(): 
        for j in bicing[bicing.index > i.Index].itertuples():
    	    edge_list.append((haversine((i.lat, i.lon), (j.lat, j.lon)), i.Index, j.Index))

    edge_list.sort()
    return edge_list

def geometric_graph(edge_list, d):
	print("here we are")
	print(len(edge_list))

	G = nx.Graph()

	i = 0
	while edge_list[i][0] < d/1000:
		print(i)
		G.add_edge(edge_list[i][1], edge_list[i][2], weight = edge_list[i][0])

	print(G.number_of_nodes())
	return G

#A = precalculation()
#G = geometric_graph(A, 500)

# This function constructs a geometic graph given the distance d
#def construct(G, d):




#def dijkstra(G):
    



