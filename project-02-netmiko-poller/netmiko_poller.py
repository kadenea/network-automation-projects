from dotenv import load_dotenv
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
import os
import csv

load_dotenv()


def get_inventory():
    inventory = []
    with open('devices.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            inventory.append(row)
    return inventory

def get_credentials():
    username = os.getenv('LAB_USERNAME')
    password = os.getenv('LAB_PASSWORD')
    return username, password

def build_connection(device,username,password):
    try:
        connection = ConnectHandler(
            device_type=device['device_type'],
            host=device['host'],
            username=username,
            password=password
        )
        return connection
    except NetmikoTimeoutException:
        print(f"Connection to {device['hostname']} is unreachable.")
        return None
    except NetmikoAuthenticationException:
        print(f"Authentication for {device['hostname']} failed.")
        return None

def print_report(results):
    for result in results:
        print(f"Hostname: {result['hostname']}")
        print(f"Device Type: {result['device_type']}")
        print(f"Status: {result['status']}")
        print(f"Output:\n{result['output']}")
        print("-" * 80)
    summary = (f"Total Devices: {len(results)}, "
               f"Successful: {len([r for r in results if r['status'] == 'Success'])}, "
               f"Failed: {len([r for r in results if r['status'] == 'Failed'])}")
    print(f"Summary: {summary}")

if __name__ == "__main__":
    username, password = get_credentials()
    inventory = get_inventory()
    results = []

    for device in inventory:
        connection = build_connection(device, username, password)
        report = {}
        if connection:
            try:
                output = connection.send_command('show ip int brief')
                report = {
                    'hostname': device['hostname'],
                    'output': output,
                    'device_type': device['device_type'],
                    'status': 'Success'
                }
            except Exception as e:
                print(f"Error occurred while sending command to {device['hostname']}: {e}")
                output = f"Error: {e}"
                report = {
                    'hostname': device['hostname'],
                    'output': output,
                    'device_type': device['device_type'],
                    'status': 'Failed'
                }
            finally:
                connection.disconnect()
        else:
            report = {
                'hostname': device['hostname'],
                'output': 'Connection Failed',
                'device_type': device['device_type'],
                'status': 'Failed'
            }
        results.append(report)
    print_report(results)