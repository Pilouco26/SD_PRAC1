import grpc
import store_pb2
import store_pb2_grpc
import yaml
import threading
import time


def create_stubs(config):
    stubs = []
    for node in config['nodes']:
        channel = grpc.insecure_channel(f"{node['ip']}:{node['port']}")
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        stubs.append((stub, node['weight']))
    return stubs


def test_quorum_put(stubs, key, value, write_quorum_size):
    total_weight = 0
    for stub, weight in stubs:
        response = stub.put(store_pb2.PutRequest(key=key, value=value))
        if response.success:
            total_weight += weight
        if total_weight >= write_quorum_size:
            break
    assert total_weight >= write_quorum_size, "Put operation did not meet the quorum size."


def test_quorum_get(stubs, key, expected_value, read_quorum_size):
    responses = []
    total_weight = 0
    for stub, weight in stubs:
        response = stub.get(store_pb2.GetRequest(key=key))
        if response.found:
            responses.append(response.value)
            total_weight += weight
        if total_weight >= read_quorum_size:
            break
    result = max(set(responses), key=responses.count) if responses else None
    assert total_weight >= read_quorum_size, "Get operation did not meet the quorum size."
    assert result == expected_value, f"Expected value: {expected_value}, but got: {result}"


if __name__ == '__main__':
    with open('decentralized_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    stubs = create_stubs(config)
    write_quorum_size = 3  # As defined in the prompt
    read_quorum_size = 2   # As defined in the prompt

    key, value = "testKey", "testValue"

    # Test put operation
    test_quorum_put(stubs, key, value, write_quorum_size)
    print("Put operation test passed")

    # Allow some time for put operations to propagate
    time.sleep(1)

    # Test get operation
    test_quorum_get(stubs, key, value, read_quorum_size)
    print("Get operation test passed")
