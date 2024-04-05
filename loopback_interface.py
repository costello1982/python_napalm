import re
import ipaddress

switches = ['SW_01', 'SW_02', 'SW_03']

for switch in switches:
    last_digit = re.search(r'\d+$', switch).group()
    last_digit = str(int(last_digit))  # Removing leading zeros
    loopback_ip = f'10.10.10.{last_digit}'
    try:
        ipaddress.IPv4Address(loopback_ip)
        print(f"Configuring loopback interface for {switch} with IP address {loopback_ip}")
        # You can add your configuration commands here, like using Netmiko to SSH into the switch and apply the configurations.
    except ipaddress.AddressValueError:
        print(f"Invalid IP address: {loopback_ip} for switch {switch}")
