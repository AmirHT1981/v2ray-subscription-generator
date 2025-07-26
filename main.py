import base64
import requests
import subprocess
import concurrent.futures
import re
import json
import socket
import time


# ------------------------------
# خواندن لینک‌ها از فایل
def load_sources(file='nodes_sources.txt'):
    with open(file, 'r') as f:
        return [line.strip() for line in f if line.strip()]


# ------------------------------
# گرفتن نودها از هر سورس
def fetch_nodes_from_url(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text
        nodes = re.findall(r'(vmess://[A-Za-z0-9+/=]+)', text)
        return nodes
    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        return []


# ------------------------------
# decode کردن vmess → گرفتن host و port
def parse_vmess(node):
    try:
        raw = node[8:]
        decoded = base64.b64decode(raw).decode()
        j = json.loads(decoded)
        host = j.get('add')
        port = int(j.get('port'))
        return host, port
    except:
        return None, None


# ------------------------------
# تست ICMP Ping
def ping_host(host):
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '1', host],
            capture_output=True
        )
        output = result.stdout.decode()
        match = re.search(r'time=(\d+\.?\d*) ms', output)
        if match:
            return float(match.group(1))
        return None
    except:
        return None


# ------------------------------
# تست TCP Port
def check_tcp(host, port):
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=2)
        sock.close()
        latency = (time.time() - start) * 1000  # ms
        return latency
    except:
        return None


# ------------------------------
# ترکیب تست‌ها
def check_node_latency(node):
    host, port = parse_vmess(node)
    if not host or not port:
        return node, 9999

    latency = ping_host(host)
    if latency is None:
        latency = check_tcp(host, port)
    if latency is None:
        latency = 9999

    return node, latency


# ------------------------------
# اجرا
def main():
    urls = load_sources()
    print(f"🔗 Found {len(urls)} sources...")

    all_nodes = []
    for url in urls:
        nodes = fetch_nodes_from_url(url)
        print(f"✅ {url} → {len(nodes)} nodes")
        all_nodes.extend(nodes)

    print(f"📡 Total nodes fetched: {len(all_nodes)}")

    # موازی سازی
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(check_node_latency, all_nodes))

    # مرتب‌سازی
    results = sorted(results, key=lambda x: x[1])

    # بهترین‌ها
    best_nodes = [node for node, latency in results[:10]]
    print("\n🏆 Best nodes:")
    for n, l in results[:10]:
        print(f"  {l:.1f} ms → {n[:50]}...")

    # ساخت subscription base64
    content = '\n'.join(best_nodes).encode()
    subscription_b64 = base64.b64encode(content).decode()

    with open('docs/subscription.txt', 'w') as f:
        f.write(subscription_b64)

    print("\n✅ Updated → docs/subscription.txt")


if __name__ == '__main__':
    main()
