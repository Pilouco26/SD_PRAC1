import threading

import pika
import sys
import os




class ChatConsumer:
    def __init__(self, exchange):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        ###MIRAR QUE FA UNIC UN CHAT
        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key='chatID')
        self.messages = []


##PROVAR