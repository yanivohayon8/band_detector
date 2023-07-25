import sys
sys.path.append("./")

import unittest
#from src.my_http_client import HTTPClient
from src.my_http_client import SpringsHTTPClient 



class TestHTTPClient(unittest.TestCase):
    
    def test_sanity(self):
        http = SpringsHTTPClient()
        print(http.send_sanity())

    def test_reconstruction(self):
        http = SpringsHTTPClient()
        res = http.send_reconstruct_request("RPf_00194_intact_mesh,1,RPf_00195_intact_mesh,1")
        print(res)


if __name__ == "__main__":
    unittest.main()