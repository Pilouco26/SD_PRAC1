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
        self.connected_clients = {}
        self.message_queue = {}
        self.cv = threading.Condition()

    def Connect(self, request, context):
        print(f"Client {request.client_id} connected at {request.client_address}")
        self.connected_clients[request.client_id] = context
        self.message_queue[request.client_id] = []
        return xatPrivat_pb2.ConnectionResponse(message="Connected")

    def SendMessage(self, request, context):
        print(f"Message from {request.from_id}: {request.message}")
        with self.cv:
            if request.to_id in self.connected_clients:
                if request.to_id not in self.message_queue:
                    self.message_queue[request.to_id] = []
                self.message_queue[request.to_id].append(request)
                self.cv.notify_all()
        return xatPrivat_pb2.MessageAck(message="Message received")

    def ReceiveMessage(self, request, context):
        with self.cv:
            while True:
                if request.client_id in self.message_queue and self.message_queue[request.client_id]:
                    message = self.message_queue[request.client_id].pop(0)
                    return message
                self.cv.wait()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    xatPrivat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
