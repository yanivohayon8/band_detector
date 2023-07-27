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

        physical_assembler = PhysicalAssembler(SpringsHTTPClient())

        for i,permut in enumerate(permutations):
            matings = []
            matings.append(VertexMating(first_fragment,permut[0][0],second_fragment,permut[1][1]))
            matings.append(VertexMating(first_fragment,permut[0][1],second_fragment,permut[1][0]))
            print(matings[0])
            print(matings[1])
            response = physical_assembler.run(matings,screenshot_name=f"permutation_{i+1}")
            print(f"permutation {i+1} score: ", physical_assembler.score_assembly(response))


if __name__ == "__main__":
    unittest.main()