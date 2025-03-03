import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr.strip()}")
        return None

def list_apps_module2_fourth():
    output = execute_command("sudo ufw app list")
    print(output)
    if output:
        return output.splitlines()[1:]  # Skip the header
    return None

def allow_app_module2_fourth(app_name):
    output =  execute_command(f"sudo ufw allow '{app_name}'")
    print(output)
    return output