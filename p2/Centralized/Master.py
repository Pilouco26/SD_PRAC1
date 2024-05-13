import socket
import threading
import grpc
from concurrent import futures
import time

import xatPrivat_pb2
import xatPrivat_pb2_grpc


class Master:
    connected_clients = {}
    message_queue = {}

    def __init__(self):
        self.connected_clients = {}
        self.connected_clientsList = []
        self.message_queue = {}
        self.cv = threading.Condition()
        self.nodes = []
        self.node_id = "master"

    def can_commit(self):
        try:
            message = "canCommit?"
            # Crear un canal gRPC hacia el servidor
            channel = grpc.insecure_channel(f'{self.server_ip}:{self.client.server_port}')
            stub = xatPrivat_pb2_grpc.ChatServiceStub(channel)
            unanimity = True
            # Llamar al método Connect del servidor
            for node in self.nodes and unanimity == True:
                response = stub.SendMessage(
                    xatPrivat_pb2.ChatMessage(from_id=self.node_id, to_id=node, message=message))
                if response.message == 'No':
                    unanimity = False
        except grpc.RpcError as e:
            print(f"Error connecting to chat: {e}")

    def Connect(self, request, context):
        return 0

    def canCommit(self):

        return False

    def doCommit(self, request, context):
        return 0

    def doAbort(self, request, context):
        return 0


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server.add_insecure_port('[::]:32770')
    server.start()
    try:

        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        return


if __name__ == '__main__':
    serve()
