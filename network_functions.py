import pandas as pd
from collections import defaultdict, deque

def setupUndirHeroGraph():
    # setup map for hero relationship searches
    hero_network_df = pd.read_csv("./hero-network.csv")

    # strip spaces from hero names
    hero_network_df["hero1"] = hero_network_df["hero1"].apply(lambda x: x.strip())
    hero_network_df["hero2"] = hero_network_df["hero2"].apply(lambda x: x.strip())

    # this is the map used for the BFS API
    undir_hero_map = defaultdict(set)

    for row in hero_network_df.index:
        hero1 = hero_network_df["hero1"][row]
        hero2 = hero_network_df["hero2"][row]
        
        undir_hero_map[hero1].add(hero2)
        undir_hero_map[hero2].add(hero1)

    return undir_hero_map

# basic BFS for getting hero degree of separation
# includes information about the links between the heroes specified

def hero_BFS(hero1, hero2, graph_map):    
    queue = deque()
    queue.append((hero1, [hero1]))
    seen = set([hero1])
    
    while(len(queue) > 0):
        curr_hero, hero_chain = queue.popleft()
        
        # if curr_hero is hero2, end loop
        if(curr_hero == hero2):
            return hero_chain
        
        # otherwise, add all unseen heroes to queue, with chain
        for new_hero in graph_map[curr_hero]:
            if(new_hero not in seen):
                new_hero_chain = hero_chain.copy()
                new_hero_chain.append(new_hero)
                
                queue.append((new_hero, new_hero_chain))
                
                seen.add(new_hero)
#     print(seen)
    return ["Not connected!"]

# basic BFS for getting all routes to hero at min. degree of separation
# includes information about the links between the heroes specified
# as an array of all possible paths

def all_paths_BFS(hero1, hero2, graph_map):    
    # stop at the minimum degree, and return all paths
    # that have hero2 as the last value
    min_degree = len(hero_BFS(hero1, hero2, graph_map))
    all_paths = []
    
    queue = deque()
    queue.append((hero1, [hero1]))
    seen = set([hero1])
    
    while(len(queue[0][1]) <= min_degree):
        curr_hero, hero_chain = queue.popleft()
        
        # if curr_hero is hero2, end loop
        if(curr_hero == hero2):
            all_paths.append(hero_chain)
        
        # otherwise, add all unseen heroes to queue, with chain
        for new_hero in graph_map[curr_hero]:
            if(new_hero not in seen or new_hero == hero2):
                new_hero_chain = hero_chain.copy()
                new_hero_chain.append(new_hero)
                
                queue.append((new_hero, new_hero_chain))
                
                seen.add(new_hero)
#     print(seen)
    return all_paths

# convert all shortest hero1 to hero2 paths to a sankey-friendly json format
def hero_paths_to_json(all_paths_arr):
    # degree of separation
    sep_degree = len(all_paths_arr[0])
    
    # all heroes present in the sankey, no duplicates
    heroes_seen = set([b for a in all_paths_arr for b in a])
    
    # index values are the node numbers in the json
    heroes_ordered = list(heroes_seen)
    
    # used for mapping hero names to indices - for output json
    hero_index_map = {}
    for i, hero in enumerate(heroes_ordered):
        hero_index_map[hero] = i
        
    # create nodes list of "objects" - first part of output json
    nodes = [{"name": hero, "node": i} for i, hero in enumerate(heroes_ordered)]
        
    # tuple dictionary for weighting flows/edges
    edge_dict = defaultdict(int)
    
    for arr in all_paths_arr:
        for i in range(sep_degree-1):
            from_hero = arr[i]
            to_hero = arr[i+1]
            edge_dict[(from_hero, to_hero)] += 1
        
    links = [{"source":hero_index_map[key[0]], "target":hero_index_map[key[1]], "value":value} for key, value in edge_dict.items()]
    
    output_to_json = {"nodes":nodes, "links":links}
    
    return output_to_json

# combine hero path search and json conversion into one function to export to app.py
def getSankeyResult(hero1, hero2, undir_hero_graph):
    # get all shortest paths from hero1 to hero2
    hero_relations = all_paths_BFS(hero1, hero2, undir_hero_graph)

    #convert to a sankey-friendly object
    output_json = hero_paths_to_json(hero_relations)

    return output_json