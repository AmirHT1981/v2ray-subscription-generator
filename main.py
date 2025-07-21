import base64
import json
import socket
import time

def read_nodes(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]

def check_node(node):
    try:
        data = base64.b64decode(node[8:]).decode()
        config = json.loads(data)
        address = config["add"]
        port = int(config["port"])
        s = socket.socket()
        s.settimeout(2)
        start = time.time()
        s.connect((address, port))
        latency = time.time() - start
        s.close()
        return latency
    except Exception as e:
        return None

def main():
    nodes = read_nodes("nodes.txt")
    results = []
    for node in nodes:
        latency = check_node(node)
        if latency is not None:
            results.append((latency, node))
            print(f"OK: {node[:30]}... - {latency:.2f}s")
        else:
            print(f"FAIL: {node[:30]}...")

    results.sort(key=lambda x: x[0])
    best_nodes = [node for _, node in results[:10]]

    with open("docs/subscription.txt", "w") as f:
        f.write("\n".join(best_nodes))

if __name__ == "__main__":
    main()
