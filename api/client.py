import requests
import json
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from api.exception import APIException

HTTP_SUCCESS = (200, 201, 202, 203, 204, 205, 206, 207)

class ApiClient(object):
    def __init__(self, api_key, api_secret, base_url, ssl_verify_cert, ca, timeout):
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = base_url
        self._ssl_verify_cert = ssl_verify_cert
        self._timeout = timeout
        self._ca = ca

    @property
    def ssl_verify_cert(self):
        if self._ssl_verify_cert:
            return self._ca
        return self._ssl_verify_cert

    def _process_response(self, response):
        if response.status_code in HTTP_SUCCESS:
            return json.loads(response.text)
        else:
            raise APIException(response=response.status_code, resp_body=response.text, url=response.url)

    def build_endpoint_url(self, *args, **kwargs):
        endpoint = f"{kwargs['module']}/{kwargs['controller']}/{kwargs['command']}"
        endpoint_params = '/'.join(args)
        if endpoint_params:
            return f"{endpoint}/{endpoint_params}".lower()
        return endpoint.lower()


    def get(self, endpoint):
        print(self.ssl_verify_cert)
        req_url = '{}/{}'.format(self._base_url, endpoint)
        response = requests.get(req_url, verify=self.ssl_verify_cert,
                                auth=(self._api_key, self._api_secret),
                                timeout=self._timeout)
        return self._process_response(response)

    def post(self, endpoint, body=None):
        req_url = '{}/{}'.format(self._base_url, endpoint)
        response = requests.post(req_url, data=body, verify=self.ssl_verify_cert,
                                 auth=(self._api_key, self._api_secret),
                                 timeout=self._timeout)
        return self._process_response(response)

    def execute(self, *args, **kwargs):
        endpoint = self.build_endpoint_url(*args, **kwargs)
        if kwargs['method'] == 'get':
            return self.get(endpoint)
        elif kwargs['method'] == 'post':
            return self.post(endpoint)
        else:
            raise NotImplementedError(f"Unkown HTTP method: {kwargs['method']}")

