from deploy_fish import run_cmd, run_with_output


def start_miner():
    cmd = """
    ironfish miners:start --rpc.tcp
    -p 127.0.0.1:9034
    -a 814b8229e796eff3a470de8e6633ce6c1229ae76f75647b14ce93ba9292433e18c4afc831aa434fef2d117
    -t 1
    """
    cmd = cmd.split()
    cmd = " ".join(cmd)
    print(cmd)
    run_cmd(cmd)


def start_pool():
    cmd = "ironfish miners:pools:start --no-payouts"
    run_with_output(cmd)


def start_node():
    cmd = "ironfish start -v --port 14444  --rpc.tcp.secure --rpc.tcp"
    run_with_output(cmd)


if __name__ == "__main__":
    allow = ["miner", "node", "pool"]
    cmd = input("ironfish mod to start(node, pool, miner): ")
    if cmd == "miner":
        start_miner()
    elif cmd == "node":
        start_node()
    elif cmd == "pool":
        start_pool()
    else:
        print("not support")
