from netmiko import ConnectHandler

# List of switch details
switches = [
    {'ip': '192.168.1.1', 'device_type': 'cisco_nxos', 'username': 'admin', 'password': 'password'},
    {'ip': '192.168.1.2', 'device_type': 'cisco_nxos', 'username': 'admin', 'password': 'password'},
    # Add more switches as needed
]

def configure_features(net_connect):
    """Configure feature on a switch"""
    
    command = "terminal dont-ask"
    output = net_connect.send_command(command)
    print(output)

def configure_vlan(net_connect):
    """Configure VLAN on a switch"""
    
    vlan_id = 100
    vlan_name = 'VLAN100'
    command = f"vlan {vlan_id}"
    output = net_connect.send_config_set([command, f"name {vlan_name}"])
    print(output)

for switch in switches:
    net_connect = ConnectHandler(**switch)

    configure_features(net_connect)
    configure_vlan(net_connect)

    net_connect.disconnect()
