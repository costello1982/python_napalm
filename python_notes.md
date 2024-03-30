### Dictionaries:
```
>>> switch1 = {
...     'device_type': 'cisco_nsos',
...     'ip': '192.168.1.72',
...     'username': 'admin',
...     'password': 'admin'
... }
>>>
>>> switch1
{'device_type': 'cisco_nsos', 'ip': '192.168.1.72', 'username': 'admin', 'password': 'admin'}
>>> switch1['ip']
'192.168.1.72'
We can modify a value:
>>> switch1['ip'] = '192.168.2.100'
>>> switch1['ip']
'192.168.2.100'
We can easly add a value:
>>> switch1['secret'] = 'cisco123'
>>> switch1
{'device_type': 'cisco_nsos', 'ip': '192.168.2.100', 'username': 'admin', 'password': 'admin', 'secret': 'cisco123'}
Combine two dictionaries:
>>> switch1
{'device_type': 'cisco_nsos', 'ip': '192.168.2.100', 'username': 'admin', 'password': 'admin', 'secret': 'cisco123'}
>>> switch2
{'model': 'iosv', 'color': 'white', 'support': 'none'}
>>> switch1.update(switch2)
>>> switch1
{'device_type': 'cisco_nsos', 'ip': '192.168.2.100', 'username': 'admin', 'password': 'admin', 'secret': 'cisco123', 'model': 'iosv', 'color': 'white', 'support': 'none'}

>>> 'secret' in switch1
True

>>> switch1.get('ip')
'192.168.2.100'

>>> switch1.keys()
dict_keys(['device_type', 'ip', 'username', 'password', 'secret', 'model', 'color', 'support'])

>>> list(switch1.keys())
['device_type', 'ip', 'username', 'password', 'secret', 'model', 'color', 'support']

>>> switch1.values()
dict_values(['cisco_nsos', '192.168.2.100', 'admin', 'admin', 'cisco123', 'iosv', 'white', 'none'])

>>> switch1.items()
dict_items([('device_type', 'cisco_nsos'), ('ip', '192.168.2.100'), ('username', 'admin'), ('password', 'admin'), ('secret', 'cisco123'), ('model', 'iosv'), ('color', 'white'), ('support', 'none')])

```
### Functions
To create easy to use and reusable code
Modular code

Python Function
     - def
     - function name
     - paranthesis enclosing any input parameters to the function
     - colon(:)

```
def printhello():
    print ('hello')

printhello()
printhello()
printhello()

python3 python02functions.py
hello
hello
hello
```

```
def device_type(device):
    if device == '1800':
        return "It's a Cisco Router"
    if device == '2900':
        return "It's a Cisco Router"
    if device == '3750':
        return "It's a Cisco Switch"
    if device == '2950':
        return "It's a Cisco Switch"
    else:
        return "It's a shit"

whatdevice = input("Enter device [1800,2900,3750,2950]:")
answer = device_type(whatdevice)

print(answer)
```


