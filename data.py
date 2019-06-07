import networkx as nx
import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
from staticmap import StaticMap, CircleMarker, Line

def precalculation():
    
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

def distance(i, j, position):
    return haversine(position[i], position[j]);
   

def geometric_graph(d):
    # Import station data.
    url_info = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    
    bicing = DataFrame.from_records(pd.read_json(url_info)['data']['stations'], index='station_id')
    bikes = DataFrame.from_records(pd.read_json(url_status)['data']['stations'], index='station_id')

    bikes = bikes[['num_bikes_available', 'num_docks_available']]

    origin_lat, origin_lon = min(bicing.lat), min(bicing.lon)
    end_lat, end_lon = max(bicing.lat), max(bicing.lon)
    
    cells_lat = (1 + end_lat - origin_lat)//d
    cells_lon = (1 + end_lon - origin_lon)//d
    grid = [[list() for j in range(cells_lon + 2)] for i in range(cells_lat + 1)]
    # grid[cells_lat][cells_lon]
    
    position = dict()

    for station in bicing.itertuples():
        position[station.index] = (station.lat, station.lon)

        distance_lat, distance_lon = station.lat - origin_lat, station.lon - origin_lon
        grid[1 + distance_lat//d][1 + distance_lon//d].append(station.index)
    
    G = nx.Graph()
    G.add_nodes_from(bicing.index)

    for i in range(cells_lat):
        for j in range(1, cells_lon + 1):
            for k in range(0, len(grid[i][j])):

                v = grid[i][j][k]

                for u in grid[i][j][k+1:] + grid[i][j+1][0:] + grid[i+1][j-1:j+2:1][0:]:
                    dist = distance(v, u, position)

                    if (dist <= d):
                        G.add_weighted_edges_from([(u, v, dist)])
                  
    return G, position, bicing, bikes



def distribute (requiredBikes, requiredDocks, G, bicing, bikes):
    nbikes = 'num_bikes_available'
    ndocks = 'num_docks_available'
    
    
    if (bikes[nbikes].sum() < requiredBikes * len(bikes.index)):
        return -3

    if (bikes[ndocks].sum() < requiredDocks * len(bikes.index)):
        return -2
    
    if (min(stations[capacity]) < requiredDocks + requiredBikes):
        return -1

    F = nx.DiGraph()
    F.add_nodes_from(G.nodes)

    for e in G.edges:
        d = G.get_edge_data(*e)['weight']
        F.add_weighted_edges_from([(e[0], e[1], d)])
        F.add_weighted_edges_from([(e[1], e[0], d)])
        

    F.add_node('TOP') # The green node
    demand = 0

    for st in bikes.itertuples():
        idx = st.Index
        stridx = str(idx)
        
        # The blue (s), black (g) and red (t) nodes of the graph
        s_idx, t_idx = 's'+stridx, 't'+stridx
            
        b, d = st.num_bikes_available, st.num_docks_available

        req_bikes = max(0, requiredBikes - b)
        req_docks = max(0, requiredDocks - d)

        F.add_node(s_idx, demand = -req_docks)
        F.add_node(t_idx, demand = req_bikes)
        
        demand += (req_bikes - req_docks)
        
        F.add_edge('TOP', s_idx)
        F.add_edge(t_idx, 'TOP')
        F.add_edge(s_idx, idx)
        F.add_edge(idx, t_idx)
        
    F.nodes['TOP']['demand'] = -demand


    err = False

    try:
        flowCost, flowDict = nx.network_simplex(F)

    except nx.NetworkXUnfeasible:
        err = True
        print("No solution could be found")

    except:
        err = True
        print("***************************************")
        print("*** Fatal error: Incorrect graph model ")
        print("***************************************")

    if not err:
        print("The total cost of transferring bikes is", flowCost/1000, "km.")

        # We update the status of the stations according to the calculated transportation of bicycles
        for src in flowDict:
            if src[0] != 'g': continue
            idx_src = int(src[1:])
            for dst, b in flowDict[src].items():
                if dst[0] == 'g' and b > 0:
                    idx_dst = int(dst[1:])
                    print(idx_src, "->", idx_dst, " ", b, "bikes, distance", F.edges[src, dst]['weight'])
                    bikes.at[idx_src, nbikes] -= b
                    bikes.at[idx_dst, nbikes] += b 
                    bikes.at[idx_src, ndocks] += b 
                    bikes.at[idx_dst, ndocks] -= b

    return flowCost


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

def ruta(addresses, G, position):
    position[-1], position[0] = addressesTOcoordinates(addresses)
    ratio = 10/4

    for e in G.edges:
        d = G.get_edge_data(*e)['weight']
        F.add_weighted_edges_from([(e[0], e[1], d)])
        
    
    F.add_edge(-1, 0, weight = ratio * distance(-1, 0, position))

    for a in F.nodes():
        if (a > 0):
            F.add_edge(0, a, weight = ratio * distance(0, a, position))
            F.add_edge(-1, a, weight = ratio * distance(-1, a, position))


    path = nx.dijkstra_path(F,-1,0)
    
    m = StaticMap(400, 500)

    last = int(-1)
    path[0] = 0
    path[len(path)-1] = -1
    time = int()

    for i in path:
        m.add_marker(CircleMarker(diccionari[i], 'red', 1))

        if (i != 0):
            coord1 = (diccionari[last], )
            coord2 = (diccionari[i], )

            if i == path[1] or i == -1:
                m.add_line(Line((coord1, coord2), 'green', 2))
                time += 10*haversine()

            else:
                m.add_line(Line((coord1, coord2), 'blue', 2))
                time += 4*haversine()
        
        last = i
        
      
    return m, time
