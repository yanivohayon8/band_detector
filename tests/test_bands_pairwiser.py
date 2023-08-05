import unittest
from src.assembler.matings import VertexMating
from src.assembler.anchors_selectors import RandomVertexSelector,pairwise_permutations
from src.assembler.physical_assemler import PhysicalAssembler
from src.my_http_client import SpringsHTTPClient

# from src.assembler.pairwiser import BandsPairwiser

class TestPairwiser(unittest.TestCase):
    
    def test_toy_example_two_pieces(self):
        first_fragment = "RPf_00194_intact_mesh"
        second_fragment = "RPf_00197_intact_mesh"
        rpf_00194_closest_vertices = [15,16,16,17,32,33] 
        rpf_00197_closest_vertices =  [19,20,42,43,43,44]

        anchor_selector = RandomVertexSelector()
        first_frag_anchor_1, first_frag_anchor_2 = anchor_selector.select_anchors(rpf_00194_closest_vertices)
        second_frag_anchor_1, second_frag_anchor_2 = anchor_selector.select_anchors(rpf_00197_closest_vertices)
        permutations = pairwise_permutations(first_frag_anchor_1,first_frag_anchor_2,second_frag_anchor_1,second_frag_anchor_2)
        inner_springs_pairs_permutations = [[(0,0),(1,1)],[(0,1),(1,0)]]


        physical_assembler = PhysicalAssembler(SpringsHTTPClient())

        for i,permut in enumerate(permutations):

            for permut_spring_repr, spring_permutation in zip(["springPermA","springPermB"],inner_springs_pairs_permutations):
                matings = []
                first_spring_side1_i = spring_permutation[0][0]
                first_spring_side2_i = spring_permutation[0][1]
                second_spring_side1_i = spring_permutation[1][0]
                second_spring_side2_i = spring_permutation[1][1]

                mate_1 = VertexMating(first_fragment,permut[0][first_spring_side1_i],
                                      second_fragment,permut[1][first_spring_side2_i])
                matings.append(mate_1)

                mate_2 = VertexMating(first_fragment,permut[0][second_spring_side1_i],
                                      second_fragment,permut[1][second_spring_side2_i])
                matings.append(mate_2)
                print(matings[0])
                print(matings[1])
                response = physical_assembler.run(matings,screenshot_name=f"permutation_{i+1}_{permut_spring_repr}")
                print(f"permutation {i+1} score: ", physical_assembler.score_assembly(response))


if __name__ == "__main__":
    unittest.main()