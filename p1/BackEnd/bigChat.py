import time
import pika


class ChatConsumer:
    def __init__(self, exchange):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange=exchange, queue=self.queue_name, routing_key='chatID')
        self.messages = []
        self.user_message_counts = {}  # Store the count of messages for each user
        self.user_message_times = {}  # Store the time of the last message for each user

    def callback(self, ch, method, properties, body):
        user_id = properties.user_id  # Assuming the user_id is stored in properties
        if user_id not in self.user_message_counts:
            self.user_message_counts[user_id] = 0
            self.user_message_times[user_id] = time.time()
        if time.time() - self.user_message_times[user_id] < 60:  # Check if less than 60 seconds have passed
            if self.user_message_counts[user_id] > 10:  # Check if the user has sent more than 10 messages in the
                # last minute
                print("Spam detected from user", user_id)
                return
            else:
                self.user_message_counts[user_id] += 1
        else:
            self.user_message_counts[user_id] = 1
            self.user_message_times[user_id] = time.time()
        message = body.decode()
        self.messages.append(message)
        print(message)
