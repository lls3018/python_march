
import openstack_plugin_common as common

SERVER_STATUS_VERIFY_RESIZE = 'VERIFY_RESIZE'

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



        nova_client, neut_client, cind_client = \
            self._create_clients(inputs_cfg)
        return nova_client, neut_client, cind_client

    def _create_clients(self, inputs_cfg):

        orig_nova_client = common.NovaClientWithSugar
        orig_neut_client = common.NeutronClientWithSugar
        orig_cind_client = common.CinderClientWithSugar
        #orig_keys_client = common.keystone_client.Client

        try:
            common.NovaClient().get(config=inputs_cfg)
            common.NeutronClient().get(config=inputs_cfg)
            common.CinderClient().get(config=inputs_cfg)
            #common.KeystoneClient().get(config=inputs_cfg)
        except:
            print "except"
        finally:
            common.NovaClientWithSugar = orig_nova_client
            common.NeutronClientWithSugar = orig_neut_client
            common.CinderClientWithSugar = orig_cind_client
            #common.keystone_client.Client = orig_keys_client

            return (common.NovaClient().get(config=inputs_cfg), common.NeutronClient().get(config=inputs_cfg), common.CinderClient().get(config=inputs_cfg) )


def _get_server_floating_ip(neutron_client, server_id):
    floating_ips = neutron_client.list_floatingips()

    floating_ips = floating_ips.get('floatingips')
    if not floating_ips:
        return None
    for floating_ip in floating_ips:
        port_id = floating_ip.get('port_id')
        if not port_id:
            # this floating ip is not attached to any port
            continue

        port = neutron_client.show_port(port_id)['port']
        device_id = port.get('device_id')
        if not device_id:
            # this port is not attached to any server
            continue

        if server_id == device_id:
            return floating_ip
    return None


def _get_server_floating_ip1(nova_client, server_id):
    floating_ips = nova_client.floating_ips.list()


    if not floating_ips:
        return None
    for floating_ip in floating_ips:
        instance_id = floating_ip.instance_id
        if not instance_id:
            # this floating ip is not attached to any port
            continue

        if server_id == instance_id:
            return floating_ip
    return None


if __name__ == '__main__':
    client = OpenstackClients()
    nova_client, neut_client, cind_client = client.clients_custom_configuration()
    #print nova_client, neut_client, cind_client, keys_client

    #print dir(nova_client)
    #print keys_client.tenant_id
    #print "-----"
    # common.get_resource_by_name_or_id('default', 'security_group', neut_client)

    import operator


    #floating_ip = _get_server_floating_ip1(nova_client, 'e5ec49a1-1d02-4da6-bd98-18d8d6e7611a')
    #print floating_ip.ip
    #
    server_id = 'bca10730-6d1f-4407-ad29-12d7ba8df704'
    server = nova_client.servers.get(server_id)

    address_list = []
    for network, addresses in server.addresses.items():
        for address in addresses:
            if address.get('OS-EXT-IPS:type') == 'fixed':
                address_list.append(address['addr'])

    print address_list


    # for address in addresses:
    #     if address.get('OS-EXT-IPS:type') == 'fixed':
    #         print address['addr']


    #print _get_server_floating_ip(neut_client, server_id)


    # net_id = '22da7c10-2890-42c3-8a54-4b97a87ec1ee'
    # network = neut_client.show_network(net_id)
    #
    # print network
    #
    # network = neut_client.show_network(net_id).get('network')
    # sub_nets = network.get('subnets')
    # sub_net = neut_client.show_subnet(sub_nets[0]).get('subnet')
    # sub_net_id = sub_net.get('id')
    # print sub_net_id
    # for port in neut_client.list_ports(net_id)['ports']:
    #     for fixed_ip in port.get('fixed_ips', []):
    #        if fixed_ip.get('subnet_id') == sub_net_id:
    #            print fixed_ip


    # router_id = '2ae9ba58-43ed-4120-b4d4-0bcc399dc532'
    # for port in neut_client.list_ports(device_id=router_id)['ports']:
    #     for fixed_ip in port.get('fixed_ips', []):
    #         print fixed_ip
            # if fixed_ip.get('subnet_id') == subnet_id:
            #     return

    #if server.status == SERVER_STATUS_VERIFY_RESIZE:
    #    nova_client.servers.confirm_resize(server)
    #print server.status
    # server_task_state = getattr(server, 'OS-EXT-STS:task_state')
    # print server_task_state
    #
    #
    # floating_ip = _get_server_floating_ip(neut_client, '29499648-6aae-440a-a586-7e56fea4db33')
    # print floating_ip
    #print floating_ip.get('floating_ip_address', None)
    #search_param = {'name': 'default', 'tenant_id': keys_client.tenant_id}
    #search_param = {'name': 'default'}
    #resource = nova_client.cosmo_get_if_exists('security_group', **search_param)

"""
    from keystoneauth1.identity import v2
    from keystoneauth1 import session
    from keystoneclient.v2_0 import client

    username = 'admin'
    password = 'password'
    tenant_name = 'demo'
    auth_url = 'http://192.168.84.3:5000/v2.0'
    auth = v2.Password(username=username, password=password,
                       tenant_name=tenant_name, auth_url=auth_url)
    sess = session.Session(auth=auth)
    keystone = client.Client(session=sess)
    print keystone.tenants.list()
"""