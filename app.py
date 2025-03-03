from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import re
from collections import defaultdict
# module2 Imports
from firewall_allow_all_necessary_ports.allow_all_deny_port_1 import manage_ports,list_deny_ports,allow_all_ports,deny_port  # Import allow_port
from firewall_allow_all_necessary_ports.app_list import list_apps_module2_fourth,allow_app_module2_fourth  # Import allow_port
from firewall_allow_all_necessary_ports.show_all_ports import show_all_module2_eight
from firewall_allow_all_necessary_ports.allow_1 import allow_port  # Import allow_port
# modeule3 Imports
from firewall_blocking_ip.block_range_of_ip_address import block_module3_first
from firewall_blocking_ip.block_specific_ip import block_module3_second
from module9.cron1 import block_ip_in_sshd_config,is_ip_blocked_in_sshd_config,ssh_log_analys
from module9.cron_on_off import add_cron_job,remove_cron_job

import subprocess

app = Flask(__name__)
CORS(app)  # Apply CORS to your app

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None


# module 2
@app.route('/api/allow-port', methods=['POST'])
def allow_port_route():
    # Get the port number from the JSON request
    data = request.get_json()
    if 'port' not in data:
        return jsonify({"error": "Port is required"}), 400
    
    port = data['port']
    print(port)
    # Try to allow the port
    result = allow_port(port)
    print(result)
    if result:
        return jsonify({"message": f"Port {port} allowed successfully", "output": result}), 200
    else:
        return jsonify({"error": "Failed to allow port"}), 500


@app.route('/api/list-deny-ports', methods=['GET'])
def list_deny_ports1():
    ports = list_deny_ports()
    return jsonify({"deny_ports": ports}), 200

@app.route('/api/allow-all-ports', methods=['POST'])
def allow_all_ports1():
    allow_all_ports()
    return jsonify({"message": "All ports allowed successfully"}), 200

@app.route('/api/deny-port', methods=['POST'])
def deny_port1():
    data = request.get_json()
    if 'port' not in data:
        return jsonify({"error": "Port is required"}), 400

    port = data['port']
    deny_port(port)
    return jsonify({"message": f"Port {port} denied successfully"}), 200

@app.route('/api/manage-ports', methods=['POST'])
def manage_ports1():
    data = request.get_json()
    if 'port_to_disable' not in data:
        return jsonify({"error": "Port to disable is required"}), 400

    port_to_disable = data['port_to_disable']
    manage_ports(port_to_disable)
    return jsonify({"message": f"Port {port_to_disable} managed successfully"}), 200

# Endpoint to list all denied ports
@app.route('/api/denied-ports', methods=['GET'])
def get_denied_ports():
    denied_ports = list_deny_ports_third()
    if isinstance(denied_ports, str):  # Check if an error message was returned
        return jsonify({"error": denied_ports}), 500
    return jsonify({"denied_ports": denied_ports})

# Endpoint to allow all denied ports
# @app.route('/api/allow-all', methods=['POST'])
# def allow_all_ports():
#     result = allow_all_third()
#     if isinstance(result, str) and result.startswith("No denied ports"):
#         return jsonify({"message": result}), 400
#     return jsonify({"message": result})


#module 2 fourth
@app.route('/api/apps', methods=['GET'])
def get_apps_module2_fourth():
    apps = list_apps_module2_fourth()
    if apps is None:
        return jsonify({"error": "Failed to fetch application list"}), 500
    return jsonify({"apps": apps})

# Endpoint to allow an application
@app.route('/api/allow-app', methods=['POST'])
def allow_application_module2_fourth():
    data = request.get_json()
    print(data)
    app_name = data.get("app")
    if not app_name:
        return jsonify({"error": "Application name is required"}), 400

    result = allow_app_module2_fourth(app_name)
    if result is None:
        return jsonify({"error": f"Failed to allow application '{app_name}'"}), 500
    return jsonify({"message": f"Application '{app_name}' allowed successfully."})

#module2 eight
@app.route('/api/show-all', methods=['GET'])
def get_firewall_status():
    rules = show_all_module2_eight()
    if rules is None:
        return jsonify({"error": "Failed to fetch firewall status"}), 500
    return jsonify({"rules": rules})

@app.route('/api/block-ip-third', methods=['POST'])
def block_ip():
    data = request.json
    ip = data.get('ip')
    print(ip)
    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    result = block_module3_first(ip)
    if result:
        return jsonify({"message": f"IP {ip} blocked successfully", "result": result}), 200
    else:
        return jsonify({"error": f"Failed to block IP {ip}"}), 500


@app.route('/api/block-ip-single', methods=['POST'])
def block_ip_single():
    data = request.json
    ip = data.get('ip')
    if not ip:
        return jsonify({"error": "IP address is required"}), 400

    result = block_module3_second(ip)
    if result:
        return jsonify({"message": f"IP {ip} blocked successfully", "result": result}), 200
    else:
        return jsonify({"error": f"Failed to block IP {ip}"}), 500


@app.route('/default-deny', methods=['POST'])
def default_deny():
    output = execute_command("sudo ufw default deny incoming")
    return jsonify({"result": output})

@app.route('/default-allow', methods=['POST'])
def default_allow():
    output = execute_command("sudo ufw default allow outgoing")
    return jsonify({"result": output})

@app.route('/fetch-status', methods=['GET'])
def fetch_status():
    output = execute_command("sudo ufw status verbose")
    return jsonify({"result": output})

@app.route('/ufw-enable', methods=['POST'])
def enable_ufw_module4_enable():
    output = execute_command("sudo ufw enable")
    return jsonify({"result": output})

@app.route('/ufw-disable', methods=['POST'])
def disable_ufw_module4_disable():
    output = execute_command("sudo ufw disable")
    return jsonify({"result": output})



FILE_PATH = '/etc/default/ufw'

def update_ipv6_in_file(new_value):
    if os.geteuid() != 0:
        return {
            "error": True,
            "message": "This script requires root privileges to modify /etc/default/ufw"
        }
    
    try:
        with open(FILE_PATH, 'r') as file:
            lines = file.readlines()

        updated = False
        for i, line in enumerate(lines):
            if line.startswith('IPV6='):
                lines[i] = f'IPV6={new_value}\n'
                updated = True
                break

        if not updated:
            lines.append(f'IPV6={new_value}\n')

        with open(FILE_PATH, 'w') as file:
            file.writelines(lines)

        return {"success": True, "message": f"Updated IPV6 to {new_value}"}
    except Exception as e:
        return {"error": True, "message": str(e)}

@app.route('/update-ipv6', methods=['POST'])
def update_ipv6():
    data = request.json
    new_value = data.get('value')
    if not new_value:
        return jsonify({"error": "No value provided"}), 400

    result = update_ipv6_in_file(new_value)
    return jsonify(result)


@app.route('/get-ufw-logs', methods=['GET'])
def get_ufw_logs_module5():
    command = "sudo cat /var/log/ufw.log /var/log/ufw.log"
    output = execute_command(command)
    if isinstance(output, dict) and output.get("error"):
        return jsonify(output), 500
    return jsonify({"logs": output})



def execute_command_module5(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "error": f"Command '{command}' failed with exit code {e.returncode}",
            "stderr": e.stderr.strip()
        }


@app.route('/set-ufw-logging', methods=['POST'])
def set_ufw_logging_module5():
    data = request.json
    option = data.get('option', '').lower()

    if option not in ['off', 'low', 'medium', 'high', 'full']:
        return jsonify({"success": False, "error": "Invalid logging level"}), 400

    command = f"sudo ufw logging {option}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"message": f"Logging set to {option}", "output": result["output"]})
    else:
        return jsonify({"error": result["error"], "stderr": result["stderr"]}), 500


# module6

# Allow incoming traffic from a specific IP address to a specific interface
@app.route('/allow-ip-module6', methods=['POST'])
def allow_ip_module6():
    data = request.json
    interface = data.get('interface')
    ip = data.get('ip')

    if not interface or not ip:
        return jsonify({"success": False, "error": "Interface and IP address are required"}), 400

    command = f"sudo ufw allow in on {interface} from {ip}"
    result = execute_command(command)

    if 'failed' in result.lower():
        return jsonify({"success": False, "error": result}), 500
    else:
        return jsonify({"success": True, "message": f"Allowed incoming traffic on {interface} from {ip}"}), 200

# Get the list of network interfaces on the system
@app.route('/get-interfaces', methods=['GET'])
def get_interfaces_module6():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        pattern = r"^([a-zA-Z0-9-]+):"
        interfaces = re.findall(pattern, result.stdout, re.MULTILINE)
        return jsonify({"success": True, "interfaces": interfaces}), 200
    except subprocess.CalledProcessError:
        return jsonify({"success": False, "error": "Failed to get network interfaces"}), 500
    except Exception as e:
        print("sdssdkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkds",e)
        return jsonify({"success": False, "error": str(e)}), 500



# Route to allow incoming traffic on a specific port from a specific IP
@app.route('/allow-port-ip', methods=['POST'])
def allow_port_ip_module6_second():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({"success": False, "error": "Both IP address and port number are required."}), 400

    command = f"sudo ufw allow from {ip} to any port {port}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Allowed incoming traffic from {ip} to port {port}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500




# API to allow outgoing traffic to a specific IP address
@app.route('/allow-outgoing-ip', methods=['POST'])
def allow_outgoing_ip_module6_third():
    data = request.json
    ip = data.get('ip')

    if not ip:
        return jsonify({"success": False, "error": "IP address is required."}), 400

    command = f"sudo ufw allow out to {ip}"
    result = execute_command_module5(command)
    print(result)
    if result["success"]:
        return jsonify({"success": True, "message": f"Allowed outgoing traffic to {ip}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500


@app.route('/allow-outgoing-port-ip', methods=['POST'])
def allow_outgoing_port_ip():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({"success": False, "error": "IP address and port number are required."}), 400

    command = f"sudo ufw allow out to {ip} port {port}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Allowed outgoing traffic to {ip} on port {port}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500





# Function to get network interfaces
def get_network_interfaces():
    try:
        result = subprocess.run(['ifconfig'], capture_output=True, text=True, check=True)
        pattern = r"^([a-zA-Z0-9-]+):"
        interfaces = re.findall(pattern, result.stdout, re.MULTILINE)
        return interfaces
    except subprocess.CalledProcessError:
        return []

# API to get available network interfaces
@app.route('/get-interfaces', methods=['GET'])
def get_interfaces():
    interfaces = get_network_interfaces()
    if interfaces:
        return jsonify({"success": True, "interfaces": interfaces})
    else:
        return jsonify({"success": False, "error": "No interfaces found."})

# API to deny incoming traffic on a specific interface from a specific IP
@app.route('/deny-incoming-ip', methods=['POST'])
def deny_incoming_ip():
    data = request.json
    interface = data.get('interface')
    ip = data.get('ip')

    if not interface or not ip:
        return jsonify({"success": False, "error": "Interface and IP address are required."}), 400

    command = f"sudo ufw deny in on {interface} from {ip}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Denied incoming traffic from {ip} on interface {interface}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500







# API to deny incoming traffic to a specific port from a specific IP
@app.route('/deny-port-ip', methods=['POST'])
def deny_port_ip():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({"success": False, "error": "IP address and Port number are required."}), 400

    command = f"sudo ufw deny from {ip} to any port {port}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Denied incoming traffic from {ip} on port {port}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500


@app.route('/deny-outgoing-port-ip', methods=['POST'])
def deny_outgoing_port_ip_module6():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({"success": False, "error": "IP address and Port number are required."}), 400

    command = f"sudo ufw deny out to {ip} port {port}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Denied outgoing traffic to {ip} on port {port}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500


@app.route('/deny-outgoing-port-ip', methods=['POST'])
def deny_outgoing_port_ip_module6_lastSecond():
    data = request.json
    ip = data.get('ip')
    port = data.get('port')

    if not ip or not port:
        return jsonify({"success": False, "error": "IP address and Port number are required."}), 400

    command = f"sudo ufw deny out to {ip} port {port}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Denied outgoing traffic to {ip} on port {port}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500




@app.route('/deny-subnet', methods=['POST'])
def deny_subnet():
    data = request.json
    ip_range = data.get('ip_range')

    if not ip_range:
        return jsonify({"success": False, "error": "IP range is required."}), 400

    command = f"sudo ufw deny from {ip_range}"
    result = execute_command_module5(command)

    if result["success"]:
        return jsonify({"success": True, "message": f"Denied traffic from {ip_range}"}), 200
    else:
        return jsonify({"success": False, "error": result["stderr"]}), 500




#module 8

@app.route('/allow-http-port', methods=['POST'])
def allow_http_port():
    data = request.json
    port = data.get('port')
    
    if not port or not port.isdigit():
        return jsonify({"success": False, "message": "Invalid port number"}), 400
    
    command = f"sudo ufw allow from any to any port {port} proto tcp"
    output = execute_command(command)
    
    if "Rule added" in output or "Rule updated" in output:
        return jsonify({"success": True, "message": f"Inbound HTTP traffic allowed on port {port}"})
    else:
        return jsonify({"success": False, "message": output})


@app.route('/allow-ip-module8', methods=['POST'])
def allow_ip_module8():
    data = request.get_json()
    ip = data.get('ip')
    if not ip or not re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip):
        return jsonify({"success": False, "message": "Invalid IP address"}), 400
    command = f"sudo ufw allow from {ip}"
    result = execute_command(command)
    return jsonify({"success": True, "message": f"Traffic allowed from {ip}", "output": result}), 200

@app.route('/allow-subnet', methods=['POST'])
def allow_subnet():
    data = request.get_json()
    ip_range = data.get('ip_range')
    # Basic validation for CIDR notation or IP range (like 192.168.1.0/24)
    if not ip_range or not re.match(r'^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$|^\d{1,3}(\.\d{1,3}){3}-\d{1,3}$', ip_range):
        return jsonify({"success": False, "message": "Invalid IP range or subnet"}), 400
    command = f"sudo ufw allow from {ip_range}"
    result = execute_command(command)
    return jsonify({"success": True, "message": f"Traffic allowed from {ip_range}", "output": result}), 200

@app.route('/deny-ip-module8', methods=['POST'])
def deny_ip_module8():
    data = request.get_json()
    ip_address = data.get('ip_address')
    # Validate IP address format
    if not ip_address or not re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip_address):
        return jsonify({"success": False, "message": "Invalid IP address format"}), 400
    command = f"sudo ufw deny from {ip_address}"
    result = execute_command(command)
    return jsonify({"success": True, "message": f"Traffic denied from {ip_address}", "output": result}), 200





@app.route('/ufw-status-module9', methods=['GET'])
def ufw_status_module9():
    command = "sudo ufw status numbered"
    output = execute_command(command)
    if output:
        return jsonify({"success": True, "status": output.splitlines()})
    else:
        return jsonify({"success": False, "message": "Unable to retrieve UFW status"}), 500

@app.route('/delete-rule', methods=['POST'])
def delete_rule():
    data = request.get_json()
    rule_number = data.get("rule_number")
    if not isinstance(rule_number, int):
        return jsonify({"success": False, "message": "Invalid rule number"}), 400

    command = f"echo 'y' | sudo ufw delete {rule_number}"
    output = execute_command(command)
    return jsonify({"success": True, "message": output}), 200



def ssh_log_analysis():
    ip_pattern = r'from (\d+\.\d+\.\d+\.\d+)'
    ip_counts = defaultdict(int)
    try:
        with open('/var/log/auth.log', 'r') as file:
            for line in file:
                if "Failed password" in line:
                    match = re.search(ip_pattern, line)
                    if match:
                        ip_address = match.group(1)
                        ip_counts[ip_address] += 1
    except FileNotFoundError:
        return {"error": "Log file not found: /var/log/auth.log"}
    return [{"ip": ip, "count": count} for ip, count in ip_counts.items() if count > 4]

def manage_ip(ip):
    try:
        with open('ips.txt', 'r') as file:
            if ip in file.read().splitlines():
                return {"message": f"IP {ip} is already blocked"}
    except FileNotFoundError:
        pass

    execute_command(f"echo 'DenyUsers *@{ip}' >> /etc/ssh/sshd_config")
    execute_command("systemctl restart sshd")
    with open('ips.txt', 'a') as file:
        file.write(f"{ip}\n")
    return {"message": f"IP {ip} has been blocked"}

@app.route('/analyze', methods=['GET'])
def analyze_logs():
    analysis_result = ssh_log_analysis()
    print(analysis_result)
    return jsonify(analysis_result)

@app.route('/block', methods=['POST'])
def block_ipbruteforce():
    data = request.get_json()
    ip = data.get('ip')
    if not ip:
        return jsonify({"error": "IP address is required"}), 400
    result = manage_ip(ip)
    return jsonify(result)





# module 9

@app.route('/api/ssh_log_analysis', methods=['POST'])
def ssh_log_analysis():
    ip = ssh_log_analys()
    if ip:
        block_ip_in_sshd_config(ip)
        return jsonify({"message": f"IP {ip} blocked successfully!"}), 200
    else:
        return jsonify({"message": "No IP to block."}), 200



@app.route('/api/add_cron_job', methods=['POST'])
def api_add_cron_job():
    result = add_cron_job()
    return jsonify({"message": result})

@app.route('/api/remove_cron_job', methods=['POST'])
def api_remove_cron_job():
    result = remove_cron_job()
    return jsonify({"message": result})






if __name__ == "__main__":
    app.run()
