import subprocess
# module 7
def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None
    
command = "sudo ufw status numbered"
output = execute_command(command)
print(output)
number = int(input("Rule number: "))
command1= f"echo 'y' | sudo ufw delete {number}"
output1 = execute_command(command1)
print(output1)