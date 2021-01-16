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
result = channel.queue_declare(queue='retrieve', exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un exchange
channel.queue_bind(exchange='nestor', queue=queue_name, routing_key="retrieve")

myclient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myclient["nestor"]
mycol = mydb["persistance"]

print(' [x] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
	indexN = body[-10:]
	index = indexN.decode()
	print(index)
	x = mycol.find({"fechaB":index},{ "_id": 0, "usuario": 1, "texto": 1 , "bloques": 1, "fecha": 1, "fechaB":1}).sort("_id",1)
	l = list(x)
	if (len(l)):
		for j in range(len(l)):
			i = l[j]
			print(i["usuario"])
			print(i["fecha"])
			print(i["texto"])
			m = json.dumps(i)
			channel.basic_publish(exchange="nestor", routing_key="publish", body=m)
			print("Mensaje recuperado y enviado")
	else:
		m="error"
		channel.basic_publish(exchange="nestor", routing_key="publish", body=m)
##	channel.basic_publish(exchange="nestor", routing_key="exit", body="Saved to db (tried)")


channel.basic_consume(
	queue=queue_name, on_message_callback=callback)

channel.start_consuming()