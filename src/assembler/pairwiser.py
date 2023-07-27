# from src.assembler.anchors_selectors import RandomVertexSelector
# from src.assembler.matings import VertexMating

# class BandsPairwiser():

#     def __init__(self,vertex_selector:RandomVertexSelector) -> None:
#         self.vertex_selector = vertex_selector
    
#     def compute_mating_permutations(self,first_frag_id,first_frag_closest_vertices,second_frag_id,second_frag_closest_vertices):
#         first_frag_anchor_1, first_frag_anchor_2 = self.vertex_selector.select_anchors(first_frag_closest_vertices)
#         second_frag_anchor_1, second_frag_anchor_2 = self.vertex_selector.select_anchors(second_frag_closest_vertices)

#         permutations =  [
#             (first_frag_anchor_1,second_frag_anchor_1),
#             (first_frag_anchor_1,second_frag_anchor_2),
#             (first_frag_anchor_2,second_frag_anchor_1),
#             (first_frag_anchor_2,second_frag_anchor_2)
#         ]

#         return [VertexMating(first_frag_id,permut[0],second_frag_id,permut[1]) for permut in permutations]
    
    



       






