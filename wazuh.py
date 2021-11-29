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
if config.has_section('Host') and 'user' in config['Host']:
    user = config['Host']['user']

if args.user:
    user = args.user

if config.has_section('Host') and 'server' in config['Host']:
    host = config['Host']['server']

if args.host:
    host = args.host



# syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_SYSLOG)

def last_keep_alive_diff(agent):
    return datetime.now() - datetime.strptime(agent['lastKeepAlive'], '%Y-%m-%dT%H:%M:%SZ')

def last_keep_alive_more_than(agent, days):
    if agent['status'] == "never_connected":
        return False

    lastKeepAliveDiff = last_keep_alive_diff(agent)
    if(lastKeepAliveDiff.days > days):
        return True
        

try:
    api = Wazuh(user, host)
except Exception as e:
    logger.error(e)
    exit()


while True:
    api.authenticate()
    logger.info("Getting all agents")
    status_code, response = api.get_all_agents()
    agents = [agent for agent in response['data']['affected_items']]

    agentsConnected = [agent for agent in agents if agent['status'] != "never_connected"]

    agentsLastKeepAliveMoreThan = [agent for agent in agentsConnected if last_keep_alive_more_than(agent,10)]
    agentsLastKeepAliveMoreThan.sort(key=last_keep_alive_diff)

    for agent in agentsLastKeepAliveMoreThan:
        logger.info(f"Host {agent['name']} with id {agent['id']} has not connected for {last_keep_alive_diff(agent).days} days.")

    #body = "Host".ljust(40) + "Days Without Connections\n"
    #body += '\n'.join([f"{agent['name'].ljust(40)} {last_keep_alive_diff(agent).days}" for agent in agentsLastKeepAliveMoreThan])
    body = "<table><tr><th>Host</th><th>Days Without Connections</th></tr>"
    body += ''.join([f"<tr><td>{agent['name']}</td><td>{last_keep_alive_diff(agent).days}</td></tr>" for agent in agentsLastKeepAliveMoreThan])
    body += "</table>"

    if args.email:
        logger.info(f"Sending email to {config['Email']['to']}.")
        send_email(config['Email']['from'], config['Email']['to'], config['Email']['subject'], body, config['Email']['server'])

    seconds = 86400
    logger.info(f'Waiting {seconds} seconds...')
    time.sleep(seconds) # one day

    

    