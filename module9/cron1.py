from flask import Flask, jsonify, request
import subprocess
import re
from collections import defaultdict

app = Flask(__name__)

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def ssh_log_analys():
    ip_pattern = r'from (\d+\.\d+\.\d+\.\d+)'
    ip_counts = defaultdict(int)
    
    with open('/var/log/auth.log', 'r') as file:
        for line in file:
            if "Failed password" in line:
                match = re.search(ip_pattern, line)
                if match:
                    ip_address = match.group(1)
                    ip_counts[ip_address] += 1
    
    ip_to_block = None
    for ip, count in ip_counts.items():
        if count > 5:
            print(f"[+] IP Address: {ip} -- Failed password attempts: {count}")
            ip_to_block = ip
    return ip_to_block

def is_ip_blocked_in_sshd_config(ip_to_match):
    try:
        with open('/etc/ssh/sshd_config', 'r') as file:
            for line in file:
                if f"DenyUsers *@{ip_to_match}" in line:
                    return True
    except FileNotFoundError:
        print("[*] /etc/ssh/sshd_config not found.")
    return False

def block_ip_in_sshd_config(ip_to_match):
    if not is_ip_blocked_in_sshd_config(ip_to_match):
        print(f"[+] Blocking IP: {ip_to_match}")
        execute_command(f"echo 'DenyUsers *@{ip_to_match}' | sudo tee -a /etc/ssh/sshd_config")
        execute_command("systemctl restart sshd")
    else:
        print(f"[+] IP {ip_to_match} is Already Blocked.")



if __name__ == '__main__':
    app.run(debug=True)
