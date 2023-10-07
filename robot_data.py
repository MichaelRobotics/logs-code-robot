import paramiko
import logging

# Specify the path to script for accesing robot container
CONTAINER_SCRIPT_FILE_PATH = 'container_script.py'

class RobotData:
    """
        Klasa tworząca obiekt zawierający pożądane logi robota i inne
    """
    def __init__(self, hostname: str, port: int, username: str, password: str):
        """
            Definiowanie danych do logowania
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def invoke_ssh_connection(self):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(self.hostname, port=self.port, username=self.username, password=self.password, timeout=180)
            except Exception as exc:
                ### loginfo(f'Failed to connect when restarting services, exc: {exc}')
                print(exc)
                ###raise TestsAutomationException('Failed to establish connection to stack PC')     
        return ssh
    
    def push_log_container_to_host(self):
        try:
            ssh = self.invoke_ssh_connection()

            # Run the Python script on the remote machine
            stdin, stdout, stderr = ssh.exec_command("python3 -")

            # Send the Python script to the remote machine
            stdin.write(self.container_script_as_string_to_send())
            stdin.flush()
            stdin.channel.shutdown_write()

            output = stdout.read().decode()
            print(output)

        except paramiko.SSHException as ssh_error:
            print(f"SSH error: {ssh_error}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            # Close the SSH connection
            ssh.close()

    def container_script_as_string_to_send(self):
        try:
            # Read the contents of the script file into a string
            with open(CONTAINER_SCRIPT_FILE_PATH, 'r') as file:
                script_content = file.read()
            return script_content
        except FileNotFoundError:
            print(f"Error: The file '{CONTAINER_SCRIPT_FILE_PATH}' does not exist.")
        except IOError as e:
            print(f"Error reading the file '{CONTAINER_SCRIPT_FILE_PATH}': {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def get_file_from_robot():
        pass

    