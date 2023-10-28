import paramiko

# Create an SSH client
ssh = paramiko.SSHClient()

try:
    # Set the missing host key policy to automatically add unknown hosts
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("one")
    # Connect to the SSH server
    hostname = "10.1.40.145"  # Replace with the actual hostname or IP address
    port = 22  # The default SSH port
    username = "vb"  # Replace with the actual username
    password = "vbrobot123"  # Replace with the actual password
    print("one")
    ssh.connect(hostname, port, username, password)
    print("SSH connection established.")
    
    # Open an SFTP session
    sftp = ssh.open_sftp()

    # Now you can use sftp to perform file operations
    # For example, to upload a file to the remote server:
    local_file_path = "/home/vb/test.txt"  # Replace with the actual local file path
    remote_file_path = "/home/vb/test.txt"  # Replace with the actual remote file path
    sftp.get(local_file_path, remote_file_path)

    print(f"File '{local_file_path}' uploaded to '{remote_file_path}'.")

    # Don't forget to close the SFTP session when you're done
    sftp.close()

except paramiko.AuthenticationException:
    print("Authentication failed.")
except paramiko.SSHException as e:
    print(f"SSH connection failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the SSH connection when you're done, even if an exception occurs
    ssh.close()
