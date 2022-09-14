from .deploy_fish import run_cmd


def start_miner():
    cmd = """
    ironfish miners:start --rpc.tcp
    -p 127.0.0.1:14444
    -a 814b8229e796eff3a470de8e6633ce6c1229ae76f75647b14ce93ba9292433e18c4afc831aa434fef2d117
    -t 1
    """
    cmd = cmd.strip()
    cmd = cmd.replace("\n", " ")
    cmd = cmd.replace("    ", "")
    print(cmd)
    run_cmd(cmd)
