import subprocess
# module 5
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

option1 = "/var/log/ufw.log.1"
option = "/var/log/ufw.log"
command = f"sudo cat {option} {option1}"
output = execute_command(command)
print(output)