import docker

# Docker container name or ID got from API script
def get_container_id():
    # Initialize the Docker client
    client = docker.from_env()

    try:
        # List all containers or apply filters as needed
        containers = client.containers.list(all=True)

        # Iterate through the list of containers and print their names
        for container in containers:
            print(f"Container ID: {container.id}")
            print(f"Container Name: {container.name}")
            if "robot" in container:
                container_id = container
    except docker.errors.APIError as e:
        print(f"Error while communicating with Docker API: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return container_id
    

# List of file paths inside the container to read
file_paths = [
    "/path/to/file1.txt",
    "/path/to/file2.txt",
    # Add more file paths as needed
]

def execute_command_in_container(container, command):
    client = docker.from_env()
    exec_id = client.containers.get(container).exec_create(command)
    result = client.containers.get(container).exec_start(exec_id)
    return result.decode('utf-8')

def main():
    try:
        for file_path in file_paths:
            command = f"cat {file_path}"
            container_name_or_id = get_container_id()
            file_content = execute_command_in_container(container_name_or_id, command)
            
            print(f"Contents of {file_path}:")
            print(file_content)
            print("=" * 50)
    
    except docker.errors.NotFound:
        print(f"Container '{container_name_or_id}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
