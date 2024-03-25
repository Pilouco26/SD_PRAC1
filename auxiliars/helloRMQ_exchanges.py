#!/usr/bin/env python
import pika

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare the exchange
    channel.exchange_declare(exchange='chat_exchange', exchange_type='direct')

    # Message to be sent
    message = "Hello, World!"

    # Publish the message to the exchange with the routing key 'chatID'
    channel.basic_publish(exchange='chat_exchange', routing_key='chatID', body=message)

    print(" [x] Sent 'Hello, World!'")

    connection.close()

if __name__ == '__main__':
    main()
