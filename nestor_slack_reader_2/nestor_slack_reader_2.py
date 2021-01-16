##Este lee de slack, pasa a la que guarda en db
import pika
import sys
import time
import os
import logging
import json
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from datetime import datetime


time.sleep(30)

##Rabbit mq

HOST="rabbitmq"

connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()

#exchange declaration
channel.exchange_declare(exchange="nestor", exchange_type="topic", durable=True)

##Flask
app = Flask(__name__)
##Event adapter too
SLACK_SECRET = os.environ.get("SLACK_S1")+os.environ.get("SLACK_S2")
SLACK_TOKEN = os.environ.get("SLACK_T1")+os.environ.get("SLACK_T2")

slack_events_adapter = SlackEventAdapter(SLACK_SECRET, "/slack/events", app)
print(SLACK_SECRET)

##WebClient
slack_web_client = WebClient(SLACK_TOKEN)
print(SLACK_TOKEN)

#flask app route example
@app.route("/")
def hello():
	return "Hello there!"

@slack_events_adapter.on("message")
def message(payload):
	"""Parse the message event
	"""
	# Get event data from payload
	event = payload.get("event", {})
	if (event.get("user") != "U01C4EKLL0N"):
		#Get the text
		text=event.get("text")
		if text.startswith("!retrieve"):
			print ("retrievepo")
			channel.basic_publish(exchange="nestor", routing_key="retrieve", body=text)
		else:
			user_id=str(event.get("user"))
			nameFetch = slack_web_client.users_info(user=user_id)
			user = nameFetch.get("user")
			name = user.get("name")
			sl_channel=event.get("channel")
			blocks=event.get("blocks")
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
			dt_search_string = now.strftime("%d/%m/%Y")

			m=json.dumps({"usuario" : name, "texto" : text, "fecha" : dt_string, "fechaB" : dt_search_string, "canal" : sl_channel, "bloques" : blocks})
			print(m)
			channel.basic_publish(exchange="nestor", routing_key="intake", body=m)

if __name__=="__main__":
	#create the logging object
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	logger.addHandler(logging.StreamHandler())
	#Run our app on our externally facing ip address on port 3000 insteaf o running it on localhost wich is traditional for development
	app.run(host='0.0.0.0', port=3000)