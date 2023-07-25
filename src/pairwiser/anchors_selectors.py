import json
import random
from sklearn.cluster import KMeans

class RandomVertexSelector():

    def __init__(self,vertices_indices) -> None:
        self.vertices_indices = vertices_indices
        self.clustered_numbers = []

    def _partition_by_sides(self,num_clusters=2):
        # Create a KMeans object with the desired number of clusters
        kmeans = KMeans(n_clusters=num_clusters)
        
        # Reshape the input list into a 2D array (required for KMeans)
        X = [[num] for num in self.vertices_indices]
        
        # Perform clustering
        kmeans.fit(X)
        
        # Get the cluster centers
        cluster_centers = kmeans.cluster_centers_.ravel().tolist()
        
        # Find the closest number to each cluster center and add it to the result list
        self.labels = {}
        [self.labels.setdefault(center,[]) for center in cluster_centers]

        for index in self.vertices_indices:
            closest_num = min(cluster_centers, key=lambda center: abs(center - index))
            self.labels[closest_num].append(index)
        
        return self.labels

    def select_anchors(self):
        self._partition_by_sides()
        sampled_indices = []
        
        for side in self.labels.keys():
            selected_vertex = random.choice(self.labels[side])
            sampled_indices.append(selected_vertex)
        
        return sampled_indices
