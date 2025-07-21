import base64
import socket

def check_node(node):
    if node.startswith('vmess://'):
        data = base64.b64decode(node[8:].encode()).decode()
        if '"add":"' in data:
            host = data.split('"add":"')[1].split('"')[0]
            port = int(data.split('"port":"')[1].split('"')[0])
            try:
                with socket.create_connection((host, port), timeout=2):
                    return True
            except:
                return False
    return False

def main():
    with open('nodes.txt', 'r') as f:
        nodes = f.read().splitlines()

    alive_nodes = []
    for node in nodes:
        if check_node(node):
            alive_nodes.append(node)

    if not alive_nodes:
        print("هیچ نود فعالی پیدا نشد.")
        return

    sub_content = '\n'.join(alive_nodes)
    sub_b64 = base64.b64encode(sub_content.encode()).decode()

    with open('subscription.txt', 'w') as f:
        f.write(sub_b64)

    print("subscription.txt ساخته شد.")

if __name__ == '__main__':
    main()
