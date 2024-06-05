import grpc
from concurrent import futures
import time
import threading
import sys
import os
import yaml
import store_pb2
import store_pb2_grpc


class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.store = {}
        self.lock = threading.Lock()

    def put(self, request, context):
        with self.lock:
            self.store[request.key] = request.value
        return store_pb2.PutResponse(success=True)

    def get(self, request, context):
        with self.lock:
            value = self.store.get(request.key, None)
        if value is None:
            return store_pb2.GetResponse(found=False)
        return store_pb2.GetResponse(value=value, found=True)

    def slowDown(self, request, context):
        time.sleep(request.seconds)
        return store_pb2.SlowDownResponse(success=True)

    def restore(self, request, context):
        return store_pb2.RestoreResponse(success=True)


def serve_master(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


def serve_slave(port, master_stub):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()

    def sync_with_master():
        while True:
            time.sleep(10)

    threading.Thread(target=sync_with_master).start()
    server.wait_for_termination()


if __name__ == '__main__':
    with open('centralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

        serve_master(config['master']['port'])
        master_stub = grpc.insecure_channel(f"{config['master']['ip']}:{config['master']['port']}")
        serve_slave(config['slaves'][0]['port'], store_pb2_grpc.KeyValueStoreStub(master_stub))
