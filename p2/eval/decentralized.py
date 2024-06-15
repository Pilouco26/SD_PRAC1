import grpc
from concurrent import futures
import time
import threading
import os
import yaml
import store_pb2
import store_pb2_grpc


class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()
        self.sleep = False

    def put(self, request, context):
        while self.sleep:
            time.sleep(1)
        stubs = create_stubs(load_config())
        if quorum_put(stubs, request.key, request.value, 3):
            return store_pb2.PutResponse(success=True)
        else:
            return store_pb2.PutResponse(success=False)

    def get(self, request, context):
        while self.sleep:
            time.sleep(1)
        stubs = create_stubs(load_config())
        value = quorum_get(self, stubs, request.key, 2)
        if value is None:
            return store_pb2.GetResponse(found=False)
        return store_pb2.GetResponse(value=value, found=True)

    def slowDown(self, request, context):
        self.sleep = True
        time.sleep(request.seconds)
        self.sleep = False
        return store_pb2.SlowDownResponse(success=True)

    def restore(self, request, context):
        self.sleep = False
        return store_pb2.RestoreResponse(success=True)

    def canCommit(self, request, context):
        return store_pb2.CanCommitResponse(canCommit=True)

    def doCommit(self, request, context):
        with self.lock:
            self.data[request.key] = request.value
        return store_pb2.DoCommitResponse(success=True)

    def abort(self, request, context):
        return store_pb2.AbortResponse(success=True)


def serve(port):
    ip_address = "localhost"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kv_store_servicer = KeyValueStoreServicer()
    if os.path.exists("backup.txt"):
        with open("backup.txt", "r") as f:
            for line in f:
                key, value = line.strip().split("=", 1)
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


def quorum_put(stubs, key, value, write_quorum_size):
    vote_count = 0
    for stub, weight in stubs:
        response = stub.canCommit(store_pb2.CanCommitRequest(key=key, value=value))
        if response.canCommit:
            vote_count += weight
        if vote_count >= write_quorum_size:
            for stub, weight in stubs:
                stub.doCommit(store_pb2.DoCommitRequest(key=key, value=value))
            return True
    for stub, weight in stubs:
        stub.abort(store_pb2.AbortRequest(key=key))
    return False


def quorum_get(self, stubs, key, read_quorum_size):
    responses = []
    total_weight = 0
    for stub, weight in stubs:
        value = self.data.get(key, "")
        if value:
            responses.append(value)
            total_weight += weight
        if total_weight >= read_quorum_size:
            break
    return max(set(responses), key=responses.count) if responses else None


def load_config():
    with open('decentralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    return config


def create_stubs(config):
    stubs = []
    for node in config['nodes']:
        channel = grpc.insecure_channel(f"{node['ip']}:{node['port']}")
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        stubs.append((stub, node['weight']))
    return stubs


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
