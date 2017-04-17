
import openstack_plugin_common as common

SERVER_STATUS_VERIFY_RESIZE = 'VERIFY_RESIZE'

class OpenstackClients():

    def clients_custom_configuration(self):
        # tests for clients custom configuration, passed via properties/inputs

        inputs_cfg = {
            'username': 'admin',
            'password': 'crowbar',
            'auth_url': 'http://10.30.104.2:5000/v2.0',
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


def _wait_lb_ready(neut_client, lb_id, timeout=120, sleep_interval=15):
    import time
    timeout = time.time() + timeout
    while time.time() < timeout:
        provisioning_status, operating_status = describe_lb_status_from_id(neut_client, lb_id)
        print('Waiting for lb "{0}" to be ready. current status: {1}:{2}'
                        .format(lb_id, provisioning_status, operating_status))
        time.sleep(sleep_interval)
        if provisioning_status == 'ACTIVE' and operating_status == 'ONLINE':
            return
    return


def describe_lb_status_from_id(neut_client, lb_id):
    loadbalancer = neut_client.show_loadbalancer(lb_id)['loadbalancer']
    return loadbalancer.get('provisioning_status'), loadbalancer.get('operating_status')


if __name__ == '__main__':
    client = OpenstackClients()
    nova_client, neut_client, cind_client = client.clients_custom_configuration()

    #print neut_client.show_loadbalancer('a7300be8-08df-433e-8417-316b40eb6795')
    #print neut_client.list_networks()
    #print neut_client.list_loadbalancers()

    # lb_pools = neut_client.list_pools().get('pools')
    # lb_vips = neut_client.list_vips().get('vips')

    # print '1. create loadbalancer'
    # loadbalancer = {
    #     "vip_network_id": "7746bb86-4be8-4df7-86a3-cae0f307ed2a",
    # }
    #
    # loadbalancer_obj = neut_client.create_loadbalancer({'loadbalancer': loadbalancer})['loadbalancer']
    # print loadbalancer_obj
    # _wait_lb_ready(neut_client, loadbalancer_obj['id'])
    #
    # print '2. create listener'
    # listener = {
    #     "loadbalancer_id": loadbalancer_obj['id'],
    #     "protocol": "TCP",
    #     "protocol_port": "101",
    # }
    #
    # listener_obj = neut_client.create_listener({'listener': listener})['listener']
    # print listener_obj
    # _wait_lb_ready(neut_client, loadbalancer_obj['id'])
    #
    # print '3. create pool'
    # pool = {
    #     "listener_id": listener_obj['id'],
    #     "lb_algorithm": "ROUND_ROBIN",
    #     "protocol": "TCP",
    # }
    #
    # pool_obj = neut_client.create_lbaas_pool({'pool': pool})
    # print pool_obj
    # _wait_lb_ready(neut_client, loadbalancer_obj['id'])

    lb_id = '950fc3c0-c871-4b5e-b07c-4efc39d5def3'
    lb_obj = neut_client.show_loadbalancer(lb_id)['loadbalancer']
    print lb_obj

    print lb_obj['pools'][0]['id']
    listener_id = lb_obj['listeners'][0]['id']


    listener_obj = neut_client.show_listener(listener_id)['listener']
    print listener_obj['protocol_port']

    # member= {
    #     "address": "10.30.106.7",
    #     "protocol_port": "80",
    #     'subnet_id': '5c30cad8-6b50-4a65-a39d-f985a982dc24'
    # }
    #
    # member_obj = neut_client.create_lbaas_member('5c7a864f-5b4b-470f-a748-19e0ca0568b9', {'member': member})
    #
    member_objs = neut_client.list_lbaas_members('5c7a864f-5b4b-470f-a748-19e0ca0568b9')['members']
    print member_objs




    # print lb_obj
    # # for listerner in lb_obj.get('listeners'):
    # #     neut_client.delete_listener(listerner['id'])
    # for pool in lb_obj.get('pools'):
    #     pool_obj = neut_client.show_lbaas_pool(pool['id'])['pool']
    #     print pool_obj
    #     if pool_obj['healthmonitor_id']:
    #         neut_client.delete_lbaas_healthmonitor(pool_obj['healthmonitor_id'])
    #     neut_client.delete_lbaas_pool(pool_obj['id'])
    # neut_client.delete_loadbalancer(lb_obj['id'])

    #lb_pools = neut_client.list_lbaas_pools().get('pools')

    #print lb_pools

    # for pool in lb_pools:
    #     print pool
    #
    # for vip in lb_vips:
    #     print vip
    # print network

    # pool = {
    #         "lb_method": "ROUND_ROBIN",
    #         "name": "my-pool",
    #         "protocol": "HTTP",
    #         "subnet_id": "5e3ba00f-107b-410f-adc6-c23a3c938aac",
    #     }
    #
    # neut_client.create_pool({'pool': pool})


    # pool = {
    #         "admin_state_up": True,
    #         "description": "simple pool2",
    #         "lb_algorithm": "ROUND_ROBIN",
    #         "name": "my-pool",
    #         "protocol": "HTTP",
    #         "subnet_id": "5e3ba00f-107b-410f-adc6-c23a3c938aac",
    #         "listener_id": "8d205350-c925-4a35-a9ea-2dcca1bea47d"
    #     }
    # neut_client.create_lbaas_pool({'pool': pool})

    # vip = {
    #     "name": "NewVip",
    #     "pool_id": "105320c3-8416-4997-9c1c-4098b95fdaca",
    #     "protocol": "HTTP",
    #     "protocol_port": "80",
    #     "subnet_id": "0ba2ef27-0054-4b28-a8fa-f215e8079272"
    # }
    #
    # neut_client.create_vip({'vip': vip})

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
