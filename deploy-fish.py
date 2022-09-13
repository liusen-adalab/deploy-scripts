import subprocess


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
#         window-middleware { // 运行 redis, mysql, rabbitmq 等中间件
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
POOL_DIR = ""
COIN_DIR = ""


def run_cmd(cmd: str):
    return subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)


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


def middleware_tmux():
    cmds = [
        f"tmux new-window -t {SESSION_FISH}:1 -n {WIN_SERVICE}",
        f"tmux splitw -h -p 50",
    ]
    for cmd in cmds:
        run_cmd(cmd)


def node_tmux():
    cmds = [
        f"tmux new-session -d -s {SESSION_NODE}",
        f"tmux rename-window -t {SESSION_NODE}:0 {WIN_NODE}",
        f"tmux splitw -h -p 50",
    ]
    for cmd in cmds:
        run_cmd(cmd)


def pool_tmux():
    cmds = [
        f"tmux kill-session -t {SESSION_FISH}",
        f"tmux new-session -d -s {SESSION_FISH}",
        f"tmux splitw -h -p 50",
        f"tmux splitw -v -p 70",
        f"tmux selectp -t 0",
        f"tmux splitw -v -p 50",
    ]

    for cmd in cmds:
        run_cmd(cmd)


def run_pool():
    # run pool
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cd {POOL_DIR}" C-m',
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cargo run fish-pool --release" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)

    # run pool-gate
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cd {POOL_DIR}" C-m',
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cargo run pool-gate --release" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)

    # run coin distribution
    cmds = [
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cd {COIN_DIR}" C-m',
        f'tmux send-keys -t {SESSION_FISH}:{WIN_POOL}.0 "cargo run --release" C-m',
    ]
    for cmd in cmds:
        run_cmd(cmd)

    