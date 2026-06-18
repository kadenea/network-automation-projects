import csv
import argparse

def load_devices(filepath):
    devices = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader: devices.append(row)
    return devices

def filter_devices(devices, device_type=None, location=None):
    filtered = devices
    if device_type:
        filtered = [d for d in filtered if device_type.lower() in d['device_type'].lower()]
    if location:
        filtered = [d for d in filtered if location.lower() in d['location'].lower()]
    return filtered

def print_report(devices):
    print('=' * 55)
    print(f'{'NETWORK DEVICE INVENTORY':^55}')
    print(f'Total devices: {len(devices)}')
    print('=' * 55)

    for device in devices:
        print(f'Hostname: {device['hostname']}')
        print(f'IP Address: {device['ip_address']}')
        print(f'Type: {device['device_type']}')
        print(f'Location: {device['location']}')
        print(f'VLAN Count: {device['vlan_count']}')
        print('-' * 55)

def build_parser():
    parser = argparse.ArgumentParser(description='Print a network device inventory report.')

    parser.add_argument('--file', default='devices.csv', help='Path to the CSV file.')
    parser.add_argument('--type', dest='device_type', help='Filter by device type (e.g., Router, Switch).')
    parser.add_argument('--location', help='Filter by location (e.g., "Floor1")')
    return parser

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    devices = load_devices(args.file)
    devices = filter_devices(devices, device_type=args.device_type, location=args.location)

    if not devices:
        print('No devices matched your filters.')
    else:
        print_report(devices)