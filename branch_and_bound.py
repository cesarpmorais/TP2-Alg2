from distance_matrix import DistanceMatrix

import sys
import numpy as np
import heapq

class Node:
    def __init__(self, path, bound):
        self.path = path
        self.bound = bound
        
    def __lt__(self, other):
        return self.bound < other.bound

class BranchAndBound:
    def __init__(self, distance_matrix: DistanceMatrix):
        self.distance_matrix = distance_matrix
        self.dimension = distance_matrix.dimension
        
    def __treat_best_path(self, visited):
        for i in range(len(visited)):
            visited[i] += 1
        visited.append(1)
        
    def run(self):
        best_solution = np.inf
        best_path = None
        heap = []
        
        heapq.heappush(heap, Node([0], self.distance_matrix.calculate_bound([0])))
        
        while heap:
            node = heapq.heappop(heap)
            
            if node.bound > best_solution:
                continue
            
            if len(node.path) == self.dimension:
                if node.bound < best_solution:
                    best_solution = node.bound
                    best_path = node.path
            else:
                for i in range(self.dimension):
                    if i not in node.path:
                        new_path = node.path + [i]
                        heapq.heappush(heap, Node(new_path, self.distance_matrix.calculate_bound(new_path)))
        
        self.__treat_best_path(best_path)
        
        return best_solution, best_path            

