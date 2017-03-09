
import json
import os
import ssl

import constants


config = {}
conf_file_path = './broker_config.json'
if os.path.isfile(conf_file_path):
    with open(conf_file_path) as conf_handle:
        conf_file = conf_handle.read()
        config = json.loads(conf_file)
else:
    config = {}

# Provided as variables for retrieval by amqp_client and logger as required
broker_ssl_enabled = config.get('broker_ssl_enabled', False)
broker_cert_path = config.get('broker_cert_path', '')
broker_username = config.get('broker_username', 'guest')
broker_password = config.get('broker_password', 'guest')
broker_hostname = config.get('broker_hostname', 'localhost')

if broker_ssl_enabled:
    BROKER_USE_SSL = {
        'ca_certs': broker_cert_path,
        'cert_reqs': ssl.CERT_REQUIRED,
    }
    broker_port = constants.BROKER_PORT_SSL
else:
    broker_port = constants.BROKER_PORT_NO_SSL

print config