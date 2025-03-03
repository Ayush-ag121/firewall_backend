#Allow inbound HTTP traffic
# module 8
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

def allow_ip_module8_first(number):
    command = f"sudo ufw allow from any to any port {number} proto tcp"
    execute_command(command)

number = input("Enter the Port Number: ")
allow_ip_module8_first(number)