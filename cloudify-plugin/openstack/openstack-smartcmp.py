#!/usr/bin/env python
# encoding: utf-8
__author__ = 'Wayne'
__date__ = '2017/3/14'


import openstack_plugin_common as common
from instance import create_vm

class OpenstackClients():

    def clients_custom_configuration(self):
        # tests for clients custom configuration, passed via properties/inputs

        inputs_cfg = {
            'username': 'admin',
            'password': 'crowbar',
            'auth_url': 'http://192.168.126.2:5000/v2.0',
            'region': 'RegionOne',
            'tenant_name': 'admin'
        }

        nova_client, neut_client = \
            self._create_clients(inputs_cfg)
        return nova_client, neut_client

    def _create_clients(self, inputs_cfg):

        orig_nova_client = common.NovaClientWithSugar
        orig_neut_client = common.NeutronClientWithSugar

        try:
            common.NovaClient().get(config=inputs_cfg)
            common.NeutronClient().get(config=inputs_cfg)
        except:
            print "except"
        finally:
            common.NovaClientWithSugar = orig_nova_client
            common.NeutronClientWithSugar = orig_neut_client

            return (common.NovaClient().get(config=inputs_cfg), common.NeutronClient().get(config=inputs_cfg))


def create_floatingip(neutron_client):

    floatingip = {
        'floating_network_name': 'floating'  # floating ip 所在网络名
    }
    if 'floating_network_name' in floatingip:
        floatingip['floating_network_id'] = neutron_client.cosmo_get_named(
            'network', floatingip['floating_network_name'])['id']
        del floatingip['floating_network_name']
    else:
        raise Exception('Missing floating network id or name')

    fip = neutron_client.create_floatingip(
        {'floatingip': floatingip})['floatingip']

    print('Floating IP creation response: {0}'.format(fip))
    return fip['floating_ip_address']


def _wait_for_server_to_be_targetstatus(nova_client,
                                        server,
                                        targetstatus,
                                        timeout=120,
                                        sleep_interval=5):
    import time
    timeout = time.time() + timeout
    while time.time() < timeout:
        server = nova_client.servers.get(server)
        print('Waiting for server "{0}" to be {1}. current status: {2}'
                         .format(server.id, targetstatus, server.status))
        time.sleep(sleep_interval)
        if server.status in targetstatus:
            return

    raise RuntimeError('Server status {} is not {}. waited for {} seconds'
                       .format(server.id, targetstatus, timeout))


if __name__ == '__main__':
    client = OpenstackClients()
    nova_client, neut_client = client.clients_custom_configuration()
    server_id = create_vm(nova_client, neut_client)
    print server_id
    server = nova_client.servers.get(server_id)
    _wait_for_server_to_be_targetstatus(nova_client, server, 'ACTIVE')

    floating_ip_address = create_floatingip(neut_client)
    print floating_ip_address

    server = nova_client.servers.get(server_id)
    server.add_floating_ip(floating_ip_address)