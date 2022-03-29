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



## For getting all the packages from wazuh, use wazuhpg.py

### Usage:

`wazuhpg.py --user <user> --host <host> --port <default 55000> --output <default package.lst>`

### Then a simple grep to search package quickly

`grep -C2 <package> package.lst`
