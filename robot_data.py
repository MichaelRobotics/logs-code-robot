import paramiko
import os

LOCAL_PATH_TO_SCRIPT = '/home/vb/Bsst-logs-code/container_script.py'
REMOTE_PATH_TO_SCRIPT = '/tmp/container_script.py'
REMOTE_PATH_TO_LOGS = "/tmp/testfile.txt"

class RobotData:
    """
        Klasa tworząca obiekt zawierający pożądany rodzaj loga
    """
    def __init__(self, hostname: str, port: int, username: str, password: str):
        """
            Definiowanie danych do logowania i zmiennych komunikacyjnych
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.sftp = None

    def check_path(self, file_path):
        
        if file_path == LOCAL_PATH_TO_SCRIPT:
            if not os.path.exists(file_path):
                raise Exception(f"Script not present localy in: '{file_path}' ! ! !")
            
    def check_passed_local_paths(self):
        """
            Check if paths to file is already taken by other file or dir
        """
        try:
            self.check_path(LOCAL_PATH_TO_SCRIPT)
        except Exception as e:
            print("An exception occurred:", str(e))
            
    def invoke_ssh_connection(self):
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                print("connecting...")
                self.ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password, timeout=180)
                print("connected")
            except Exception as exc:
                print(exc)

    def create_sftp_client(self):
        try:
            self.sftp = self.ssh.open_sftp()
        except Exception as sftp_error:
            print(f'Error creating SFTP client: {str(sftp_error)}')
    
    def send_script_to_container(self):
        try:
            self.create_sftp_client()
            # Upload the script file
            self.sftp.put(LOCAL_PATH_TO_SCRIPT, REMOTE_PATH_TO_SCRIPT)
            print(f'Script file {LOCAL_PATH_TO_SCRIPT} uploaded successfully to {REMOTE_PATH_TO_SCRIPT}')
        except Exception as upload_error:
            print(f'Error uploading script file: {str(upload_error)}')
        finally:
            # Close the SFTP connection
            self.sftp.close()

    def execute_script_inside_container(self):
        try:
        # Execute the script remotely
            stdin, stdout, stderr = self.ssh.exec_command(f'python3 {REMOTE_PATH_TO_SCRIPT} {REMOTE_PATH_TO_LOGS}')

            # Wait for the command to complete
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("Script executed")
            else:
                print(f"Script execution failed with exit status {exit_status}")
                # You can print the error output if needed:
                print("Error output:")
                print(stderr.read().decode())
            output = stdout.read().decode()
            print(output)

        except paramiko.SSHException as ssh_error:
            print(f"SSH error: {ssh_error}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def download_log_file_from_robot(self, path_to_save):
        try:
            self.create_sftp_client()
            self.sftp.get(REMOTE_PATH_TO_LOGS, path_to_save)
            print(f"File '{path_to_save}' downloaded from '{REMOTE_PATH_TO_LOGS}'")
        except FileNotFoundError:
            print(f"Remote file not found")
        except Exception as e:
            print("An error occurred while downloading the file:", str(e))
        finally:
            # Close the SFTP session and the SSH connection
            self.sftp.close()
            
    def rm_buff_log_and_script_from_robot(self):
        try:
            # Remove the remote file using the 'rm' command
            rm_log = f'rm "{REMOTE_PATH_TO_LOGS}"'
            rm_script = f'rm "{REMOTE_PATH_TO_SCRIPT}"'
            stdin, stdout, stderr = self.ssh.exec_command(rm_log)
            if stderr.read():
                raise Exception(f"Error: {stderr.read().decode('utf-8')}")
            else:
                print(f"File {REMOTE_PATH_TO_LOGS} removed successfully.")

            stdin, stdout, stderr = self.ssh.exec_command(rm_script)
            if stderr.read():
                raise Exception(f"Error: {stderr.read().decode('utf-8')}")
            else:
                print(f"File {REMOTE_PATH_TO_SCRIPT} removed successfully.")
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
    def capture_container_log_data(self, path_to_save):
        try:
            self.check_passed_local_paths()
            self.invoke_ssh_connection()
            self.send_script_to_container()
            self.execute_script_inside_container()
            self.download_log_file_from_robot(path_to_save)
            self.rm_buff_log_and_script_from_robot()            
        finally:
            # Close the SSH connection
            self.ssh.close()