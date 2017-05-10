#!/usr/bin/env python
import os
import argparse
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client

def get_keystone_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_PROJECT_NAME']
    return d

def get_nova_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_PROJECT_NAME']
    return d

def get_hostname_of_host(server):
    #return getattr(server, 'OS-EXT-SRV-ATTR:host')
    return getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="the source hypervisor")
    parser.add_argument("--target", help="the target of the migration")
    args = parser.parse_args()
    host_source = args.source
    host_target = args.target
    print("INFO: This will sequentially live migrate all ACTIVE instances from %s to %s" % (host_source, host_target) )

    auth = v3.Password(auth_url='https://compute.datacentred.io:5000/v3/',
                       username=os.environ['OS_USERNAME'],
                       password=os.environ['OS_PASSWORD'],
                       project_name=os.environ['OS_PROJECT_NAME'],
                       user_domain_id='default',
                       project_domain_id='default')
    sess = session.Session(auth=auth)
    nova = client.Client("2.1", session=sess)
    #print(nova.hypervisors.list())
    #print(nova.servers.list())
    servers_to_migrate = nova.hypervisors.search(host_source, servers=True)[0].servers
    for s in servers_to_migrate:
        server = nova.servers.get( s['uuid'] )
        server_id = server.id
        server_name = server.name
        server_status = server.status
        server_host = get_hostname_of_host(server)
        # or faster but potentially more error prone:
        #server_host = host_source
        if server_status == 'ACTIVE':
            print("INFO: Original host: %s" % (server_host)
            print("INFO: Live-migrating server \'%s\' (UUID: %s)" % (server_name, server_id))
            print("INFO: Current host: %s" % get_hostname_of_host(server) )
            print("INFO: Current status: %s" % server.status)
            print("INFO: Progress: %s" % server.progress)
        else:
            print("WARNING: Skipping server \'%s\' (UUID: %s) because it's in the state: %s" % (server_name, server_id, server_status) )

if __name__ == "__main__":
    main()
