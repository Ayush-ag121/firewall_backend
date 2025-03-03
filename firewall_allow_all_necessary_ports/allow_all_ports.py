import subprocess

# Function to execute shell commands
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Command '{command}' failed with exit code {e.returncode}. Error: {e.stderr.strip()}"

# Function to list denied ports
def list_deny_ports_third():
    command = "sudo ufw status numbered"
    output = execute_command(command)
    print(output)
    if output and not output.startswith("Command"):
        return [line.split()[2] for line in output.splitlines() if 'DENY' in line]
    return []

# Function to allow all denied ports
def allow_all():
    deny_ports = list_deny_ports()
    if not deny_ports:
        return "No denied ports to allow."

    for port in deny_ports:
        command = f"sudo ufw allow {port}"
        output = execute_command(command)
        
    return f"Allowed all denied ports: {deny_ports}"
