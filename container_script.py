import docker
import os
import argparse

LOG_CONTAINER_BUFF_PATH = "/home/vb/robotlog.txt"


class ContainerScript():

    def __init__(self):
        """
            Definiowanie atrybutów
        """
        self.client = None
        self.container_id = None

    def initialize_docker_client(self):
        try:
            self.client = docker.from_env()
        except docker.errors.APIError as e:
            print(f"Error while communicating with Docker API: {e}")
            self.client = None
    
    def find_Robot_container_id(self):
        container_id = None

        try:
            containers = self.client.containers.list(all=True)

            for container in containers:
                if "robot" in container.attrs['Config']['Image']:
                    container_id = container.id
                    print(f"Found a robot container with ID: {container_id}")
                    self.container_id = container_id

            if container_id is None:
                print("No robot containers found in the list of containers.")

        except docker.errors.DockerException as e:
            print(f"An error occurred while working with Docker containers: {e}")
    

    def move_log_file_inside_container(self):
        try:
            command = f"cp {container_path} {LOG_CONTAINER_BUFF_PATH}"
            exec_instance = self.client.api.exec_create(container=self.container_id, cmd=command)
            # The result will contain the exec instance ID
            exec_id = exec_instance['Id']
            # You can now start the exec instance to run the command
            self.client.api.exec_start(exec_id)
        except docker.errors.APIError as e:
            # Handle Docker API-related errors
            print(f"Docker API Error: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")

    def move_file_from_container(self):

        try:
            # Construct the docker cp command
            print(f'docker cp {self.container_id}:{LOG_CONTAINER_BUFF_PATH} {remote_path}')
            docker_cp_command = f'docker cp {self.container_id}:{LOG_CONTAINER_BUFF_PATH} {remote_path}'

            # Execute the command using os.system
            os.system(docker_cp_command)

            print(f"File from container copied to {remote_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def remove_file_from_container(self):
        try:
            # Use the `exec_run` method to execute the `rm` command inside the container
            command = f'rm {LOG_CONTAINER_BUFF_PATH}'
            exec_instance = self.client.api.exec_create(container=self.container_id, cmd=command)
            # The result will contain the exec instance ID
            exec_id = exec_instance['Id']
            # run the command
            self.client.api.exec_start(exec_id)
        except docker.errors.APIError as e:
            # Handle Docker API-related errors
            print(f"Docker API Error: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"An error occurred: {e}")

    def main(self):
        try:
            self.initialize_docker_client()
            self.find_Robot_container_id()
            self.move_log_file_inside_container()
            self.move_file_from_container()
            self.remove_file_from_container()

        except Exception as e:

            print(f"An error occurred at main: {e}")


parser = argparse.ArgumentParser(description="Copy a file from a Docker container to a local directory.")
parser.add_argument("remote_log_path", help="remote path to copy the file to")
parser.add_argument("container_log_path", help="path to log on container to copy from")
args = parser.parse_args()

# Assign the parsed argument to a variable named "remote_log_path"
remote_path = args.remote_log_path
# Assign the parsed argument to a variable named "container_log_path"
container_path = args.container_log_path
obj = ContainerScript()
obj.main()
