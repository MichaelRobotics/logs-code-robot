import docker

def initialize_docker_client():
    container_id = None
    try:
        client = docker.from_env()
        containers = client.containers.list(all=True)
        for container in containers:
            ##print(f"Container ID: {container.id}")
            ##print(f"Container Image: {container.attrs['Config']['Image']}")
            if "robot" in container.attrs['Config']['Image']:
                container_id = container.id
                print(f"this is container id: {container_id}")
            else:
                print("no robot image in list containers")
    except docker.errors.APIError as e:
        print(f"Error while communicating with Docker API: {e}")
    finally:
        print("Test Done! Good or bad... ")
    return container_id, 

def execute_command_in_container(container, command):
    client = docker.from_env()
    exec_id = client.containers.get(container).exec_create(command)
    result = client.containers.get(container).exec_start(exec_id)
    return result.decode('utf-8')


def main():
    # This is where your program's code begins
    print("Hello, World!")
    initialize_docker_client()
    execute_command_in_container(initialize_docker_client())

# Check if the script is being run as the main program
if __name__ == "__main__":
    main()