import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

# Function to show all firewall rules
def show_all_module2_eight():
    command = "sudo ufw status numbered"
    output = execute_command(command)
    if output:
        return output.splitlines()  # Return each line as a list item
    return None

