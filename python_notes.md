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
