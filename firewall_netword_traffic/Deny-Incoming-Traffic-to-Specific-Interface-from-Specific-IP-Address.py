#Deny Incoming Traffic to a Specific Interface from a Specific IP Address

import subprocess
import re

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def deny_ip_module6_fifth(interface, ip):
    command = f"sudo ufw deny in on {interface} from {ip}"
    execute_command(command)

def get_network_interfaces_module6_fifth():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        pattern = r"^([a-zA-Z0-9-]+):"
        interfaces = re.findall(pattern, result.stdout, re.MULTILINE)
        return interfaces
    except subprocess.CalledProcessError:
        return []
    except Exception:
        return []

interfaces = get_network_interfaces_module6_fifth()
print(f"Network Interfaces: {interfaces}")
interface = input("Enter the Interface: ")
ip = input("Enter the IP address: ")
deny_ip_module6_fifth(interface,ip)