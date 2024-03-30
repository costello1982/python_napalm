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
```
