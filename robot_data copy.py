import paramiko
import logging

LOCAL_PATH_TO_SCRIPT = '/home/vb/Bsst-logs-code/container_script.py'
REMOTE_PATH_TO_SCRIPT = '/tmp/Bsst-logs-code/container_script.py'
REMOTE_PATH_TO_LOGS = '/tmp/Bsst-logs-code/logs'
LOCAL_PATH_TO_LOGS = '/tmp/Bsst-logs-code/logs'

class RobotData:
    """
        Klasa tworząca obiekt zawierający pożądany rodzaj loga
    """
    def __init__(self, hostname: str, port: int, username: str, password: str, local_logs_location: str):
        """
            Definiowanie danych do logowania
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.local_logs_location = local_logs_location
        self.ssh = None
        self.sftp = None

    def check_passed_local_paths_logs():
        """
            Check if paths to file is already taken by other file
        """
        pass

    def invoke_ssh_connection(self):
        with paramiko.SSHClient() as ssh:
            self.ssh = ssh
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                self.ssh.connect(self.hostname, port=self.port, username=self.username, password=self.password, timeout=180)
            except Exception as exc:
                ### loginfo(f'Failed to connect when restarting services, exc: {exc}')
                print(exc)
                ###raise TestsAutomationException('Failed to establish connection to stack PC')     
    
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
            stdin, stdout, stderr = self.ssh.exec_command(f'python3 {REMOTE_PATH_TO_SCRIPT} --log_path {REMOTE_PATH_TO_LOGS}')

            # Wait for the command to complete
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print("Script execution successful")
            else:
                print(f"Script execution failed with exit status {exit_status}")
                # You can print the error output if needed:
                print("Error output:")
                print(stderr.read().decode())

        except Exception as e:
            print(f"Error executing script: {str(e)}")            

    def Download_log_file_from_robot(self):
        try:
            self.create_sftp_client(self)
            # Download the remote file to the local machine
            self.sftp.get(REMOTE_PATH_TO_LOGS, LOCAL_PATH_TO_LOGS)
            print(f"File '{REMOTE_PATH_TO_LOGS}' downloaded to '{LOCAL_PATH_TO_LOGS}'")
        except FileNotFoundError:
            print(f"Remote file '{REMOTE_PATH_TO_LOGS}' not found")
        except Exception as e:
            print("An error occurred while downloading the file:", str(e))
        finally:
            # Close the SFTP session and the SSH connection
            self.sftp.close()

    def Capture_container_log_data(self):
        try:
            self.check_passed_local_paths_logs()
            self.invoke_ssh_connection()
            self.send_script_to_container()
            self.execute_script_inside_container()
            self.Download_log_file_from_robot()            
        finally:
            # Close the SSH connection
            self.ssh.close()
            
                        # TESTY ROBOT_DATA.py
            ##### Dodać 1) Pobieranie pliku 2) dlaczego nie przesyła się obiekt ssh \ 
            # 3) dodać exception, a jeżeli wszystko ok i plik istnieje to zwrócić ścieżkę do pliku \
            # 4) jak obsługiwać ścieżki do plików, kto jak wysyła 5) dodać logowanie
            # 6) sprawdzić poprawność u siebie 7) sprawdzić poprawność na systemie vb
            