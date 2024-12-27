import networkx as nx
import matplotlib.pyplot as plt
from copy import deepcopy
from collections import deque
import heapq

class TravelingEthiopia:

    def __init__(self,cities,roads):
        self.cities = cities
        self.roads = roads
        self.G = self.__create_graph()

    def __create_graph(self):
        G = nx.Graph()
        G.add_nodes_from(cities)
        for city in self.roads:
            for neigh,weight in roads[city]:
                G.add_edge(city,neigh, weight=weight)
        return G
    
    def highlight_path(self, path):
        node_colors = []
        edge_colors = []
        edge_widths = []
        for node in self.G.nodes():
            node_colors.append("red" if node in path else "blue")
        for u, v in self.G.edges():
            edge_colors.append("red" if (u,v) in zip(path, path[1:]) else "black")
            edge_widths.append(3 if (u, v) in zip(path, path[1:]) else 1)

        pos = nx.circular_layout(self.G) 
        nx.draw(self.G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, width=edge_widths)
        plt.show()
    
    def uninformed_path_finder(self,start_city, goal_city, strategy):
        visited = set()
        def dfs(start_city, goal_city, total_dist, path):
            if start_city in visited:
                return ([], 0)
            path.append(start_city)
            visited.add(start_city)
            if(start_city == goal_city):
                return (deepcopy(path), total_dist)
            for neigh in self.roads[start_city]:
                path_found,dist = dfs(neigh[0],goal_city,total_dist+neigh[1],path)
                if(len(path_found) != 0):
                    return (path_found,dist)
            path.pop()
        
        def bfs(start_city, goal_city):
            q = deque()
            q.append(([start_city],0))
            visited.add(start_city)
            while q:
                curr_path,dist = q.popleft()
                last_city = curr_path[-1]
                if(last_city == goal_city):
                    return (curr_path,dist)
                for neigh,next_dist in self.roads[last_city]:
                    if neigh not in visited:
                        visited.add(neigh)
                        new_path = deepcopy(curr_path)
                        new_path.append(neigh)
                        q.append((new_path,dist+next_dist))
        def dijkstra(start_city, goal_city):
            min_heap = []
            heapq.heappush(min_heap,(0, [start_city]))
            while min_heap:
                dist,curr_path = heapq.heappop(min_heap)
                last_city = curr_path[-1]
                if(last_city == goal_city):
                    return (curr_path,dist)
                for neigh,next_dist in roads[last_city]:
                    if neigh not in visited:
                        visited.add(neigh)
                        new_path = deepcopy(curr_path)
                        new_path.append(neigh)
                        heapq.heappush(min_heap,(dist+next_dist,new_path))
        result = None 
        if(strategy == 'bfs'):
            result = bfs(start_city,goal_city)
        elif(strategy == 'dfs'):
            result = dfs(start_city,goal_city,0,[])
        elif strategy == 'dijkstra':
            result = dijkstra(start_city,goal_city)
        self.highlight_path(result[0])
        return result
        
    def traverse_all_cities(self,cities, roads, start_city, strategy):
        visited = set()
        path = []
        def dfs(start_city):
            if start_city in visited:
                return 0
            visited.add(start_city)
            path.append(start_city)
            total_dist = 0
            for neigh in self.roads[start_city]:
                total_dist += dfs(neigh[0])
            return total_dist
        def bfs(start_city):
            q = deque()
            q.append(start_city)
            visited.add(start_city)
            total_dist = 0
            while q:
                curr_city = q.popleft()
                path.append(curr_city)
                for neigh,next_dist in self.roads[curr_city]:
                    if neigh not in visited:
                        visited.add(neigh)
                        q.append(neigh)
                        total_dist+=next_dist
            return (path,total_dist)
        result = None
        if strategy == 'dfs':
            result = (path,dfs(start_city))
        elif strategy == 'bfs':
            result =  bfs(start_city)  
        self.highlight_path(result[0])
        return result
    
    def k_shortest_paths(self,start_city,goal_city,k):
        k_paths = []
        min_heap = []
        heapq.heappush(min_heap,(0, [(start_city)]))
        while(len(k_paths) < k and min_heap):
            dist,curr_path = heapq.heappop(min_heap)
            city = curr_path[-1]
            if(city == goal_city):
                k_paths.append(curr_path)
            for neigh,next_dist in roads[city]:
                if len(curr_path) < 2 or curr_path[-2] != neigh:
                    new_path = deepcopy(curr_path)
                    new_path.append(neigh)
                    heapq.heappush(min_heap,(dist+next_dist,new_path))
        return k_paths





if __name__ == "__main__":
    cities = ['Addis Ababa', 'Bahir Dar', 'Gondar', 'Hawassa', 'Mekelle']
    roads = {
        'Addis Ababa': [('Bahir Dar', 510), ('Hawassa', 275)],
        'Bahir Dar': [('Addis Ababa', 510), ('Gondar', 180)],
        'Gondar': [('Bahir Dar', 180), ('Mekelle', 300)],
        'Hawassa': [('Addis Ababa', 275)],
        'Mekelle': [('Gondar', 300)]
    }
    te = TravelingEthiopia(cities,roads)
    print(te.k_shortest_paths("Addis Ababa", "Mekelle", 2))

   
    







