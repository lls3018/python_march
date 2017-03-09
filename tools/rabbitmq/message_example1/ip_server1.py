import pika
import broker_config
import simplejson as json
import time


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ip_info = {'ip_address': '192.168.176.225', 'cidr': '192.168.176.0/21', 'gateway': '192.168.176.1'}
    response = json.dumps(ip_info)
    print response
    print properties.correlation_id
    print body

    ch.basic_publish(exchange='',
                     routing_key='hello1',
                     properties=pika.BasicProperties(
                              reply_to='hello1',
                              correlation_id=properties.correlation_id,
                     ),
                     body=response)

    ch.basic_ack(delivery_tag=method.delivery_tag)


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

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()
    channel.queue_declare(queue='hello1')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue='hello1')
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
