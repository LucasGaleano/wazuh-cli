# Wazuh-get-all-packages

### Usage:
`wazuhpg.py --user <user> --host <host> --port <default 55000> --output <default package.lst>`

### Then a simple grep to search package quickly

`grep -C2 <package> package.lst`
