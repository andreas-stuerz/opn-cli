import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from opnsense_api.exception import APIException

HTTP_SUCCESS = (200, 201, 202, 203, 204, 205, 206, 207)

class ApiClient(object):
    def __init__(self, api_key, api_secret, base_url, ssl_verify_cert, timeout):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.ssl_verify_cert = ssl_verify_cert
        self.timeout = timeout

    def _process_response(self, response):
        if response.status_code in HTTP_SUCCESS:
            return json.loads(response.text)
        else:
            print(response.text)
            raise APIException(response=response.status_code, resp_body=response.text, url=response.url)

    def build_endpoint_url(self, *args, **kwargs):
        endpoint = f"{kwargs['module']}/{kwargs['controller']}/{kwargs['command']}"
        endpoint_params = '/'.join(args)
        if endpoint_params:
            return f"{endpoint}/{endpoint_params}".lower()
        return endpoint.lower()


    def get(self, endpoint):
        req_url = '{}/{}'.format(self.base_url, endpoint)
        response = requests.get(req_url, verify=self.ssl_verify_cert,
                                auth=(self.api_key, self.api_secret),
                                timeout=self.timeout)
        return self._process_response(response)

    def post(self, endpoint, body=None):
        req_url = '{}/{}'.format(self.base_url, endpoint)
        response = requests.post(req_url, data=body, verify=self.ssl_verify_cert,
                                 auth=(self.api_key, self.api_secret),
                                 timeout=self.timeout)
        return self._process_response(response)

    def execute(self, *args, **kwargs):
        endpoint = self.build_endpoint_url(*args, **kwargs)
        if kwargs['method'] == 'get':
            return self.post(endpoint)
        elif kwargs['method'] == 'post':
            return self.get(endpoint)
        else:
            raise NotImplementedError(f"Unkown HTTP method: {kwargs['method']}")

