import argparse
import ipaddress

def build_parser():
    parser = argparse.ArgumentParser(description='Calculate the subnet information in a given network prefix.')

    parser.add_argument('--network', required=True, help='The network prefix to calculate (e.g. 192.168.10.0/24)')
    parser.add_argument('--check', help='Check if a specific IP address is within the subnet')
    return parser

def subnet_info(network):
    try:
        net = ipaddress.ip_network(network, strict=False)
    except ValueError as e:
        print(f'Error: {e}')
        return

    print('=' * 55)
    print(f'{'SUBNET INFORMATION':^55}')
    print(f'Input network: {network}')
    print('=' * 55)

    print(f'Network address: {net.network_address}')
    print(f'Broadcast address: {net.broadcast_address}')
    print(f'Subnet mask: {net.netmask}')
    print(f'Number of usable hosts: {net.num_addresses - 2}')
    print(f'Usable host range: {net.network_address + 1 } - {net.broadcast_address - 1}')

def check_ip(network, ip):
    check = ipaddress.ip_address(ip)
    net = ipaddress.ip_network(network, strict=False)
    print('=' * 55)
    if check in net:
        print('✓ in subnet')
    else:
        print('✗ not in subnet')

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    subnet_info(args.network)
    if args.check:
        check_ip(args.network, args.check)