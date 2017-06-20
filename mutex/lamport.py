class PriorityQueue(list):
    def append(self, obj):
        super().append(obj)
        self.sort()


class LamportMutex:
    def __init__(self, node):
        self.node = node
        self.is_running = False
        self.pending_replies = []
        self.requests = PriorityQueue()

    def request(self, msg):
        self.requests.append(msg)

    def release(self, msg=None):
        if msg is None:
            self.is_running = False
            self.requests = self.requests[1:]
        elif self.requests and self.requests[0].from_pid == msg.from_pid:
            self.requests = self.requests[1:]

    def try_acquire(self):
        if not self.is_running:
            self.is_running = True
            self.pending_replies = self.node.pids[:]
            self.node.multicast('request')
        if self.requests and self.requests[0].from_pid == self.node.pid:
            if len(self.pending_replies) == 0:
                return True
        return False

    def reply_request(self):
        if self.is_running:
            self.pending_replies.pop()
