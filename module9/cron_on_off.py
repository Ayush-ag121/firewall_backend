from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

# The command to be added/removed in crontab
cron_command = "/usr/bin/python3 /home/all_modules/module9/cron1.py 2>&1"
cron_schedule = "*/5 * * * *"  # Example: runs every hour, modify as needed
cron_job = f"{cron_schedule} {cron_command}"

# Function to add the cron job
def add_cron_job():
    try:
        # Retrieve current crontab
        current_crontab = subprocess.check_output("crontab -l", shell=True, text=True)
    except subprocess.CalledProcessError:
        # If no crontab exists, start with an empty string
        current_crontab = ""
    
    # Check if the command already exists in the crontab
    if cron_command not in current_crontab:
        # Add the new cron job to the crontab
        with open("/tmp/new_crontab", "w") as temp_file:
            temp_file.write(current_crontab + cron_job + "\n")
        
        # Set the new crontab
        subprocess.run("crontab /tmp/new_crontab", shell=True)
        return "Cron job added successfully."
    else:
        return "Cron job already exists."

# Function to remove the cron job
def remove_cron_job():
    try:
        # Retrieve current crontab
        current_crontab = subprocess.check_output("crontab -l", shell=True, text=True)
    except subprocess.CalledProcessError:
        # If no crontab exists, nothing to remove
        return "No crontab exists to remove jobs from."
    
    # Check if the command exists in the crontab
    if cron_command in current_crontab:
        # Remove the cron job by excluding the line containing the cron command
        new_crontab = "\n".join(line for line in current_crontab.splitlines() if cron_command not in line)
        
        # Set the new crontab
        with open("/tmp/new_crontab", "w") as temp_file:
            temp_file.write(new_crontab + "\n")
        
        subprocess.run("crontab /tmp/new_crontab", shell=True)
        return "Cron job removed successfully."
    else:
        return "Cron job does not exist."

