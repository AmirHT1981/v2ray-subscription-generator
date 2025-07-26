import base64
import requests
import subprocess
import concurrent.futures
import re
import json

def load_sources(file='nodes_sources.txt'):
    with open(file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

def fetch_nodes_from_url(url):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        text = resp.text
        nodes = re.findall(r'(vmess://[A-Za-z0-9+/=]+)', text)
        return nodes
    except Exception as e:
        print(f"Failed to fetch from {url}: {e}")
        return []

def extract_address(node):
    try:
        b64 = node[8:]
        json_str = base64.b64decode(b64).decode()
        j = json.loads(json_str)
        return j.get("add", None)
    except:
        return None

def ping_host(host):
    if not host:
        return 9999
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', host], capture_output=True)
        output = result.stdout.decode()
        match = re.search(r'time=(\d+\.?\d*) ms', output)
        if match:
            return float(match.group(1))
        else:
            return 9999
    except Exception:
        return 9999

def check_node_latency(node):
    host = extract_address(node)
    latency = ping_host(host)
    return node, latency

def main():
    urls = load_sources()
    print(f"Loading nodes from {len(urls)} sources...")
    
    all_nodes = []
    for url in urls:
        nodes = fetch_nodes_from_url(url)
        print(f"Got {len(nodes)} nodes from {url}")
        all_nodes.extend(nodes)
    
    print(f"Total nodes fetched: {len(all_nodes)}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_node_latency, all_nodes))
    
    results = sorted(results, key=lambda x: x[1])
    
    best_nodes = [node for node, latency in results[:10]]
    print("Best 10 nodes:")
    for n, l in results[:10]:
        print(f"Latency: {l} ms, Node: {n[:50]}...")
    
    # ⚠️ توجه: اینجا بدون Base64 کل!
    subscription_content = '\n'.join(best_nodes)
    
    with open('docs/subscription.txt', 'w') as f:
        f.write(subscription_content)
    
    print("Subscription updated in docs/subscription.txt")

if __name__ == "__main__":
    main()
