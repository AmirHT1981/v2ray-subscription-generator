import base64
import subprocess

NODES_FILE = "nodes.txt"
OUTPUT_FILE = "docs/subscription.txt"

def check_node(node):
    try:
        b64_part = node[8:].strip()  # حذف فاصله‌ها و 'vmess://'
        decoded = base64.b64decode(b64_part).decode()
        # اینجا می‌تونی تست پینگ یا تست اتصال اضافه کنی
        # مثلاً با subprocess پینگ بزن یا درخواست TCP باز کن
        return True
    except Exception as e:
        print(f"Invalid node skipped: {node[:30]}... because {e}")
        return False

def main():
    try:
        with open(NODES_FILE, "r") as f:
            nodes = f.readlines()
    except FileNotFoundError:
        print(f"{NODES_FILE} not found!")
        return

    valid_nodes = []

    for node in nodes:
        node = node.strip()
        if not node:
            continue
        if node.startswith("vmess://") and check_node(node):
            valid_nodes.append(node)

    if not valid_nodes:
        print("No valid nodes found.")
        return

    with open(OUTPUT_FILE, "w") as f:
        for node in valid_nodes:
            f.write(node + "\n")

    print(f"Subscription updated with {len(valid_nodes)} nodes.")

if __name__ == "__main__":
    main()
