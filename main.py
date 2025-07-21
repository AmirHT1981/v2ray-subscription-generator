import base64

# خروجی نهایی توی پوشه docs ساخته میشه
OUTPUT_FILE = "docs/subscription.txt"

# لیست نودها (مثال)
nodes = [
    "vmess://eyJhZGQiOiAidGVzdC5jb20iLCAicG9ydCI6ICI0NDMiLCAidHlwZSI6ICJub25lIiwgImlkIjogIjEyMzQ1Ni03ODkwIiwgImFpZCI6ICI2NCIsICJuZXQiOiAidGNwIiwgInRscyI6ICJub25lIiwgInYiOiAiMiJ9",
    "vmess://eyJhZGQiOiAidGVzdDIuY29tIiwgInBvcnQiOiAiNDQzIiwgInR5cGUiOiAibm9uZSIsICJpZCI6ICI3ODkwMTIzIiwgImFpZCI6ICI2NCIsICJuZXQiOiAidGNwIiwgInRscyI6ICJub25lIiwgInYiOiAiMiJ9"
]

def check_node(node):
    """
    اینجا میتونی پینگ یا هر چک دیگه‌ای بذاری.
    فعلا همه رو اوکی برمیگردونه.
    """
    try:
        data = base64.b64decode(node[8:]).decode()
        return True
    except Exception:
        return False

def main():
    active_nodes = [node for node in nodes if check_node(node)]
    content = "\n".join(active_nodes)
    with open(OUTPUT_FILE, "w") as f:
        f.write(content)
    print(f"Subscription written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
