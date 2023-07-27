import json
import random
from sklearn.cluster import KMeans

class RandomVertexSelector():

    def __init__(self) -> None:
        pass

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

    def select_anchors(self,vertices_indices):
        self.vertices_indices = vertices_indices
        self.clustered_numbers = []
        self._partition_by_sides()
        sampled_indices = []
        
        for side_center in self.labels.keys():
            selected_vertex_min = min(self.labels[side_center], key=lambda index: side_center - index)#random.choice(self.labels[side])
            selected_vertex_max = max(self.labels[side_center], key=lambda index: side_center - index)#random.choice(self.labels[side])
            sampled_indices.append([selected_vertex_min,selected_vertex_max])
        
        return sampled_indices

# class WideGripSelector(RandomVertexSelector):
#     def select_anchors(self,vertices_indices):
#         self.vertices_indices = vertices_indices
#         self.clustered_numbers = []
#         self._partition_by_sides()
#         sampled_indices = []
        
#         for side in self.labels.keys():
#             selected_vertex = random.choice(self.labels[side])
#             sampled_indices.append(selected_vertex)
        
#         return sampled_indices

def pairwise_permutations(first_frag_anchor_1,first_frag_anchor_2,second_frag_anchor_1,second_frag_anchor_2 ):
    '''
    first_frag_anchor_1 - The vertex index of the first side of the first fragment
    first_frag_anchor_2 - ...
    second_frag_anchor_1
    second_frag_anchor_2
    '''

    return [
        (first_frag_anchor_1,second_frag_anchor_1),
        (first_frag_anchor_1,second_frag_anchor_2),
        (first_frag_anchor_2,second_frag_anchor_1),
        (first_frag_anchor_2,second_frag_anchor_2)
    ]