
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


if __name__ == '__main__':
    client = OpenstackClients()
    nova_client, neut_client, cind_client = client.clients_custom_configuration()

    # pool = {
    #         "lb_method": "ROUND_ROBIN",
    #         "name": "my-pool",
    #         "protocol": "HTTP",
    #         "subnet_id": "5e3ba00f-107b-410f-adc6-c23a3c938aac",
    #     }
    #
    # pool_obj = neut_client.create_pool({'pool': pool})['pool']
    # print pool_obj
    #
    # vip = {
    #     "name": "NewVip",
    #     "pool_id": pool_obj['id'],
    #     "protocol": "HTTP",
    #     "protocol_port": "80",
    #     "subnet_id": "5e3ba00f-107b-410f-adc6-c23a3c938aac"
    # }
    #
    # vip_obj = neut_client.create_vip({'vip': vip})['vip']
    # print vip_obj

    # lb_pools = neut_client.list_pools().get('pools')
    # lb_vips = neut_client.list_vips().get('vips')
    #
    lb_pool_id = '867d7829-d505-4654-aa54-17b43c01c00e'
    lb_pool_obj = neut_client.show_pool(lb_pool_id)['pool']
    print lb_pool_obj

    print neut_client.show_vip(lb_pool_obj['vip_id'])
    # if lb_pool_obj['vip_id']:
    #     print neut_client.show_vip(lb_pool_obj['vip_id'])
    #
    # for member in lb_pool_obj['members']:
    #     print neut_client.show_member(member)['member']
    #
    # neut_client.delete_member('3d97d16e-7979-4219-8a2c-e5922dae7461')

    #neut_client.delete_pool(lb_pool_obj['id'])

    # network = neut_client.show_network(net_id).get('network')
    # sub_nets = network.get('subnets')
    # sub_net = neut_client.show_subnet(sub_nets[0]).get('subnet')
    # sub_net_id = sub_net.get('id')
    # print sub_net_id
    # for port in neut_client.list_ports(net_id)['ports']:
    #     for fixed_ip in port.get('fixed_ips', []):
    #        if fixed_ip.get('subnet_id') == sub_net_id:
    #            print fixed_ip
