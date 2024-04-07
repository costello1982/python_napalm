import netmiko
from netmiko import ConnectHandler
import yaml

def get_switch_info(switch):
    try:
        connection = ConnectHandler(**switch)
        output = connection.send_command('show version')
        print(f"Switch {switch['ip']} version information:")
        print(output)
        connection.disconnect()
    except netmiko.NetMikoTimeoutException:
        print(f"Failed to connect to {switch['ip']}. Timeout.")
    except netmiko.NetMikoAuthenticationException:
        print(f"Failed to authenticate to {switch['ip']}. Check username/password.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Load switch information from YAML file
    with open('switches.yaml') as f:
        switch_data = yaml.safe_load(f)
    
    switches = switch_data['switches']

    # Iterate over switches in the YAML file
    for switch in switches:
        get_switch_info(switch)

if __name__ == "__main__":
    main()



#switches:
#  - ip: switch1_ip
#    username: switch1_username
#    password: switch1_password
#  - ip: switch2_ip
#    username: switch2_username
#    password: switch2_password
#  ...
