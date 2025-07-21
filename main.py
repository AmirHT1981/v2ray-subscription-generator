nodes = [
    "vmess://eyJhZGQiOiAidGVzdC5jb20iLCAicG9ydCI6ICI0NDMiLCAidHlwZSI6ICJub25lIiwgImlkIjogIjEyMzQ1Ni03ODkwIiwgImFpZCI6ICI2NCIsICJuZXQiOiAidGNwIiwgInRscyI6ICJub25lIiwgInYiOiAiMiJ9"
]

def check_node(node):
    return True

def main():
    active_nodes = [node for node in nodes if check_node(node)]
    with open("docs/subscription.txt", "w") as f:
        f.write("\n".join(active_nodes))

if __name__ == "__main__":
    main()
