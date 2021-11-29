from dataclasses import dataclass, field
import sys
from loggingHelper import logger
import requests
import urllib3
from base64 import b64encode
import getpass
import logging


# Disable insecure https warnings (for self-signed SSL certificates)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



@dataclass
class Wazuh:
    username: str
    password: str = field(init=False)
    host: str
    port: str = field(default='55000')
    baseUrl: str = field(init=False)
    token: str = field(init=False)
    verify: bool = field(default=False)
    loginEndpoint: str = field(init=False, default='security/user/authenticate')
    requests_headers: str = field(init=False)
    
    
    def __post_init__(self):

        self.baseUrl = f"{self.host}:{self.port}"
        self.password = getpass.getpass(prompt='Password: ', stream=None)
        self.authenticate()        

    def authenticate(self):

        basic_auth = f"{self.username}:{self.password}".encode()
        login_headers = {'Content-Type': 'application/json','Authorization': f'Basic {b64encode(basic_auth).decode()}'}
        logging.info("Attempting to login")
        status_code, response = self.req('auth', self.loginEndpoint, data=login_headers)
        if status_code != requests.codes.ok:
            raise ConnectionError("Invalid Password")
        self.token = response['data']['token']
        logging.info('Authentication Success')
        self.requests_headers = {'Content-Type': 'application/json','Authorization': f'Bearer {self.token}'}



    def req(self, method, resource, data=None):
        url = '{0}/{1}'.format(self.baseUrl, resource)

        try:
            requests.packages.urllib3.disable_warnings()

            if method.lower() == 'post':
                r = requests.post(url, headers=self.requests_headers, data=data, verify=self.verify)
            elif method.lower() == 'put':
                r = requests.put(url, headers=self.requests_headers, data=data, verify=self.verify)
            elif method.lower() == 'delete':
                r = requests.delete(url, headers=self.requests_headers, data=data, verify=self.verify)
            elif method.lower() == 'auth':
                r = requests.get(url, headers=data, verify=self.verify)
            else:
                r = requests.get(url, headers=self.requests_headers, params=data, verify=self.verify)

            code = r.status_code
            res_json = r.json()

        except Exception as exception:
            print("Error: {0}".format(exception))
            sys.exit(1)

        return code, res_json



    def get_all_agents(self):
        response = self.req('get', '/agents')
        return response

class ConnectionError(Exception):
    pass
