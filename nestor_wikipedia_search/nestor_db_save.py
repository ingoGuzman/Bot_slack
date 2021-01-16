##Este se inicia primero, o falla
import pika
import time
import os
import pymongo
import json

time.sleep(20)

HOST="rabbitmq"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#El consumidor utiliza el exchange 'nestor'
channel.exchange_declare(exchange='nestor', exchange_type='topic', durable=True)

#Se crea una cola temporaria exclusiva para este consumidor
result = channel.queue_declare(queue='intake', exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un exchange
channel.queue_bind(exchange='nestor', queue=queue_name, routing_key="intake")

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["nestor"]
mycol = mydb["persistance"]

print(' [x] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	m = json.loads(body)
	print(m)
	x = mycol.insert_one(m)
	print("Mensaje ingresado a la db")
##	channel.basic_publish(exchange="nestor", routing_key="exit", body="Saved to db (tried)")


channel.basic_consume(
	queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()