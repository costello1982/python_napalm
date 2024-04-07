# pip install openpyxl You will need to install openpyxl first.
import netmiko
from netmiko import ConnectHandler
import openpyxl

def get_switch_info(switch_ip, username, password):
    switch = {
        'device_type': 'cisco_nxos',
        'ip': switch_ip,
        'username': username,
        'password': password,
    }
    
    try:
        connection = ConnectHandler(**switch)
        output = connection.send_command('show version')
        print(f"Switch {switch_ip} version information:")
        print(output)
        connection.disconnect()
    except netmiko.NetMikoTimeoutException:
        print(f"Failed to connect to {switch_ip}. Timeout.")
    except netmiko.NetMikoAuthenticationException:
        print(f"Failed to authenticate to {switch_ip}. Check username/password.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Load switch information from Excel file
    workbook = openpyxl.load_workbook('switches.xlsx')
    sheet = workbook.active

    # Iterate over rows in the Excel file
    for row in sheet.iter_rows(values_only=True):
        switch_ip, username, password = row
        get_switch_info(switch_ip, username, password)

if __name__ == "__main__":
    main()

# Excel file named switches.xlsx with the following columns: Switch IP, Username, Password. Fill in the details accordingly for each switch you want to connect to.
