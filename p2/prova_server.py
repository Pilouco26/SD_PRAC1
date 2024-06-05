import time

import grpc
import store_pb2  # Replace with your actual package path
import store_pb2_grpc


def wait_for_server(channel, timeout=15):
    """Wait until the server is available or the timeout is reached."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            grpc.channel_ready_future(channel).result(timeout=1)
            return True
        except grpc.FutureTimeoutError:
            continue
    return False


def connect_to_server(address, port):
    channel_address = f"localhost:{port}"
    channel = grpc.insecure_channel(channel_address)
    if not wait_for_server(channel):
        raise Exception(f"Failed to connect to the gRPC server ({channel_address}).")
    print("connected")
    return channel, store_pb2_grpc.KeyValueStoreStub(channel)


def main():
    address = "localhost"
    port = 50053
    channel, stub = connect_to_server(address, port)

    # Example usage: Put a key-value pair
    response = stub.put(store_pb2.PutRequest(key="test_key", value="test_value"))
    print(f"Put response: {response}")
    time.sleep(0.1)  # Simulate time delay between operations
    get_response = stub.get(store_pb2.GetRequest(key="test_key"))
    print(f"Get response: {get_response}")  # This line retrieves the value


    # You can add more calls to your gRPC service methods here

    channel.close()  # Close the channel when finished


if __name__ == "__main__":
    main()
