# Python Network Programming for Network Engineers (Python 3)

## NAPALM INSTALL: 
===============
### These steps are only required if you don't have Netmiko and NAPALM installed. See the below steps for Python3 NAPALM
```
apt-get update
apt-get install python -y
apt-get install build-essential libssl-dev libffi-dev -y
apt-get install python-pip -y
pip install cryptography
pip install netmiko
pip install napalm
```
## PYTHON3 NAPALM INSTALL:
========================
### Use the following commands to install Python3 Netmiko and NAPALM:
```
apt-get update
apt-get install python3-pip
pip3 install -U netmiko
pip3 install -U napalm
pip3 install -U simplejson
pip3 install --upgrade pipenv
 ```

JSON allows us to format in human readable format


https://app.freedev.ai

```
import ipaddress

ip = "192.168.2.14"
subnet = ipaddress.ip_network(f"{ip}/24", strict=False)
print(subnet)

```
