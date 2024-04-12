from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from getpass import getpass
import json, re
import ipaddress

# ******************************************************
# **                                                  **
# **     This code was written by Costello            **
# **                                                  **
# **                                                  **
# **       constantin.cotiuga@gmail.com               **
# **                                                  **
# **                                                  **
# ******************************************************

username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Open the config.json file and load its contents for switch configuration.
with open('config.json') as json_file:
    confVars = json.load(json_file)

    # nxData is a list containing dictionaries.
    # Each dictionary contains the config parameters of the switch.
    nxData = confVars["switches"]

switchList = []
for switch in nxData:
    switchList.append(switch["hostname"])

ospfInst = confVars["ospf"]["name"]

# Create a dictionary of hostnames to loopback interface0 IPs
lo0Dict = {}
for switch in nxData:
    lo0Dict.update({switch["hostname"] : switch["loopback0"]})

bgpAs = confVars["bgp"]["as"]

mcastSub = confVars["mcast"]["group"]

for switch in nxData:
    if switch['role'] == 'leaf':
        lo0lf = switch['loopback0']
        lo0lf_sub = ipaddress.ip_network(f"{lo0lf}/24", strict=False)
        lo0lf_sub_str = str(lo0lf_sub)
    elif switch['role'] == 'bl':
        lo0bl = switch['loopback0']
        lo0bl_sub = ipaddress.ip_network(f"{lo0bl}/24", strict=False)
        lo0bl_sub_str = str(lo0bl_sub)
    else:
        pass

#Enable features on switches
features_vxlan_evpn = [
        'no cdp enable', # There is a bug, if CDP is enable in NXOSv the LLDP doesn;t show properly.
        'feature vn-segment-vlan-based',
        'feature nv overlay',
        'feature interface-vlan',
        'nv overlay evpn',
        'feature lldp',
        'feature nxapi',
        'feature tacacs+',
        'feature ospf',
        'feature bgp',
        'feature bfd',
        'feature pim'
                        ]

ospf_underlay = [
        'router ospf ' + ospfInst,
        'timers throttle spf 10 100 1000',
        'timers lsa-arrival 50',
        'timers throttle lsa 10 100 1000',
        'auto-cost reference-bandwidth 1000 gbps'
                ]
lo0 = None
#Firstly, I created the lo0 variable outside the for loop and initialized it to None
#As a result, the intlo0 list contained the string 'ip address <none>' with the <none> placeholder representing the lo0 variable.
#Then, in the for loop, after initializing lo0 with the correct value
intlo0 = [
        'interface Loopback0',
        'ip address {}/32'.format(lo0),
        'ip ospf network point-to-point',
        'ip router ospf UNDERLAY area 0.0.0.0',
        'ip pim sparse-mode'
         ]

pimRP = [
        'ip pim rp-address 10.121.0.255 group-list 239.121.0.0/16',
        'ip pim rp-candidate loopback1 group-list 239.121.0.0/16',
        'ip pim anycast-rp 10.121.0.255 Spine-Loopback1'
        ]
#Since lists in Python start counting from zero, the <none> placeholder was stored at index zero. By updating the intlo0 list's second element with the format method and the correct lo0 value

features_vxlan_evpn_bl=features_vxlan_evpn[:] # [:] is doing a copy of the features_vxlan_evpn and for bl we will append vpc later.
features_vxlan_evpn_bl.append('feature vpc')

def configure_features(net_connect):
    """Configure feature on a switch"""
    if switch['role'] == 'bl':
        output = net_connect.send_config_set(features_vxlan_evpn_bl)
    else:
        output = net_connect.send_config_set(features_vxlan_evpn)
		
def configure_interfaces(net_connect):
    """Configure VXLAN EVPN Fabric interfaces on a switch using LLDP to discover them."""
    # Send command to show LLDP neighbors
    lldp_neighbor_info = net_connect.send_command('show lldp neighbors detail', use_textfsm=True)
    # Loop through each neighbor
    for neighbor in lldp_neighbor_info:
        # Check if the neighbor's port description contains 'DC01' and if is not same device as the host from where is executed and if is an NX-OS device
        if ('DC01' in neighbor['neighbor'] and hostname_without_digits not in neighbor['neighbor'] and \
                'NX-OS' in neighbor['system_description']):

            # Construct the command to configure the interface
            cmd = [f"interface {neighbor['local_interface']}",
                   f"description Uplink to {neighbor['neighbor']}",
                   'no shutdown',
                   'no switchport',
                   'mtu 9216',
                   'no ip redirects',
                   'no ipv6 redirects',
                   'no ip port-unreachable',
                   'medium p2p',
                   'ip unnumbered loopback0',
                   'ip ospf network point-to-point',
                   'ip router ospf UNDERLAY area 0.0.0.0',
                   'ip pim sparse-mode'
                   ]
            net_connect.send_config_set(cmd)

            print(f"        - Configured port {neighbor['local_interface']}")

def configure_intlo1(net_connect):
    lo1 = switch['loopback1']
    intlo1 = [
              'interface Loopback1',
              'ip address {}/32'.format(lo1),
              'ip ospf network point-to-point',
              'ip router ospf UNDERLAY area 0.0.0.0',
              'ip pim sparse-mode'
             ]
    loopback1 = net_connect.send_config_set(intlo1)

def generate_pim_rp(net_connect):
    mcast_group = confVars["mcast"]["group"]
    anycast_rp  = [switch for switch in nxData if switch['role'] == 'spine']
    anycast_rp_ip = anycast_rp[0]['loopback1']
    pimRP = [
        'ip pim rp-address {} group-list {}'.format(anycast_rp_ip, mcast_group),
        'ip pim rp-candidate loopback1 group-list {}'.format(mcast_group),
    ]

    for switch in nxData:
        if switch['role'] == 'spine':
            loopback1 = switch['loopback1']
            loopback0 = switch['loopback0']
            pimRP.extend([
                'ip pim anycast-rp {} {}'.format(anycast_rp_ip, loopback0)
            ])

    pimRP_IP = net_connect.send_config_set(pimRP)
	
def generate_pim_mcast(net_connect):
    mcast_group = confVars["mcast"]["group"]
    anycast_rp  = [switch for switch in nxData if switch['role'] == 'spine']
    anycast_rp_ip = anycast_rp[0]['loopback1']
    mcastPIM = ['ip pim rp-address {} group-list {}'.format(anycast_rp_ip, mcast_group)]

    pimMcast = net_connect.send_config_set(mcastPIM)

def generate_nve1_int(net_connect):
    if switch['role'] == 'spine':
        pass
    else:
        nve1 = [
                'interface nve1',
                'source-interface loopback1',
                'host-reachability protocol bgp',
                'no shutdown'
                ]
        print('   - Configure NVE1 Interfaces')
        nve1_int = net_connect.send_config_set(nve1)

def generate_bgp(net_connect):
    if switch['role'] == 'spine':
        bgp_spines = [
                     'router bgp ' + bgpAs,
                     'router-id ' + switch['loopback0'],
                     'address-family l2vpn evpn',
                     'template peer RR-CLIENT',
                       'remote-as ' + bgpAs,
                       'update-source loopback0',
                       'address-family l2vpn evpn',
                         'send-community',
                         'send-community extended',
                         'route-reflector-client',
                      'neighbor ' + lo0lf_sub_str,
                      'inherit peer RR-CLIENT',
                      'neighbor ' + lo0bl_sub_str,
                      'inherit peer RR-CLIENT'
                      ]
        print('   - Configure BGP on Spines')
        bgp_spines_cmd = net_connect.send_config_set(bgp_spines)
    else:
        pass
		
def generate_bgp_leaf(net_connect):
    bgp = [
        'router bgp ' + bgpAs,
        'router-id ' + switch['loopback0'],
        'address-family l2vpn evpn',
        'template peer RR',
          'remote-as ' + bgpAs,
          'update-source loopback0',
          'address-family l2vpn evpn',
            'send-community',
            'send-community extended'
           ]
    for switches in nxData:
        if switches['role'] == 'spine':
            loopback1 = switches['loopback1']
            loopback0 = switches['loopback0']
            bgp.extend([
                'neighbor {}'.format(loopback0),
                'inherit peer RR'
                ])
        bgp_leafs_cmd = net_connect.send_config_set(bgp)

def save_config(net_connect):
    save = input('Do you want to save the configuration (yes/no)? ').lower()
    if save == 'yes':
        output = net_connect.send_command_timing('copy running-config startup-config')
        if 'Destination filename' in output:
            output += net_connect.send_command_timing("\n")
        print(output)
    else:
        print('Configuration not saved.')

# Configuration:

for switch in nxData:
    try:
        net_connect = ConnectHandler(device_type='cisco_nxos', ip=switch['ip'], username=username, password=password )
        print()
        print('*** Connectiong to', switch['hostname'] + ' ***')
        # Get the hostname of the device where the commands are executed
        hostname = switch['hostname']
        hostname_without_digits = re.sub(r'\d+$', '', hostname)
        print('   - Enable Features')
        configure_features(net_connect)
        print('   - Configure Fabric Interfaces')
        configure_interfaces(net_connect)
        print('   - Configure OSPF')
        ospf = net_connect.send_config_set(ospf_underlay)
        print('   - Configure interface Loopback0')
        lo0 = switch['loopback0']
        intlo0[1] = 'ip address {}/32'.format(lo0)
        loopback0 = net_connect.send_config_set(intlo0)
        print('   - Configure interface Loopback1')
        configure_intlo1(net_connect)
        if switch['role'] == 'spine':
            print('   - Configure PIM RP on Spines')
            generate_pim_rp(net_connect)
        else:
            print('   - Configure PIM on Leaf and BL Switches')
            generate_pim_mcast(net_connect)
        generate_nve1_int(net_connect)
        generate_bgp(net_connect)
        if switch['role'] == 'leaf' or switch['role'] == 'bl':
            print('   - Configure BGP on Leaf and BL Switches')
            generate_bgp_leaf(net_connect)
        save_config(net_connect)
    except NetMikoTimeoutException:
        print('   - Connection timed out!')
    except NetMikoAuthenticationException:
        print('   - Authentication failure!')
    except Exception as e:
        print('   - An error occurred:', e)
    net_connect.disconnect()
