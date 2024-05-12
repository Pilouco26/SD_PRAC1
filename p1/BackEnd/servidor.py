import socket
import threading
import grpc
from concurrent import futures
import time

import xatPrivat_pb2
import xatPrivat_pb2_grpc


class ChatServer(xatPrivat_pb2_grpc.ChatServiceServicer):
    connected_clients = {}
    message_queue = {}

    def __init__(self):
        # FALLA connected_clients
        self.connected_clients = {}
        self.connected_clientsList = []
        self.message_queue = {}
        self.cv = threading.Condition()

    def Connect(self, request, context):
        print(f"Client {request.client_id} connected at {request.client_address}")
        self.connected_clients[request.client_id] = context
        self.connected_clientsList.append(request.client_id)
        self.message_queue[request.client_id] = []
        print(f"Current connected clients: {self.connected_clients.keys()}")
        return xatPrivat_pb2.ConnectionResponse(message="Connected")

    def SendMessage(self, request, context):
        print(f"Message from {request.from_id}: {request.message}")
        with self.cv:
            if request.to_id in self.connected_clientsList:
                if request.to_id not in self.message_queue:
                    self.message_queue[request.to_id] = []
                self.message_queue[request.to_id].append(request)
                print(f"Current message queue for {request.to_id}: {self.message_queue[request.to_id]}")
                self.cv.notify_all()
            else:
                print("not in request.to_id")
        return xatPrivat_pb2.MessageAck(message="Message received")

    # MIRAR SI REQUEST.CLIENT_ID CONSIDEIX AMB LA IP DE LA UI CONECTADA!
    def ReceiveMessage(self, request, context):
        with self.cv:
            while True:
                print(f"Waiting for messages for client {request.client_id}")
                if request.client_id in self.message_queue and self.message_queue[request.client_id]:
                    message = self.message_queue[request.client_id].pop(0)
                    return message
                self.cv.wait()

def get_local_ip_and_port():
    # Fetch the local IP address of the machine
    ip_address = socket.gethostbyname(socket.gethostname())
    # Find an available port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close()
    return ip_address, port
def serve():
    ip, port = get_local_ip_and_port()
    print(f"Serving on {ip}:{port}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServer(), server)
    server.add_insecure_port('[::]:59137')
    server.add_insecure_port('[::]:59138')
    server.add_insecure_port('[::]:59139')
    server.start()
    print("started")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
