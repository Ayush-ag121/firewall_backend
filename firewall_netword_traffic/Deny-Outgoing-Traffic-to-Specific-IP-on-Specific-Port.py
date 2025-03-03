#Deny Outgoing Traffic to a Specific IP on a Specific Port

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

def allow_ip(number, ip):
    command = f"sudo ufw deny out to {ip} port {number}"
    execute_command(command)


number = input("Enter Port Number: ")
ip = input("Enter the IP address: ")
deny_ip(number,ip)