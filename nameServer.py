import redis

redis_host = "localhost"
redis_port = 6379
redis_password = ""


class NameServer:
    def __init__(self):
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
        self.message_queue_key = 'petitions'
        self.pubsub_channel_prefix = 'petition_channel:'

    def register(self, username, ip_address, port):
        self.redis.hset('chat:{}'.format(username), 'ip', ip_address)
        self.redis.hset('chat:{}'.format(username), 'port', port)

    def get_connection_params(self, username):
        ip_address = self.redis.hget('chat:{}'.format(username), 'ip')
        port = self.redis.hget('chat:{}'.format(username), 'port')
        return ip_address, port

    def push_petition(self, petition):
        self.redis.lpush(self.message_queue_key, petition)

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
                        self.register(username, ip_address, port)
                        print('Registered')
                    else:
                        print("Invalid petition format:", petition)
                elif len(parts) == 3:  # If it has three parts
                    username, ip_address, port = parts
                    if username:
                        info = self.get_connection_params(username)
                        if info:
                            # Publish the information to a channel associated with the sender's IP
                            channel = self.pubsub_channel_prefix + ip_address
                            self.redis.publish(channel, ":".join(info))
                            print('Published')
                        else:
                            print("No info found for username:", username)
                    else:
                        print("Invalid petition format:", petition)
                else:
                    print("Invalid petition format:", petition)


if __name__ == "__main__":
    # Example usage
    name_server = NameServer()
    # test
    name_server.register("prova", "68.69.69.69", 5050)
    name_server.process_petitions()
