import unittest
from src.assembler.anchors_selectors import RandomVertexSelector

class TestAnchorsSelectors(unittest.TestCase):

    def test_random_vertex_rpf_00194(self):
        rpf_00194_vertices = [15,16,16,17,32,33]

        selector = RandomVertexSelector()
        sampled_indices =  selector.select_anchors(rpf_00194_vertices)
        print(sampled_indices)
    
    def test_random_vertex_rpf_00197(self):
        rpf_00197_vertices =  [19,20,42,43,43,44]

        selector = RandomVertexSelector()
        sampled_indices =  selector.select_anchors(rpf_00197_vertices)
        print(sampled_indices)

if __name__ == "__main__":
    unittest.main()