#!/usr/bin/env python
import argparse
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client
import time
import credentials

def get_hostname_of_host(server):
    #return getattr(server, 'OS-EXT-SRV-ATTR:host')
    return getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="filter to a specific host; use 'all' to show instances across all hypervisors (NOT YET IMPLEMENTED)")
    args = parser.parse_args()
    host = str(args.host)

    creds = credentials.Credentials()

    auth = v3.Password(auth_url=creds.auth_url,
                       username=creds.username,
                       password=creds.password,
                       project_name=creds.project_name,
                       user_domain_id=creds.user_domain_id,
                       project_domain_id=creds.project_domain_id)
    sess = session.Session(auth=auth)
    nova = client.Client("2.1", session=sess)
    #print(nova.servers.list())
    for server in nova.servers.list(search_opts={'config_drive': True, 'all_tenants': 1}):
        host_current = get_hostname_of_host(server)
        print ("%s,%s,%s,%s" % (server.id, server.name, server.status, get_hostname_of_host(server)) )

if __name__ == "__main__":
    main()
