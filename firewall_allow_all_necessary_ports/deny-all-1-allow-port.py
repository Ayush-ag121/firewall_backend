import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def list_allowed_ports_module2_sixth():
    command = "sudo ufw status numbered"
    output = execute_command(command)
    if output:
        return [line.split()[2] for line in output.splitlines() if 'ALLOW' in line]
    return []

def deny_all_ports_module2_sixth():
    allowed_ports = list_allowed_ports_module2_sixth()
    for port in allowed_ports:
        print(f"Blocking port {port}")
        command = f"sudo ufw deny {port}"
        execute_command(command)

def allow_port_module2_sixth(port):
    print(f"Allowing port {port}")
    command = f"sudo ufw allow {port}"
    execute_command(command)

def manage_ports_module2_sixth(port_to_enable):
    deny_all_ports_module2_sixth()
    allow_port_module2_sixth(port_to_enable)

if __name__ == "__main__":
    port_to_enable = input("Enter the Port to allow: ")
    manage_ports_module2_sixth(port_to_enable)
