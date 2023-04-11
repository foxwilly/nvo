#! /usr/bin/env python3

import os
from openstack import connection

# to create a connection to openstack
def createConnection():
    try:
        connect = connection.Connection(
            auth_url=os.environ.get('OS_AUTH_URL'),
            project_name=os.environ.get('OS_PROJECT_NAME'),
            username=os.environ.get('OS_USERNAME'),
            password='secret',
            user_domain_name='Default',
            project_domain_name='Default')
        print("connection created")
        return connect
    except:
        print('Error creating the connection to {0} project {1} user {2}'.format(os.environ.get('OS_AUTH_URL'),os.environ.get('OS_PROJECT_NAME'),os.environ.get('OS_USERNAME')))



# create a network and subnet associated to it
def createNetwork(conn, net_name, sub_name, net_ip, r1):
    # creates a netw
    network = conn.create_network(name=net_name)
    # subnet for the netw created
    subnet = conn.network.create_subnet(
     name=sub_name,
     network_id=network.id,
     cidr=net_ip,
     ip_version=4)

    # add subnet to Router
    conn.network.add_interface_to_router(r1, subnet_id=subnet.id)
    print(f'Network {net_name} created ID: {network.id}')
    print(f'Subnet {sub_name} created ID: {subnet.id}')



def createInstance(conn, inst_name, net,img,vflavor):
    # find the ID of the flavor to use
    flavor = conn.compute.find_flavor(vflavor)

    # find the ID of the image to use
    image = conn.compute.find_image(img)

    # create the instance
    network = conn.network.find_network(name_or_id=net)
    instance = conn.compute.create_server(
        name=inst_name,
        flavor_id=flavor.id,
        image_id=image.id,
        networks=[{'uuid': network.id}])

    # wait for the instance to be active
    conn.compute.wait_for_server(instance)

    # print the instance details
    print('Instance ID:', instance.id)
    print('Network ID:', network.id)
    print('Instance IP address:', instance.access_ipv4)


# creates the network topology
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
    #createInstance(conn)



if __name__=='__main__':
    conn = createConnection()
    # this part create the networks, router and connections
    createTopo(conn)
    # this create the two intancess and attached to the corresponding networks
    # the parameter are name, networ, image, flavor
    createInstance(conn,'myVM1','T1-network','cirros-0.5.2-x86_64-disk','m1.small')
    createInstance(conn,'myVM2','T1-network','ubuntu22.4','ds512M')
    createInstance(conn,'myVM3','T2-network','cirros-0.5.2-x86_64-disk','m1.small')
