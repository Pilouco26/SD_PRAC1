from concurrent.futures import ThreadPoolExecutor

import grpc
from concurrent import futures
import time
import threading
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


import socket


def serve_master(port):
    ip_address = "localhost"
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port(f'{ip_address}:{port}')

    def run_server():
        try:
            server.start()
            print(f"Server Master listening on {ip_address}:{port}")
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            server.wait_for_termination()

    thread = threading.Thread(target=run_server)
    thread.start()
    return thread


def serve_slave(port, master_stub):
    ip_address = "localhost"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port(f'{ip_address}:{port}')

    def run_server():
        try:
            server.start()
            print(f"\nServer slave listening on {ip_address}:{port}")
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            server.wait_for_termination()

    thread = threading.Thread(target=run_server)
    thread.start()
    return thread


if __name__ == '__main__':
    with open('centralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

        serve_master(config['master']['port'])
        master_stub = grpc.insecure_channel(f"{config['master']['ip']}:{config['master']['port']}")
        for i in range(2):
            serve_slave(config['slaves'][i]['port'], store_pb2_grpc.KeyValueStoreStub(master_stub))

    # Once setup is done, keep servers active
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass  # Handles keyboard interrupt to exit gracefully
