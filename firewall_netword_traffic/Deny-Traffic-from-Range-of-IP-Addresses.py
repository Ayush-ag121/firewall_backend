#Deny Traffic from a Subnet or Range of IP Addresses

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

def allow_ip(ip):
    command = f"sudo ufw deny from {ip}"
    execute_command(command)

ip = input("Enter the Range of IP address: ")
deny_ip(ip)