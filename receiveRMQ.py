#!/usr/bin/env python
import pika
import sys
import os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Declare an exchange named 'chat_exchange' of type 'direct'
    channel.exchange_declare(exchange='chat_exchange', exchange_type='direct')

    # Declare a random queue. The queue will be deleted when the consumer connection is closed.
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    # Bind the queue to the exchange with routing key 'chatID'
    channel.queue_bind(exchange='chat_exchange', queue=queue_name, routing_key='chatID')

    def callback(ch, method, properties, body):
        print(body.decode('utf-8'))

    # Consume messages from the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    while True:
        channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
