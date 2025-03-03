import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None


def list_allow_ports_module2_seventh():
    command = "sudo ufw status numbered"
    output = execute_command(command)
    if output:
        return [line.split()[2] for line in output.splitlines() if 'ALLOW' in line]
    return []

def deny_all_module2_seventh():
    allow_ports = list_allow_ports_module2_seventh()
    for port in allow_ports:
        print(f"Blocking port {port}")
        command = f"sudo ufw deny {port}"
        execute_command(command)
        
deny_all_module2_seventh()