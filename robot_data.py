# class RobotData is used to manage downloading/manipulating logs from instance of object
# which is connected to robot itself. Logs ready to download are stored on robot at location:
REMOTE_PATH_TO_LOGS = "/tmp/testfile.txt"


# In order to acces class funcionality, call capture_container_log_data function on its object.

# Order of tasks done by function:
# 1. Connect to robot using utils.SSHinvoker class
# 2. cp log from robot(robot log path is defined in main.py)
# into file: REMOTE_PATH_TO_LOGS, from which it will be downloaded to host
# 3. Send log from REMOTE_PATH_TO_LOGS to host using SFTPclient class
# 4. rm copied logs from REMOTE_PATH_TO_LOG 



import utils

class RobotData:
    """
        Klasa tworząca obiekt zawierający pożądany rodzaj loga
    """
    def __init__(self, hostname: str, id: str, port: int, username: str, password: str):
        """
            Definiowanie danych do logowania, id i zmiennych komunikacyjnych
        """
        self.hostname = hostname
        self._id = id
        self.port = port
        self.username = username
        self.password = password
        self.ssh = None
        self.sftp = None
    
    @property
    def id(self):
        return self._id
        
    def copy_log(self, log_path):
        try:
        # Execute the script remotely
            stdin, stdout, stderr = self.ssh.exec_command(f'cp {log_path} {REMOTE_PATH_TO_LOGS}')

            # Wait for the command to complete
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("log copied")
            else:
                print(f"log copy action failed with exit status {exit_status}")
                # You can print the error output if needed:
                print("Error output:")

    def download_log_file_from_robot(self, path_to_save):
        try:
            self.sftp = utils.SFTPclient(self.ssh).sftp
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
#            rm_script = f'rm "{REMOTE_PATH_TO_SCRIPT}"'
            stdin, stdout, stderr = self.ssh.exec_command(rm_log)
            if stderr.read():
                raise Exception(f"Error: {stderr.read().decode('utf-8')}")
            else:
                print(f"File {REMOTE_PATH_TO_LOGS} removed successfully.")        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            
    def capture_container_log_data(self, path_to_save, log_path):
        try:
            self.ssh = utils.SSHinvoker(self.hostname, self.port, self.username, self.password).ssh
            self.copy_log(log_path)
            self.download_log_file_from_robot(path_to_save)
            self.rm_buff_log_and_script_from_robot()            
        finally:
            # Close the SSH connection
            self.ssh.close()