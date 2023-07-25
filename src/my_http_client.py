import urllib3
import json
from urllib.parse import urlencode


class SpringsHTTPClient:
    def __init__(self, host="localhost", port=8888):
        self.host = host
        self.port = port
        self.http = urllib3.PoolManager()
        self.url_prefix = "v0/RePAIR"
        self.base_target = f"http://{self.host}:{self.port}/{self.url_prefix}"

    def send_sanity(self):
        target = f"{self.base_target}/sanity"
        response = self.http.request('GET', target)

        if response.status != 200:
            raise Exception(response.reason)

        return response.data.decode('utf-8')

    def send_reconstruct_request(self, body, screenshot_name=""):
        query_parameters = {}

        if screenshot_name != "":
            query_parameters["screenShotName"] = screenshot_name

        encoded_args = urlencode(query_parameters)
        query_parameters_str = "reconstructions?" + encoded_args
        target = f"{self.base_target}/{query_parameters_str}"

        response = self.http.request(
            'POST',
            target,
            body=body,
            headers={'Content-Type': 'text/plain'}
        )

        return json.loads(response.data.decode('utf-8'))
