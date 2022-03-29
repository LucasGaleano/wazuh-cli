# Wazuh-cli

This script consists in two parts, a wazuh-client for communicate with the Wazuh-manager and a script to get all the agents that are not connected in more than x days.

## How it works
First, Create and edit the config.conf (There is a example file in the repository)
The Wazuh part of the config, configurates all the required data for the conection to the manager.
The Email part configurates the required data for sending a email with the information. 


Then just run the script
`wazuh.py`
or to enable the email
`wazuh.py --email`
you can also specify some data as a parameters
`wazuh.py --user <user> --host <host> --email`

## Logging
The script will logs all the information to stdout and to /var/log/syslog



## To get all the packages from wazuh, use wazuhpg.py
This is an aditional script to get all the packages from all the agents.
You need to install the requirements.txt to use this.
pip3 install -r requirements.txt

### Usage:

`wazuhpg.py --user <user> --host <host> --port <default 55000> --output <default package.lst>`

### Then a simple grep to search package quickly

`grep -C2 <package> package.lst`
