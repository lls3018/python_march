import amqp_client

dic1 = {'instance_id': '2', 'node_id': 'Server', 'deployment_id': 'cdea123445'}
fibonacci_rpc = amqp_client.create_client(amqp_id=dic1.get('instance_id'))
print dic1
print 'waiting...'
response = fibonacci_rpc.call(dic1)


print response
print type(response)