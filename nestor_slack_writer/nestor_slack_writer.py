import pika
import time
import os
from slack import WebClient

time.sleep(30)

CANAL_SLACK = '#general'
SLACK_TOKEN = os.environ.get("SLACK_T1")+os.environ.get("SLACK_T2")

#Slack:

slack_web_client = WebClient(SLACK_TOKEN)

#RabbitMQ

def callback(ch, method, properties, body):
	text = body.decode().replace("\n","").replace("\r","")
	message = {
		"channel": CANAL_SLACK,
		"blocks": [
			{"type": "section", "text": {"type": "mrkdwn", "text": text}},
		],
	}
	slack_web_client.chat_postMessage(**message)


#rabbitmq2
HOST = os.environ["RABBITMQ_HOST"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

#exchange nestor
channel.exchange_declare(exchange='nestor', exchange_type="topic", durable=True)


result = channel.queue_declare(queue="publicar_slack", exclusive=True, durable=True)
queue_name = result.method.queue

channel.queue_bind(exchange="nestor", queue=queue_name, routing_key="publicar_slack")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()