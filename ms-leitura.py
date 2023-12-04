#!/usr/bin/python

import os
import time
from random import randrange

import pika
from dotenv import load_dotenv

load_dotenv(verbose=True)

RABBITMQ_URL      = os.getenv('RABBITMQ_URL')
RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_QUEUE    = os.getenv('RABBITMQ_QUEUE')
RABBITMQ_PREFETCH = int(os.getenv('RABBITMQ_PREFETCH'))

connection = pika.BlockingConnection(
  pika.ConnectionParameters(
    host=RABBITMQ_URL,
    credentials=pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
  )
)

channel = connection.channel()

channel.queue_declare(queue=RABBITMQ_QUEUE)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(randrange(0, 2))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=RABBITMQ_PREFETCH)
channel.basic_consume(on_message_callback=callback, queue=RABBITMQ_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
