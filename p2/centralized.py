import logging
import os
from concurrent.futures import ThreadPoolExecutor
import grpc
from concurrent import futures
import time
import threading
import yaml
import store_pb2
import store_pb2_grpc


class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, role):
        self.role = role
        self.data = {}
        self.slaves = []
        self.lock = threading.Lock()
        self.canCommitX = True

    def put(self, request, context):
        self.canCommitX = False
        key, value = request.key, request.value
        logging.debug(f"put() called with key={request.key} value={request.value}")
        # Phase 1: Prepare
        can_commit = True
        for slave in self.slaves:
            print("slave:", slave)
            response = slave.canCommit(store_pb2.CanCommitRequest(key=key, value=value))
            if not response.canCommit:
                can_commit = False
                break

        if not can_commit:
            for slave in self.slaves:
                slave.abort(store_pb2.AbortRequest(key=key))
            return store_pb2.PutResponse(success=False)

        # Phase 2: Commit
        for slave in self.slaves:
            slave.doCommit(store_pb2.DoCommitRequest(key=key, value=value))
            with self.lock:
                self.data[key] = value
                with open("backup.txt", "a") as f:  # Open in append mode
                    f.write(f"{key}={value}\n")  # Write key-value pair with newline




        self.canCommitX = True
        return store_pb2.PutResponse(success=True)

    def get(self, request, context):
        self.canCommitX = False
        logging.debug(f"get() called with key={request.key}")
        key = request.key
        with self.lock:
            value = self.data.get(key, "")

        self.canCommitX = True
        return store_pb2.GetResponse(value=value)

    def slowDown(self, request, context):
            time.sleep(request.seconds)
            return store_pb2.SlowDownResponse(success=True)
    def restore(self, request, context):
            return store_pb2.RestoreResponse(success=True)

    def add_slave(self, slave_stub):
        self.slaves.append(slave_stub)

    def canCommit(self, request, context):
        return store_pb2.CanCommitResponse(canCommit=self.canCommitX)

    def doCommit(self, request, context):
        with self.lock:
            self.data[request.key] = request.value
        return store_pb2.DoCommitResponse(success=True)

    def abort(self, request, context):
        return store_pb2.AbortResponse(success=True)

def serve_master(port):
    ip_address = "localhost"
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    kv_store_servicer = KeyValueStoreServicer("master")
    with open("backup.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)  # Split by = sign, max split 1
            kv_store_servicer.data[key] = value
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(kv_store_servicer, server)
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
    return thread, kv_store_servicer

def serve_slave(port, master_stub):
    ip_address = "localhost"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kv_store_servicer = KeyValueStoreServicer("slave")
    with open("backup.txt", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)  # Split by = sign, max split 1
            kv_store_servicer.data[key] = value
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(kv_store_servicer, server)
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

    return thread, store_pb2_grpc.KeyValueStoreStub(grpc.insecure_channel(f'{ip_address}:{port}'))

if __name__ == '__main__':
    # Remove backup.txt if it exists
    if not os.path.exists("backup.txt"):
        # Create an empty backup.txt file
        with open("backup.txt", "w"):
            pass


    with open('centralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

        master_thread, master_servicer = serve_master(config['master']['port'])
        master_stub = grpc.insecure_channel(f"{config['master']['ip']}:{config['master']['port']}")

        slave_threads = []
        for i in range(2):
            slave_thread, slave_stub = serve_slave(config['slaves'][i]['port'], store_pb2_grpc.KeyValueStoreStub(master_stub))
            master_servicer.add_slave(slave_stub)
            slave_threads.append(slave_thread)
    # Once setup is done, keep servers active
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass  # Handles keyboard interrupt to exit gracefully
