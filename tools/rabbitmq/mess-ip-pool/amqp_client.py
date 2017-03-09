import simplejson as json
import threading
import time

import pika
import pika.exceptions
import broker_config
import uuid


class AMQPClient(object):

    def __init__(self,
                 amqp_user,
                 amqp_pass,
                 amqp_host,
                 amqp_port):
        self.connection = None
        self.channel = None
        self._is_closed = False
        self.corr_id = str(uuid.uuid4())
        self.response = None

        self.publish_queue = 'zeng'
        self.consume_queue = 'wenqi'

        credentials = pika.credentials.PlainCredentials(
            username=amqp_user,
            password=amqp_pass)
        self._connection_parameters = pika.ConnectionParameters(
                host=amqp_host,
                port=amqp_port,
                credentials=credentials,
                ssl=False,
                ssl_options={})

        self.connection = pika.BlockingConnection(self._connection_parameters)
        self.channel = self.connection.channel()
        self.channel.confirm_delivery()
        self.channel.queue_declare(queue=self.publish_queue, durable=True)
        self.channel.queue_declare(queue=self.consume_queue, durable=True)
        self.channel.basic_consume(self.on_response,
                                   queue=self.consume_queue,
                                   no_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message):
        if self._is_closed:
            raise pika.exceptions.ClosedAMQPClientException(
                'Publish failed, AMQP client already closed')

        body = json.dumps(message)
        try:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.publish_queue,
                                       properties=pika.BasicProperties(
                                           reply_to=self.consume_queue,
                                           correlation_id=self.corr_id,
                                       ),
                                       body=body)
            print "publis body is: {}".format(body)
        except pika.exceptions.ConnectionClosed as e:
            print(
                'Connection closed unexpectedly for thread {0}, '
                'reconnecting. ({1}: {2})'
                .format(threading.current_thread(), type(e).__name__, repr(e)))
            return False

        time.sleep(15)
        print self.response

    def close(self):
        if self._is_closed:
            return
        self._is_closed = True
        thread = threading.current_thread()
        if self.channel:
            print('Closing amqp channel of thread {0}'.format(thread))
            try:
                self.channel.close()
            except Exception as e:
                # channel might be already closed, log and continue
                print('Failed to close amqp channel of thread {0}, '
                      'reported error: {1}'.format(thread, repr(e)))

        if self.connection:
            print('Closing amqp connection of thread {0}'.format(thread))
            try:
                self.connection.close()
            except Exception as e:
                # connection might be already closed, log and continue
                print('Failed to close amqp connection of thread {0}, '
                      'reported error: {1}'.format(thread, repr(e)))


def create_client(amqp_host=broker_config.broker_hostname,
                  amqp_user=broker_config.broker_username,
                  amqp_pass=broker_config.broker_password,
                  amqp_port=broker_config.broker_port):
    thread = threading.current_thread()
    try:
        print(
            'Creating a new AMQP client for thread {0} '
            '[hostname={1}, username={2}, ssl_enabled={3}]'
            .format(thread, amqp_host, amqp_user, amqp_port))
        client = AMQPClient(amqp_host=amqp_host,
                            amqp_user=amqp_user,
                            amqp_pass=amqp_pass,
                            amqp_port=amqp_port)
        print('AMQP client created for thread {0}'.format(thread))
    except Exception as e:
        print(
            'Failed to create AMQP client for thread: {0} ({1}: {2})'
            .format(thread, type(e).__name__, e))
        raise
    return client