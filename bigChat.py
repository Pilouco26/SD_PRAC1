import pika
import sys
import os
import asyncio

class ChatConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='chat_exchange', exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='chat_exchange', queue=self.queue_name, routing_key='chatID')
        self.message_callback = None
        self.messages = []

    def set_message_callback(self, callback):
        self.message_callback = callback

    def callback(self, ch, method, properties, body):
        message = body.decode()
        self.messages.append(message)  # Save the message
        if self.message_callback:
            self.message_callback(message)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()


class MessageHandler:
    def __init__(self):
        self.chat_consumer = ChatConsumer()
        self.chat_consumer.set_message_callback(self.handle_message)

    def handle_message(self, message):
        print(message)
        # Add your message handling logic here

    def get_messages(self):
        return self.chat_consumer.messages


class MessageDisplayer:
    def __init__(self, message_handler):
        self.message_handler = message_handler

    def display_messages(self):
        messages = self.message_handler.get_messages()
        for message in messages:
            print("Message:", message)


if __name__ == '__main__':
    try:
        message_handler = MessageHandler()
        message_displayer = MessageDisplayer(message_handler)
        asyncio.run(message_handler.chat_consumer.start_consuming())
        message_displayer.display_messages()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
