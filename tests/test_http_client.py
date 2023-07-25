import sys
sys.path.append("./")

import unittest
#from src.my_http_client import HTTPClient
from src.my_http_client import HTTPClient 



class TestHTTPClient(unittest.TestCase):
    
    def test_sanity(self):
        http = HTTPClient()
        print(http.send_sanity())


if __name__ == "__main__":
    unittest.main()