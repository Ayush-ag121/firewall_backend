import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

print("choices: off, low, medium, high and full")
option = input("Enter Choice: ")
command = f"sudo ufw logging {option}"
output = execute_command(command)
print(output)
print(f"Logging set to {option}")