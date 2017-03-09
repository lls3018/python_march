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
        self.response = None

        self.queue = 'ip_pool_queue'
        self.routing_key = 'port_abc123'

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
        self.channel.queue_declare(queue=self.queue)

    def callback(self, ch, method, properties, body):
        self.response = body
        time.sleep(15)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def publish_msg(self, message):
        if self._is_closed:
            raise pika.exceptions.ClosedAMQPClientException(
                'Publish failed, AMQP client already closed')

        body = json.dumps(message)
        try:
            self.channel.basic_publish(exchange='',
                                       routing_key=self.routing_key,
                                       body=body)
        except pika.exceptions.ConnectionClosed as e:
            print(
                'Connection closed unexpectedly for thread {0}, '
                'reconnecting. ({1}: {2})'
                .format(threading.current_thread(), type(e).__name__, repr(e)))
            return False

    def get_msg(self):
        if self._is_closed:
            raise pika.exceptions.ClosedAMQPClientException(
                'Get failed, AMQP client already closed')

        try:
            self.channel.basic_consume(self.callback,
                                       queue=self.queue)
            if self._wait_response():
                return True
            else:
                return False
        except pika.exceptions.ConnectionClosed as e:
            print(
                'Connection closed unexpectedly for thread {0}, '
                'reconnecting. ({1}: {2})'
                .format(threading.current_thread(), type(e).__name__, repr(e)))
            return False

    def _wait_response(self, try_times=5, sleep_interval=5):
        for i in range(try_times):
            if self.response is None:
                print('Waiting for response: {}/{}'.format(i+1, try_times))
                time.sleep(sleep_interval)
                self.channel.start_consuming()
            if self.response:
                return True
        else:
            print "Cannot get response after {} times, ".format(try_times)
            return False

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