import threading

import redis
import pika
import json
from p1.BackEnd.bigChat import ChatConsumer


redis_host = "localhost"
redis_port = 6379
redis_password = ""


class NameServer:
    def __init__(self):
        self.nomChat = "chat_discovery"
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.nomChat, exchange_type='direct')
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        self.message_queue_key = 'petitions'
        self.message_queue_display_key = 'display'
        self.pubsub_channel_prefix = 'petition_channel:'
        self.pubsub_channel_display_prefix = 'display_channel:'
        self.exchange_names = []
    def register_user(self, username, ip_address, port):
        self.redis.hset('chat:{}'.format(username), 'ip', ip_address)
        self.redis.hset('chat:{}'.format(username), 'port', port)

    def get_connection_params(self, username):
        ip_address = self.redis.hget('chat:{}'.format(username), 'ip')
        port = self.redis.hget('chat:{}'.format(username), 'port')
        if ip_address and port:
            return ip_address, port
        else:
            return None, None

    def push_petition(self, petition):
        self.redis.lpush(self.message_queue_key, petition)

    def send_chats(self):
        return self.exchange_names

    def process_petitions(self):
        while True:
            petition = self.redis.lpop(self.message_queue_key)  # Use lpop
            if petition:
                # Split the petition into its components
                parts = petition.split(':')
                if len(parts) == 4:  # Ensure it has four parts
                    username, ip_address, port, r = parts
                    # Check if the petition has the correct format
                    if username and ip_address and port:
                        self.register_user(username, ip_address, port)
                        print('Registered')
                    else:
                        print("Invalid petition format:", petition)
                elif len(parts) == 3:  # If it has three parts
                    username, ip_address, port = parts
                    if username:
                        info = self.get_connection_params(username)
                        ip, port = info
                        channel2 = self.pubsub_channel_prefix + ip_address
                        if ip is not None:
                            # Publish the information to a channel associated with the sender's IP
                            self.redis.publish(channel2, ":".join(info))
                            print('Published')
                        else:
                            self.redis.publish(channel2, "error")
                            print("No info found for username:", username)
                    else:
                        print("Invalid petition format:", petition)
                # Si no esta creat, crear-lo i retornar id
                elif len(parts) == 2:
                    petition, exchange_name = parts
                    if exchange_name not in self.exchange_names:
                        self.create_chat(exchange_name)

                elif len(parts) == 1:
                    body_data = json.dumps(self.exchange_names)  # Convert list to JSON string
                    self.channel.basic_publish(exchange=self.nomChat, routing_key='chatID', body=body_data)

                    print('Chats updated!')

                else:
                    print("Invalid petition format:", petition)

    # DEMANAR PETICIÓ
    def create_chat(self, exchange_name):
        ChatConsumer(exchange_name)
        name_server.exchange_names.append(exchange_name)

    # crear xat
    def connect_to_chat(self):
        data = "connection:" + self.nomChat
        self.redis.lpush(self.message_queue_key, data)
        thread = threading.Thread(target=self.conf, args=(self.nomChat,))
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    # Example usage
    name_server = NameServer()
    # test
    name_server.register_user("prova", "68.69.69.69", 5050)
    name_server.process_petitions()
