import pika
import time
import os
from slack import WebClient
import json

time.sleep(30)

CANAL_SLACK = '#general'
SLACK_TOKEN = os.environ.get("SLACK_T1")+os.environ.get("SLACK_T2")

#Slack:

slack_web_client = WebClient(SLACK_TOKEN)

#RabbitMQ

def callback(ch, method, properties, body):
	if (body.decode()!="error"):
		print(body)
		m = json.loads(body)
		print(m)
		texto = "*"+m["usuario"]+"*"+" _("+m["fecha"]+")_ : "+m["texto"]
		message = {
			"channel": CANAL_SLACK,
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": texto
					}
				}
			],
		}
		slack_web_client.chat_postMessage(**message)
	else:
		texto="No se han encontrado mensajes para esta fecha"
		message = {
			"channel": CANAL_SLACK,
			"blocks": [
				{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": texto
					}
				}
			],
		}
		slack_web_client.chat_postMessage(**message)


#rabbitmq2
HOST = "rabbitmq"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#exchange nestor
channel.exchange_declare(exchange='nestor', exchange_type="topic", durable=True)


result = channel.queue_declare(queue="publicar_slack", exclusive=True, durable=True)
queue_name = result.method.queue

channel.queue_bind(exchange="nestor", queue=queue_name, routing_key="publish")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()