import socket
import threading
import grpc
from concurrent import futures
import time

import xatPrivat_pb2
import xatPrivat_pb2_grpc


class Master():
    connected_clients = {}
    message_queue = {}

    def __init__(self):
        self.connected_clients = {}
        self.connected_clientsList = []
        self.message_queue = {}
        self.cv = threading.Condition()

    def Connect(self, request, context):
        return 0

    def Write(self, request, context):
        return 0

    def Read(self, request, context):
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
