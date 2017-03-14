import pika
import broker_config
import simplejson as json


def on_request(ch, method, props, body):
    ip_info = {'return_code': True, 'ip_address': '192.168.176.231', 'cidr': '192.168.176.0/21',
               'gateway': '192.168.176.1', 'dns_servers': '114.114.114.114'}
    response = json.dumps(ip_info)
    print props
    ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=response
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print '---------------------'

if __name__ == '__main__':

    credentials = pika.credentials.PlainCredentials(
        username=broker_config.broker_username,
        password=broker_config.broker_password)
    connection_parameters = pika.ConnectionParameters(
        host=broker_config.broker_hostname,
        port=broker_config.broker_port,
        credentials=credentials,
        ssl=False,
        ssl_options={})

    queue = 'ip_pool_queue'

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_request, queue=queue)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
