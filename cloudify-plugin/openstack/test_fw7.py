import openstack_plugin_common as common


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

    print neut_client.list_firewalls()