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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="the source hypervisor")
    parser.add_argument("--target", help="the target of the migration")
    args = parser.parse_args()
    host_source = args.source
    host_target = args.target
    print("Will live migrate all instances from %s to %s" % (host_source, host_target) )

    auth = v3.Password(auth_url='https://compute.datacentred.io:5000/v3/',
                       username=os.environ['OS_USERNAME'],
                       password=os.environ['OS_PASSWORD'],
                       project_name=os.environ['OS_PROJECT_NAME'],
                       user_domain_id='default',
                       project_domain_id='default')
    sess = session.Session(auth=auth)
    nova = client.Client("2.1", session=sess)
    print nova.hypervisors.list()
    print nova.servers.list()
    print nova.hosts.list()

if __name__ == "__main__":
    main()
