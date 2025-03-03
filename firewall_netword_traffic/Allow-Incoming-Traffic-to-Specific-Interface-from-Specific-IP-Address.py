#Allow Incoming Traffic to a Specific Interface from a Specific IP Address

import subprocess
import re
# module 6
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def allow_ip_module6_first(interface, ip):
    command = f"sudo ufw allow in on {interface} from {ip}"
    execute_command(command)

def get_network_interfaces_module6_first():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        pattern = r"^([a-zA-Z0-9-]+):"
        interfaces = re.findall(pattern, result.stdout, re.MULTILINE)
        return interfaces
    except subprocess.CalledProcessError:
        return []
    except Exception:
        return []

interfaces = get_network_interfaces_module6_first()
print(f"Network Interfaces: {interfaces}")
interface = input("Enter the Interface: ")
ip = input("Enter the IP address: ")
allow_ip_module6_first(interface,ip)