import unittest
from src.pairwiser.physical_assemler import PhysicalAssembler
from src.my_http_client import SpringsHTTPClient

class TestPhysicalAssembler(unittest.TestCase):
    
    def test_toy_example(self):
        http = SpringsHTTPClient()
        assembler = PhysicalAssembler(http)
        res = assembler.run("RPf_00194_intact_mesh,1,RPf_00195_intact_mesh,1")
        print(assembler.score_assembly(res))

if __name__  == "__main__":
    unittest.main()