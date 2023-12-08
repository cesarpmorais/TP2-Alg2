import numpy as np

class DistanceMatrix:
    def __init__(self, file_name):
        with open(file_name) as file:
            lines = file.readlines()
            
            # Find dimension
            for l in lines[:6]:
                if "DIMENSION" in l:
                    self.dimension = ""
                    for char in l:
                        if char.isdigit():
                            self.dimension += char
                    self.dimension = int(self.dimension)
                
            # Get node matrix
            nodes = np.zeros((self.dimension, 2))
            for l in lines[6:]:
                if l.strip() == "EOF":
                    break
                id, x_coord, y_coord = map(float, l.split())
                nodes[int(id)-1] = np.array((float(x_coord), float(y_coord)))
                
            # Generate Distance Matrix
            self.distance_matrix = np.zeros((self.dimension, self.dimension))
            for i in range(self.dimension):
                for j in range(i+1, self.dimension):
                    distance = self.__euclidean_distance(nodes[i], nodes[j])
                    self.distance_matrix[i][j] = distance
                    self.distance_matrix[j][i] = distance
        
    def __euclidean_distance(self, node_1, node_2):
        return np.sqrt(np.sum((node_1 - node_2)**2))
    
    # Bound values are the mean of the 2 lowest value edges in a vertex
    def calculate_bound(self, my_path):
        bound = 0
        
        for i, j in zip(my_path, my_path[1:]):
            bound += self.distance_matrix[i][j]
        
        bound += self.distance_matrix[my_path[-1]][my_path[0]]
            
        for i, l in enumerate(self.distance_matrix):
            if i in my_path:
                continue
            
            sorted_index = np.argsort(l)
            bound += (self.distance_matrix[i][sorted_index[1]] + self.distance_matrix[i][sorted_index[2]])/2
        
        return bound
                
