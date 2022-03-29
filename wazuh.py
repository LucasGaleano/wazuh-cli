from wazuhClient import Wazuh
from loggingHelper import logger
import argparse
from datetime import datetime
import time
from sendMail import send_email

parser = argparse.ArgumentParser(description='Fetch data from wazuh API.')
parser.add_argument('--host', type=str,help='host to connect')
parser.add_argument('-u', '--user', type=str,help='user')
parser.add_argument('--email', action='store_true', help='send the report by email')
args = parser.parse_args()
  

import configparser
config = configparser.ConfigParser()
config.read('config')

#some basic validation
if config.has_section('Wazuh') and 'user' in config['Wazuh']:
    user = config['Wazuh']['user']

if args.user:
    user = args.user

if config.has_section('Wazuh') and 'server' in config['Wazuh']:
    host = config['Wazuh']['server']

if args.host:
    host = args.host




def last_keep_alive_diff(agent):
    return datetime.now() - datetime.strptime(agent['lastKeepAlive'], '%Y-%m-%dT%H:%M:%SZ')

def last_keep_alive_more_than(agent, days):
    if agent['status'] == "never_connected":
        return False

    lastKeepAliveDiff = last_keep_alive_diff(agent)
    if(lastKeepAliveDiff.days > days):
        return True
        

try:
    api = Wazuh(user, host, password=config['Wazuh']['token'])
except Exception as e:
    logger.error(e)
    exit()


while True:
    api.authenticate()
    logger.info("Getting all agents")
    status_code, response = api.get_all_agents()
    agents = [agent for agent in response['data']['affected_items']]

    # get all the agents connected except for the never_connected status 
    agentsConnected = [agent for agent in agents if agent['status'] != "never_connected"]

    # if the agent's last keep alive is more than 10 days, it'll be add to the list and sort.
    agentsLastKeepAliveMoreThan = [agent for agent in agentsConnected if last_keep_alive_more_than(agent,10)]
    agentsLastKeepAliveMoreThan.sort(key=last_keep_alive_diff)

    for agent in agentsLastKeepAliveMoreThan:
        logger.info(f"Host: {agent['name']}, id: {agent['id']}, has not connected for {last_keep_alive_diff(agent).days} days.")



    if args.email:
        # we create the table of agents for the email and send it.
        body = "<table><tr><th>Host</th><th>Days Without Connections</th></tr>"
        body += ''.join([f"<tr><td>{agent['name']}</td><td>{last_keep_alive_diff(agent).days}</td></tr>" for agent in agentsLastKeepAliveMoreThan])
        body += "</table>"

        logger.info(f"Sending email to {config['Email']['to']}.")
        send_email(config['Email']['from'], config['Email']['to'], config['Email']['subject'], body, config['Email']['server'])

    seconds = 86400
    logger.info(f'Waiting {seconds} seconds...')
    time.sleep(seconds) # one day

    

    