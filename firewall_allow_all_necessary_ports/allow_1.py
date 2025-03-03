import subprocess
# module 2
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None
    
def allow_port(port):
    print(f"Allowing port {port}")
    command = f"sudo ufw allow {port}"
    return execute_command(command)

