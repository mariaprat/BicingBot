import networkx as nx
import pandas as pd
from pandas import DataFrame
from haversine import haversine
from geopy.geocoders import Nominatim
from staticmap import StaticMap, CircleMarker, Line

# Given a dictionary (position) int --> (latitude, longitude) and two integers: i,j
# computes the distance of position[i], poistion[j] in meters
def distance(i, j, position):
    return haversine(position[i], position[j])*1000;

# Given a pair, swaps its components
def swap(p):
    return (p[1], p[0])


def geometric_graph(d):
    # Import station data.
    url_info = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'
    url_status = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_status'
    
    bicing = DataFrame.from_records(pd.read_json(url_info)['data']['stations'], index='station_id')
    bikes = DataFrame.from_records(pd.read_json(url_status)['data']['stations'], index='station_id')

    bikes = bikes[['num_bikes_available', 'num_docks_available']]
    
    origin_lat, origin_lon = min(bicing.lat), min(bicing.lon)
    end_lat, end_lon = max(bicing.lat), max(bicing.lon)

    ratio_lat = d/(1000*haversine((10,30),(11,30)))
    ratio_lon = d/(1000*haversine((end_lat, 10),(end_lat, 11)))
    #ratio_lat represents how many degrees of latitude has distance d
    #ratio_lon represents how many degrees of longitude has distance d 

    cells_lat = int((ratio_lat/2 + end_lat - origin_lat)/ratio_lat)
    cells_lon = int((ratio_lon/2 + end_lon - origin_lon)/ratio_lon)
    grid = [[list() for j in range(cells_lon + 2)] for i in range(cells_lat + 1)]
    # grid[cells_lat][cells_lon]

    position = dict()

    for station in bicing.itertuples():
        position[station.Index] = (station.lat, station.lon)
        distance_lat, distance_lon = station.lat - origin_lat, station.lon - origin_lon
        grid[int(distance_lat/ratio_lat)][int(1 + distance_lon/ratio_lon)].append(station.Index)
    
    G = nx.Graph()
    G.add_nodes_from(bicing.index)

    for i in range(cells_lat):
        for j in range(1, cells_lon + 1):
            for k in range(0, len(grid[i][j])):
                
                v = grid[i][j][k]
                
                #+ grid[i+1][j-1:j+2:1][0:][(x, y) for x in [1,2,3] for y in [3,1,4] if x != y]
                for u in grid[i][j][k+1:] + grid[i][j+1][0:] + grid[i+1][j-1][0:] + grid[i+1][j][0:] + grid[i+1][j+1][0:]:
                    dist = distance(v, u, position)
                    
                    if (dist <= d):
                        G.add_weighted_edges_from([(u, v, dist)])


    return G, position, bicing, bikes



def distribution (requiredBikes, requiredDocks, G, bicing, bikes): #IMPORTANT: CHECK ISOLATED VERTICES
    nbikes = 'num_bikes_available'
    ndocks = 'num_docks_available'
    
    if (bikes[nbikes].sum() < requiredBikes * len(bikes.index)):
        return 0, "There are not so many bicicles!"

    if (bikes[ndocks].sum() < requiredDocks * len(bikes.index)):
        return 0, "There are not so many docks!"
    
    if (min(bicing['capacity']) < requiredDocks + requiredBikes):
        return 0, "There are stations whose capacity is less than " + str(requiredDocks + requiredBikes)

    F = nx.DiGraph()
    
    for v in G.nodes:
        F.add_node('g' + str(v))

    for e in G.edges:
        d = G.get_edge_data(*e)['weight']
        F.add_edge('g' + str(e[0]), 'g' + str(e[1]), weight = int(d))
        F.add_edge('g' + str(e[1]), 'g' + str(e[0]), weight = int(d))
    
    F.add_node('TOP') # The green node
    demand = 0

    for st in bicing.itertuples():
        idx = st.Index
        stridx = str(idx)
        if idx not in bikes.index: 
            F.remove_node(stridx) 

    for st in bikes.itertuples():
        idx = st.Index
        stridx = 'g' + str(idx)
        if idx not in bicing.index: continue
        
        # The blue (s), black (g) and red (t) nodes of the graph
        s_idx, t_idx = 's'+stridx, 't'+stridx
            
        b, d = st.num_bikes_available, st.num_docks_available

        req_bikes = max(0, requiredBikes - b)
        req_docks = max(0, requiredDocks - d)

        F.add_node(s_idx, demand = -req_docks)
        F.add_node(t_idx, demand = req_bikes)
        
        demand += (req_bikes - req_docks)

        bluecap = max(0, b - requiredBikes)
        redcap = max(0, d - requiredDocks)

        F.add_edge('TOP', s_idx)
        F.add_edge(t_idx, 'TOP')
        F.add_edge(s_idx, stridx, capacity = bluecap)
        F.add_edge(stridx, t_idx, capacity = redcap)
        
    F.nodes['TOP']['demand'] = -demand

    err = False

    flowCost = float(1)
    flowDict = dict()
    information = str()
    maxdistance = int(-1)

    try:
        flowCost, flowDict = nx.network_simplex(F)
        
    except nx.NetworkXUnfeasible:
        return 0, "No solution could be found"

    
    # We update the status of the stations according to the calculated transportation of bicycles
    if (flowCost == 0): return 0, "All stations satisfy the conditions"

    for src in flowDict:
        if src[0] != 'g': continue
        idx_src = int(src[1:])
        for dst, b in flowDict[src].items():
            if dst[0] == 'g' and b > 0:
                idx_dst = int(dst[1:])
                
                if (b * F.edges[src, dst]['weight'] > maxdistance):
                    information = "The edge with greatest cost is " + str(idx_src) + " -> " + str(idx_dst) + ": " + str(b) + " bikes, distance " + str(F.edges[src, dst]['weight']) + "m"
                    maxdistance = b * F.edges[src, dst]['weight']

                bikes.at[idx_src, nbikes] -= b
                bikes.at[idx_dst, nbikes] += b 
                bikes.at[idx_src, ndocks] += b 
                bikes.at[idx_dst, ndocks] -= b

    
    return flowCost/1000, information


def ploting(G, position):
    m = StaticMap(400, 500)

    for i in G.nodes():
        m.add_marker(CircleMarker(swap(position[i]), 'red', 1))

    for j in G.edges():
        coord1 = swap(position[j[0]])
        coord2 = swap(position[j[1]])

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

def dijkstra_route(G, position):
    m = StaticMap(400, 500)

    last = int(-1)
    time = int(0)

    path = nx.dijkstra_path(G, -1, 0)
    for i in path:
        m.add_marker(CircleMarker(swap(position[i]), 'red', 1))

        if (i != -1):
            coord1 = swap(position[last])
            coord2 = swap(position[i])
            e = (last, i)
            time += G.get_edge_data(*e)['weight']

            if i == path[1] or i == -1:
                m.add_line(Line((coord1, coord2), 'green', 2))
                
            else:
                m.add_line(Line((coord1, coord2), 'blue', 2))
                
        last = i
        
    return m, int(time)


def unchecked_route(addresses, G, position):
    position[-1], position[0] = addressesTOcoordinates(addresses)
    
    F = nx.Graph()
    #weight is the time in minutes
    
    for e in G.edges:
        d = G.get_edge_data(*e)['weight']
        F.add_edge(e[0], e[1], weight = 0.006 * d)
    
    F.add_edge(-1, 0, weight = 0.015 * distance(-1, 0, position))

    for a in F.nodes():
        if (a > 0):
            F.add_edge(0, a, weight = 0.015 * distance(0, a, position))
            F.add_edge(-1, a, weight = 0.015 * distance(-1, a, position))

    return dijkstra_route(F, position)

def true_route(addresses, G, position, bikes):
    position[-1], position[0] = addressesTOcoordinates(addresses)
    
    F = nx.Graph()
    #weight is the time in minutes

    bikes_info = [0] * (1 + bikes.tail(1).index.item()) 
    # 0 means no information, 1 means no bikes, 2 means no docks, else 3

    for st in bikes.itertuples():
        idx = st.Index
        b, d = st.num_bikes_available, st.num_docks_available

        if (b == 0): bikes_info[idx] = 1
        elif (d == 0): bikes_info[idx] = 2
        else: bikes_info[idx] = 3 

    for e in G.edges:
        d = G.get_edge_data(*e)['weight']
        F.add_edge(e[0], e[1], weight = 0.006 * d)

    
    F.add_edge(-1, 0, weight = 0.015 * distance(-1, 0, position))

    for a in F.nodes():
        if (a > 0 and bikes_info[a] != 0):
            if (bikes_info[a] != 2): F.add_edge(0, a, weight = 0.015 * distance(0, a, position))
            if (bikes_info[a] != 1): F.add_edge(-1, a, weight = 0.015 * distance(-1, a, position))

    return dijkstra_route(F, position)

