import grpc
from concurrent import futures
import time
import threading
import random
import sys
import os
import yaml
import store_pb2
import store_pb2_grpc


class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def put(self, request, context):
        with self.lock:
            self.data[request.key] = request.value
            with open("backup.txt", "a") as f:  # Open in append mode
                f.write(f"{request.key}={request.value}\n")  # Write key-value pair with newline
        return store_pb2.PutResponse(success=True)

    def get(self, request, context):
        with self.lock:
            value = self.data.get(request.key, None)
        if value is None:
            return store_pb2.GetResponse(found=False)
        return store_pb2.GetResponse(value=value, found=True)

    def slowDown(self, request, context):
        time.sleep(request.seconds)
        return store_pb2.SlowDownResponse(success=True)

    def restore(self, request, context):
        return store_pb2.RestoreResponse(success=True)


def serve(port):
    ip_address = "localhost"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kv_store_servicer = KeyValueStoreServicer()
    with open("backup.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)  # Split by = sign, max split 1
            kv_store_servicer.data[key] = value
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(kv_store_servicer, server)
    server.add_insecure_port(f'{ip_address}:{port}')
    def run_server():
        try:
            server.start()
            print(f"Server listening on {ip_address}:{port}")
        except Exception as e:
            print(f"Error starting server: {e}")
        finally:
            server.wait_for_termination()

    run_server()
    return 0


def quorum_put(stubs, key, value):
    successful_puts = 0
    for stub in stubs:
        response = stub.put(store_pb2.PutRequest(key=key, value=value))
        if response.success:
            successful_puts += 1
    return successful_puts >= len(stubs) // 2 + 1


def quorum_get(stubs, key):
    responses = []
    for stub in stubs:
        response = stub.get(store_pb2.GetRequest(key=key))
        if response.found:
            responses.append(response.value)
    return max(set(responses), key=responses.count) if responses else None


if __name__ == '__main__':

    if not os.path.exists("backup.txt"):
        # Create an empty backup.txt file
        with open("backup.txt", "w"):
            pass


    with open('decentralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        threads = []
        for i in range(3):
            port = config['nodes'][i]['port']
            thread = threading.Thread(target=serve, args=(port,))
            threads.append(thread)
            thread.start()

        # Optionally join the threads if you want to wait for them to finish
        for thread in threads:
            thread.join()

