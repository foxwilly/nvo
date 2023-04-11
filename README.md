# Network Virtualization and Orcherstration
# Automate VM, VN, Docker, and BGP path 
In this lab, you will use what you have learned in previous labs and automate the processes into a single application. 
Required technologies: 
BGP 
Hypervisor/Orchestrator (such as OpenStack) 
Containers 
SDN Controller 
Hardware server 
Service-chain 

### 1.- Automate the creation of multiple virtual networks (VNs) in Openstack

Script to create the network instance in Openstack via python: 
```
def createTopo(conn):
    #conn = createConnection()
    # create a Router r1
    projectId=os.environ.get('OS_PROJECT_ID')
    r1 = conn.network.create_router(name='L9Router', project_id=projectId)
    # create Net + Sub and attach to Router r1
    createNetwork(conn,'T1-network','t1-subnet','10.10.0.0/24',r1)
    createNetwork(conn,'T2-network','t2-subnet','20.20.0.0/24',r1)
    createNetwork(conn,'T1-network','t1-subnet','20.20.0.0/24',r1)
    # attach L9Router to ext network for internet access
    conn.network.add_gateway_to_router(r1, external_network_id='7f23d313-0d7f-4834-9b42-1f79bd11b2d1')
    ext_network = conn.network.find_network(name_or_id='public')
    print('public network ID:', ext_network.id)
    conn.network.update_router(r1,external_gateway_info ={
        'network_id': ext_network.id,
        'enable_snat': True
    })
    print(f'Router r1 created ID: {r1.id} and attached!')
```
This is the graphical view of the networks created

![2](https://user-images.githubusercontent.com/25910108/231103875-2c7b6ee6-d63a-4bd3-81fc-13757ac7e4b7.jpg)

The script create T1 and T2 networks:

![1](https://user-images.githubusercontent.com/25910108/231103876-4f310c1b-4673-49a0-a97e-a3562b2601cc.jpg)

![3](https://user-images.githubusercontent.com/25910108/231103873-0c45f811-5538-4b43-9643-a3501aee9a71.jpg)

### 2.- Automate the creation of Virtual Machines (VMs) in Openstack


This section of the code is to create the instaces at this point the network topology needs to be ready
The script only considers the name, network, image, and flavor as configuration attributes, other attributes like port security, and security group are set by default.

```
if __name__=='__main__':
    conn = createConnection()
    # this part create the networks, router and connections
    createTopo(conn)
    # this create the two intancess and attached to the corresponding networks
    # the parameter are name, networ, image, flavor
    createInstance(conn,'myVM1','T1-network','cirros-0.5.2-x86_64-disk','m1.small')
    createInstance(conn,'myVM2','T1-network','ubuntu22.4','ds512M')
    createInstance(conn,'myVM3','T2-network','cirros-0.5.2-x86_64-disk','m1.small')
```
This will create the following configuration:

Instances myVM1, myVM2 and myVM3:

![4](https://user-images.githubusercontent.com/25910108/231103870-0c45235b-73b0-44e4-8ace-bdb3239912d3.jpg)

Graphical representation of the topology:





![5](https://user-images.githubusercontent.com/25910108/231103867-55de8615-ad4d-4a6d-a79f-e61576c1e7e1.jpg)



![11](https://user-images.githubusercontent.com/25910108/231103880-0ab7247b-c2a6-45da-b7b0-e165f749c34c.jpg)
![10](https://user-images.githubusercontent.com/25910108/231103882-b7f14274-185c-4577-8fee-966cb7cbf0e4.jpg)



### 3.- Automate spinning up and configuring an SDN controller as another Docker container. 
Inside of one VM with we will automate the creation of SDN Ryu and and FRR router in containers

In VM2 we have Ubuntu 22.4 and after installing the Docker engine, I will create the Docker files and the image via code

```
def createContainer(name,dockerfile):
    client = docker.from_env()
    image, build_logs = client.images.build(path=dockerfile)
    container = client.containers.run(image=image.id,name=name, detach=True)
    print(f"Container ID: {container.id}")

if __name__=='__main__':
    createContainer("c-ryu","/home/willy/ryu-container/")
    createContainer("c-frr","/home/willy/ffr-container/")
```
this is the output of the code:

![7](https://user-images.githubusercontent.com/25910108/231103860-8a56cf3a-2415-4b15-ba14-65796d37d3d7.jpg)

This process creates two images and runs the containers as follows:

![9](https://user-images.githubusercontent.com/25910108/231103886-2aca6fc9-0417-424e-9119-6b995a13753c.jpg)

The Dockerfile for each container already have the configuration for BGP so once the container is up, they start talking BGP:

this the configuration for BGP in each container:

RYU:

![6](https://user-images.githubusercontent.com/25910108/231103865-f2518ff1-a009-489c-ba09-3d4445e4c99a.jpg)

FFR:

![8](https://user-images.githubusercontent.com/25910108/231103853-63300138-b4d9-4a3d-a710-015ebebe3c9e.jpg)

enclosed you can find the python code for this project.

Thanks 
Willy Fernandez
