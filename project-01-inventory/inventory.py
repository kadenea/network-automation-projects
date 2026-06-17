import csv

def load_devices(filepath):
    devices = []
    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader: devices.append(row)
    return devices

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

if __name__ == '__main__':
    devices = load_devices('devices.csv')
    print_report(devices)