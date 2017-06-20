import threading
import argparse

from rpc.node import Node

parser = argparse.ArgumentParser(description="Lamport Mutex cli")
parser.add_argument("--pid", type=int, default=1)
parser.add_argument("--manual_mode", type=bool, default=False)    # main.py --pid 1 --manual_mode True
parser.add_argument("--stress_mode", type=bool, default=True)
parser.add_argument("--count", type=int, default=2)    # main.py --config --count 10
parser.add_argument("--config", default="config.txt")
args = parser.parse_args()

if args.stress_mode:
    nodes = []
    treads = []
    for i in range(args.count):
        n = Node(i, args.config)
        treads.append(threading.Thread(target=n.run))
    for t in treads:
        t.start()
    for t in treads:
        t.join()
else:
    n = Node(args.pid, args.config)
    t = threading.Thread(target=n.run, args=[True])
    t.start()
    t.join()
