import os
import csv
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from dotenv import load_dotenv
import json

load_dotenv()

def get_inventory(filepath):
    inventory = []
    with open (filepath) as csvfile:
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

def load_golden_vlans(filepath):
    with open(filepath) as f:
        golden_vlans = json.load(f)
    return golden_vlans

def parse_vlans(output):
    vlans = []
    for line in output.splitlines():
        if line and line[0].isdigit():
            vlan_id = int(line.split()[0])
            if vlan_id not in range(1002, 1006):
                vlans.append(vlan_id)
    return vlans

def compare_vlans(golden, actual):
    missing_vlans = set(golden) - set(actual)
    extra_vlans = set(actual) - set(golden)
    return {
        "missing_vlans": missing_vlans,
        "extra_vlans": extra_vlans
    }

def parse_trunks(output):
    trunks = []
    for line in output.splitlines():
        if 'trunking' in line.lower():
            trunks.append(line.split()[0])
    return trunks

def print_report(results):
    for report in results:
        print(f"Report for {report['hostname']}:")
        print(f"  Missing VLANs: {report['missing_vlans']}")
        print(f"  Extra VLANs: {report['extra_vlans']}")
        print(f"  Trunks: {report['trunks']}")
        if 'error' in report:
            print(f"  Error: {report['error']}")
    summary = {
        "total_devices": len(results),
        "devices_with_issues": sum(1 for r in results if r['missing_vlans'] or r['extra_vlans']),
        "devices_without_issues": sum(1 for r in results if not r['missing_vlans'] and not r['extra_vlans']),
        "noncompliant": [r['hostname'] for r in results if r['missing_vlans'] or r['extra_vlans']]
    }
    print(f"Summary:")
    print(f"  Total devices: {summary['total_devices']}")
    print(f"  Devices with issues: {summary['devices_with_issues']}")
    print(f"  Devices without issues: {summary['devices_without_issues']}")
    print(f"  Noncompliant devices: {summary['noncompliant']}")

if __name__ == "__main__":
    inventory = get_inventory('devices.csv')
    username, password = get_credentials()
    golden_vlans = load_golden_vlans('golden_vlans.json')
    results = []

    for device in inventory:
        if device['hostname'] in golden_vlans:
            connection = build_connection(device, username, password)
            if connection:
                try:
                    vlan_output = connection.send_command('show vlan brief')
                    deployed_vlans = parse_vlans(vlan_output)
                    current_golden_vlans = golden_vlans[device['hostname']]
                    result = compare_vlans(current_golden_vlans, deployed_vlans)
                    trunk_output = connection.send_command('show interfaces trunk')
                    parsed_trunks = parse_trunks(trunk_output)
                    report = {
                        'hostname': device['hostname'],
                        'missing_vlans': result['missing_vlans'],
                        'extra_vlans': result['extra_vlans'],
                        'trunks': parsed_trunks
                    }
                except Exception as e:
                    report = {
                        'hostname': device['hostname'],
                        'missing_vlans': set(),
                        'extra_vlans': set(),
                        'trunks': [],
                        'error': str(e)
                    }
                finally:
                    connection.disconnect()
            else:
                report = {
                    'hostname': device['hostname'],
                    'missing_vlans': set(),
                    'extra_vlans': set(),
                    'trunks': []
                }
            results.append(report)
    print_report(results)