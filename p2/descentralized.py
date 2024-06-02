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

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()

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
    with open('decentralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    node_info = config['nodes'][int(sys.argv[1])]
    serve(node_info['port'])
