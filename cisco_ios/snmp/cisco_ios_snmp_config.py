from netmiko import ConnectHandler
import getpass
import time

############### Function to configure SNMP on a device ###############################

def configure_snmp(ip, username, password, snmp_community, snmp_location):
    network_device = {
        "host": ip,
        "username": username,
        "password": password,
        "device_type": "cisco_ios",
        "secret": password
    }

    connect_to_device = ConnectHandler(**network_device)
    connect_to_device.enable()
    list_of_commands = [
        f"snmp-server community {snmp_community} RO",
        f"snmp-server location {snmp_location}",
    ]

    print(ip,list_of_commands)
    output = connect_to_device.send_config_set(list_of_commands)
    time.sleep(2)
    print(output)
    output = connect_to_device.send_command("wr")
    time.sleep(2)
    print(output)
    time.sleep(2)
    connect_to_device.exit_enable_mode()
    connect_to_device.disconnect()
    list_of_commands = []

########################################################################
# Taking user input to pass username and password
username = input("Enter TACACS Username:")
password = getpass.getpass("Enter Password:")

# Opening SNMP file
snmp_file = open("snmp_list.txt", "r")

# Reading lines and per line configure device
for lines in snmp_file:
    line_info = lines.strip().split(",")
    if len(line_info) == 3:
        ip, snmp_community, snmp_location = line_info
        configure_snmp(ip, username, password, snmp_community, snmp_location)
    else:
        print("File Error!!!")
snmp_file.close()