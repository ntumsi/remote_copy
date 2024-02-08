import os
import paramiko
from shutil import copy2

# Windows directory with the photos
source_directory = 'source directory goes here'

# Directory on Linux where you want to copy the photos
target_directory = 'enter target directory'

# Files transferred between the directories
file_count = 0

# SSH details
ssh_hostname = 'enter host ip here'
ssh_username = 'enter user name here'
ssh_password = 'password goes here'  # or use key-based authentication
ssh_port = 22  # default SSH port

# Copy files from Windows to a temporary directory
temp_directory = 'D:\\temp_directory\\'
for filename in os.listdir(source_directory):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Add other file types if needed
        source_file = os.path.join(source_directory, filename)
        temp_file = os.path.join(temp_directory, filename)
        copy2(source_file, temp_file)

# Use SSH to send files from the temporary directory to the Linux machine
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ssh_hostname, port=ssh_port, username=ssh_username, password=ssh_password)

sftp = ssh.open_sftp()

# Check if the file already exists in the target directory
def remote_file_exists(sftp, path):
    try:
        sftp.stat(path)
        return True
    except IOError:
        return False

for filename in os.listdir(temp_directory):
    local_path = os.path.join(temp_directory, filename)
    remote_path = os.path.join(target_directory, filename)

    if not remote_file_exists(sftp, remote_path):
        sftp.put(local_path, remote_path)
        file_count += 1

sftp.close()
ssh.close()

print(f"Files transferred: {file_count}")
print("done")

# Optionally, clean up the temporary directory
for filename in os.listdir(temp_directory):
    os.remove(os.path.join(temp_directory, filename))
