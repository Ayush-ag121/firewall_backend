import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None
    
def deny_port_module2_fifth(port):
    print(f"Denying port {port}")
    command = f"sudo ufw deny {port}"
    execute_command(command)

port_to_disable = input("Enter the Port to Disable: ")
deny_port_module2_fifth(port_to_disable)