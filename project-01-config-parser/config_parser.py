import argparse

def argument_parser():
    parser = argparse.ArgumentParser(description='Parse a network device configuration file.')
    parser.add_argument('--file', type=str, default='running_config.txt', help='Path to the configuration file')
    return parser.parse_args()



def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('interface'):
                current_interface = line.split()[1]
                config[current_interface] = {}
            elif line.startswith('description'):
                config[current_interface]['description'] = line.split(' ', 1)[1]
            elif line.startswith('ip address'):
                if line.split()[2] == 'dhcp':
                    config[current_interface]['ip_address'] = 'dhcp'
                elif line.split()[2] == 'negotiated':
                    config[current_interface]['ip_address'] = 'negotiated'
                else:
                    config[current_interface]['ip_address'] = line.split(' ', 2)[2]
            elif line.startswith('encapsulation'):
                config[current_interface]['encapsulation'] = line.split(' ', 1)[1]
            elif line.startswith('bridge-group'):
                config[current_interface]['bridge_group'] = line.split(' ', 1)[1]
            elif line.startswith('shutdown'):
                config[current_interface]['shutdown'] = True    
    return config

def print_report(config):
    for interface, details in config.items():
        print(f"Interface: {interface}")
        print(f"  Description: {details.get('description', 'None')}")
        print(f"  IP Address: {details.get('ip_address', 'None')}")
        print(f"  Encapsulation: {details.get('encapsulation', 'None')}")
        print(f"  Bridge Group: {details.get('bridge_group', 'None')}")
        print(f"  Shutdown: {'Yes' if details.get('shutdown', False) else 'No'}")

if __name__ == "__main__":
    args = argument_parser()
    config_data = read_config(args.file)
    print_report(config_data)