import pika
import sys
import time
import os

time.sleep(30)

HOST=os.environ['RABBITMQ_HOST']

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#El consumidor utiliza el exchange 'nestor'
channel.exchange_declare(exchange='nestor', exchange_type='fanout')

message1="Hola mundo"
message2="Chao"

channel.basic_publish(exchange="nestor", routing_key='', body=message1)

channel.basic_publish(exchange="nestor", routing_key='', body=message2)

print(' [x] Sent %r' % message1)
print(' [x] Sent %r' % message2)
connection.close()