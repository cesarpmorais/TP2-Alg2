from distance_matrix import DistanceMatrix
from scipy.sparse.csgraph import minimum_spanning_tree
import numpy as np
import networkx as nx

class Heuristics:
    def __init__(self, distance_matrix: DistanceMatrix):
        self.distance_matrix_obj = distance_matrix
        
    def __dfs(self, node, visited):
        neighbors = np.where(self.adj_list[node] == 1)[0]
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.append(neighbor)
                self.path.append(neighbor)
                self.__dfs(neighbor, visited)
        
    def __create_mst_adjacency_list(self):
        length = len(self.distance_matrix_obj.distance_matrix)
        mst = minimum_spanning_tree(self.distance_matrix_obj.distance_matrix)
        edges = list(zip(*mst.nonzero()))
        
        # Create adjacency list
        adj_list = np.zeros((length, length))
        for v, u in edges:
            adj_list[v, u] = 1
            adj_list[u, v] = 1
        
        self.adj_list = adj_list
    
    def __analyze_path(self):
        visited = [0]
        sum = 0
        last_i = 0
        
        for i, j in zip(self.path, self.path[1:]):
            if j in visited:
                continue
            
            visited.append(j)
            sum += self.distance_matrix_obj.distance_matrix[last_i, j]
            last_i = j
            
        sum += self.distance_matrix_obj.distance_matrix[0, visited[-1]]
        
        return sum, visited
    
    def __treat_visited(self, visited):
        for i in range(len(visited)):
            visited[i] += 1
        visited.append(1)
    
    def twice_around_the_tree(self):
        self.__create_mst_adjacency_list()
        self.path = [0]
        self.__dfs(0, [])
        
        sum, visited = self.__analyze_path()
        self.__treat_visited(visited)
        
        return sum, visited

    def christofides(self):
        self.__create_mst_adjacency_list()
        
        # Find odd degree vertices
        odd_vertices = []
        for i, l in enumerate(self.adj_list):
            if np.sum(l) % 2 == 1:
                odd_vertices.append(i)
                
        # Find minimum cost matching
        original_matrix = self.distance_matrix_obj.distance_matrix
        matching_graph = np.zeros_like(original_matrix)
        matching_graph[np.ix_(odd_vertices, odd_vertices)] = original_matrix[np.ix_(odd_vertices, odd_vertices)]
        
        matching_edges = nx.algorithms.matching.min_weight_matching(nx.Graph(matching_graph))
        
        # Add matching_edges to adj list
        for i, j in matching_edges:
            self.adj_list[i, j] = 1
            self.adj_list[j, i] = 1
            
        self.path = [0]
        self.__dfs(0, [])
        
        sum, visited = self.__analyze_path()
        self.__treat_visited(visited)
        
        return sum, visited