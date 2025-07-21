import base64
import requests
import subprocess
import concurrent.futures
import re

# خواندن URL منابع نود
def load_sources(file='nodes_sources.txt'):
    with open(file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls

# گرفتن لیست نودها از یک URL (فقط vmess:// داخل متن)
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

# تابع برای ping ساده روی سرور (extract hostname از vmess json)
def extract_address(node):
    try:
        b64 = node[8:]
        json_str = base64.b64decode(b64).decode()
        import json
        j = json.loads(json_str)
        return j.get("add", None)
    except:
        return None

def ping_host(host):
    if not host:
        return 9999
    try:
        # اجرا کردن دستور ping (یک بار با timeout 1 ثانیه)
        result = subprocess.run(['ping', '-c', '1', '-W', '1', host], capture_output=True)
        output = result.stdout.decode()
        match = re.search(r'time=(\d+\.?\d*) ms', output)
        if match:
            return float(match.group(1))
        else:
            return 9999
    except Exception as e:
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
    
    # پینگ گرفتن موازی برای سرعت
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_node_latency, all_nodes))
    
    # مرتب سازی بر اساس latency
    results = sorted(results, key=lambda x: x[1])
    
    # انتخاب بهترین 10 نود
    best_nodes = [node for node, latency in results[:10]]
    print("Best 10 nodes:")
    for n, l in results[:10]:
        print(f"Latency: {l} ms, Node: {n[:50]}...")
    
    # ساختن فایل subscription (Base64 تمام نودها با \n)
    subscription_content = '\n'.join(best_nodes).encode()
    subscription_b64 = base64.b64encode(subscription_content).decode()
    
    # ذخیره در docs/subscription.txt
    with open('docs/subscription.txt', 'w') as f:
        f.write(subscription_b64)
    print("Subscription updated in docs/subscription.txt")

if __name__ == "__main__":
    main()
