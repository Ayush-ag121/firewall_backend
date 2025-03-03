import os

file_path = '/etc/default/ufw'

def update_ipv6_in_file_module4_third(file_path, new_value):
    
    if os.geteuid() != 0:
        raise PermissionError("This script requires root privileges to modify /etc/default/ufw")

    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('IPV6='):
            
            lines[i] = f'IPV6={new_value}\n'
            updated = True
            break

    
    if not updated:
        lines.append(f'IPV6={new_value}\n')

    
    with open(file_path, 'w') as file:
        file.writelines(lines)

    print(f"Updated IPV6 to {new_value} in {file_path}")


new_ipv6_value = input("Enter the Value: ")

try:
    update_ipv6_in_file_module4_third(file_path, new_ipv6_value)
except PermissionError as e:
    print(e)
