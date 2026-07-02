import os
import csv
import datetime
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from dotenv import load_dotenv

load_dotenv()

def get_inventory():
    inventory = []
    with open ('devices.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            inventory.append(row)
    return inventory

def get_credentials():
    username = os.getenv('LAB_USERNAME')
    password = os.getenv('LAB_PASSWORD')
    return username, password

def build_connection(device, username, password):
    try:
        connection = ConnectHandler(
            device_type = device['device_type'],
            host = device['host'],
            username = username,
            password = password
        )
    except NetmikoTimeoutException:
        print(f"Connection to {device['hostname']} is unreachable.")
        return None
    except NetmikoAuthenticationException:
        print(f"Authentication for {device['hostname']} failed.")
        return None
    return connection

def save_backup(hostname, config_output, backup_date, backup_dir):
    backup_file = f"{backup_dir}/{hostname}_{backup_date}.txt"
    try:
        with open(backup_file, 'w') as f:
            f.write(config_output)
        print(f"Backup for {hostname} saved successfully at {backup_file}.")
    except Exception as e:
        print(f"Failed to save backup for {hostname}: {e}")

if __name__ == "__main__":
    username, password = get_credentials()
    inventory = get_inventory()
    backup_date = datetime.date.today()
    backup_dir = f"backups/{backup_date}"
    os.makedirs(backup_dir, exist_ok=True)
    for device in inventory:
        connection = build_connection(device, username, password)
        if connection:
            try:
                config_output = connection.send_command('show running-config')
                save_backup(device['hostname'], config_output, backup_date, backup_dir)
            except Exception as e:
                print(f"Error occured while sending command to {device['hostname']}: {e}")
            finally:
                connection.disconnect()
        else:
            print(f'Connection to {device['hostname']} failed.')

