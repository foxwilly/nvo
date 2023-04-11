import docker

def createContainer(name,dockerfile):

    # Call Docker client
    client = docker.from_env()

    # Build the Docker image from the Dockerfile
    image, build_logs = client.images.build(path=dockerfile)

    # Run the Docker container
    container = client.containers.run(image=image.id,name=name, detach=True)

    # Print the container ID
    print(f"Container ID: {container.id}")

if __name__=='__main__':
    createContainer("c-ryu","/home/willy/ryu-container/")
    createContainer("c-frr","/home/willy/ffr-container/")
~                                                          
