import subprocess
from colorama import Fore


# tmux 结构
# session {
#     node (节点 session) {
#         window-0 {
#            pane: node     // node 节点
#            pane: 1        // 可能 node 备用节点
#         }
#     }
#     fish (矿池 session) {
#         window-pool {      // 运行矿池服务
#             pane-0: pool-server
#             pane-1: pool-gate
#             pane-2: coin-distribution
#             pane-3: 
#         }
#         window-middleware { // 运行 redis, mysql, rabbitmq 等服务
#             pane-0: redis
#             pane-1
#         }
#     }
# }


SESSION_FISH = "fish"
SESSION_NODE = "node"
WIN_POOL = "pool"
WIN_NODE = "node"
WIN_SERVICE = "service"
WIN_MINER = "miner"

# 项目路径
POOL_DIR = "/home/node/data/pool/fish"
GATE_DIR = "/home/node/data/pool/gate"
COIN_DIR = "/home/node/data/pool/distribution"


def run_cmd(cmd: str):
    return subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)

def run_with_output(cmd: str):
    return subprocess.run(cmd, shell=True)


def check_call_cmd(cmd: str):
    subprocess.check_call(cmd, shell=True, stderr=subprocess.DEVNULL)


def kill_session(session: str):
    cmd = f"tmux kill-session -t {session}"
    output = run_cmd(cmd)
    if output.returncode != 0:
        print("session non-exist")
    else:
        print(f"session {session} killed")


def clear_tmux():
    cmd = "tmux kill-server"
    output = run_cmd(cmd)
    if output.returncode != 0:
        print("no tmux server")
    else:
        print("all tmux session killed")


def build_tmux():
    pool_tmux()
    middleware_tmux()
    node_tmux()
    print("tmux built")


def middleware_tmux():
    cmds = [
        f"tmux new-window -t {SESSION_FISH}:1 -n {WIN_SERVICE}",
        f'tmux rename-window -t {SESSION_FISH}:1 {WIN_SERVICE}'
        f"tmux splitw -h -p 50",
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print("middleware sevices tmux built")


def node_tmux():
    cmds = [
        f"tmux new-session -d -s {SESSION_NODE}",
        f"tmux rename-window -t {SESSION_NODE}:0 {WIN_NODE}",
        f"tmux splitw -h -p 50",
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print("node-tmux built")


def pool_tmux():
    cmds = [
        f"tmux kill-session -t {SESSION_FISH}",
        f"tmux new-session -d -s {SESSION_FISH}",
        f"tmux splitw -h -p 50",
        f"tmux splitw -v -p 70",
        f"tmux selectp -t 0",
        f"tmux splitw -v -p 50",
        f'tmux rename-window -t {SESSION_FISH}:0 {WIN_POOL}'
    ]

    for cmd in cmds:
        run_cmd(cmd)
    print("pool-tmux built")


def run_pool_modules():
    print("running pool modules")
    # run pool
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cd {POOL_DIR}" C-m',
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "fish-pool" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print("pool started")

    # run pool-gate
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.1 "cd {GATE_DIR}" C-m',
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.1 "pool-gate" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print("pool gate started")

    # run coin distribution
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.2 "cd {COIN_DIR}" C-m',
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.2 "coin-distribution" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print("coin distribution started")
    
def run_node():
    node_cmd = 'ironfish start -v --rpc.tcp.host=127.0.0.1 --rpc.tcp.port=14444 --rpc.tcp.secure --rpc.tcp'
    cmds = [
        f'tmux send-keys -t {SESSION_NODE}:{WIN_NODE}.0 "{node_cmd}" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print(Fore.GREEN + "node started")
    
def run_services():
    redis_cmd = 'redis-server'
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_SERVICE}.0 "{redis_cmd}" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print(Fore.GREEN + "redis started")
    

if __name__ == "__main__":
    kill_session(SESSION_FISH)
    kill_session(SESSION_NODE)

    build_tmux()
    run_pool_modules()
    run_node()
    run_services()