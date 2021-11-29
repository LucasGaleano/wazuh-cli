#!/usr/bin/env python3

import json
import argparse
from alive_progress import alive_bar
from wazuhClient import Wazuh



parser = argparse.ArgumentParser(description='Fetch data from wazuh API.')
parser.add_argument('--host',required=True, type=str,help='host to connect')
parser.add_argument('-p', '--port',type=str, default='55000',help='port to connect')
parser.add_argument('-o', '--output',type=str, default='packages.lst',help='output file name')
parser.add_argument('-u', '--user',required=True, type=str,help='user')
args = parser.parse_args()

host = args.host
port = args.port
user = args.user

api = Wazuh(user,host)

print("[+] Getting all agents")
status_code, response = api.get_all_agents()
agentsID = [agentID['id'] for agentID in response['data']['affected_items']]

print('[+]',len(agentsID),"agents in total")

with alive_bar(len(agentsID), title="Getting packages", spinner=None) as bar:
    with open('packages.lst', 'w') as f:
        for ID in agentsID:
            status_code, response = api.req('get', '/syscollector/' +ID+ '/packages?select=name,version')
            f.write(json.dumps(response, indent=4, sort_keys=True))
            bar()
