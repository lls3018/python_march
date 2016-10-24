#!/usr/bin/env python
# William Lam
# www.virtuallyghetto.com

"""
vSphere Python SDK program for listing Datastores in Datastore Cluster
"""
import argparse
import atexit

from pyVmomi import vim
from pyVmomi import vmodl
from pyVim import connect

from ServerClient import VsphereClient


def get_args():
    """
   Supports the command-line arguments listed below.
   """
    parser = argparse.ArgumentParser(
        description='Process args for retrieving all the Virtual Machines')

    parser.add_argument('-s', '--host',
                        required=True, action='store',
                        help='Remote host to connect to')

    parser.add_argument('-o', '--port',
                        type=int, default=443,
                        action='store', help='Port to connect on')

    parser.add_argument('-u', '--user', required=True,
                        action='store',
                        help='User name to use when connecting to host')

    parser.add_argument('-p', '--password',
                        required=True, action='store',
                        help='Password to use when connecting to host')

    parser.add_argument('-d', '--dscluster', required=True, action='store',
                        help='Name of vSphere Datastore Cluster')

    args = parser.parse_args()
    return args


def locate_vm(selected_cluster, selected_datastore):
    print("Entering place VM procedure.")

    hosts = []
    for host in selected_datastore.host:
        if host.key in selected_cluster.host:
            hosts.append(host.key)

    hosts = selected_cluster.host

    print("The available hosts are{0}.".format(hosts))

    selected_host = hosts[0]
    selected_host_memory = 0
    selected_host_memory_used = 0
    for host in hosts:
        if host.overallStatus == vim.ManagedEntity.Status.red:
            print(
                ' The host {name}  Status is red.'.format(name=host.name)
            )

        host_memory = host.hardware.memorySize
        host_memory_used = 0
        for vm in host.vm:
            if not vm.summary.config.template:
                if vm.summary.config.memorySizeMB is None:
                    continue
                host_memory_used += vm.summary.config.memorySizeMB

        host_memory_delta = host_memory - host_memory_used
        selected_host_memory_delta = selected_host_memory - selected_host_memory_used
        print(
            "The candidate host {candidate_name} with available memory {candidate_memory}".format(
                candidate_name=host.name,
                candidate_memory=host_memory_delta,
            )
        )

        if host_memory_delta > selected_host_memory_delta:
            selected_host = host
            selected_host_memory = host_memory
            selected_host_memory_used = host_memory_used

    print(
        'Deploying to host: {name}'.format(name=selected_host.name)
    )
    return selected_host


def main():
    """
    Simple command-line program for listing the virtual machines on a system.
    """
    client = VsphereClient()
    client.connect()

    datastore = {'name': u'datastore1', 'id': 'datastore-1572'}

    selected_datastore = client._get_obj_by_name([vim.Datastore], datastore['name'])
    selected_cluster = client._get_obj_by_id([vim.ComputeResource], 'domain-c7')

    host = locate_vm(selected_cluster, selected_datastore)
    print host.name, host


# Start program
if __name__ == "__main__":
    main()
