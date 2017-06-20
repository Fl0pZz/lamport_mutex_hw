class Message:
    def __init__(self, to_pid, from_pid, time, type):
        self.type = type
        self.time = time
        self.to_pid = to_pid
        self.from_pid = from_pid

    def __lt__(self, other):
        if self.time > other.time:
            return False
        elif self.time < other.time:
            return True
        elif self.from_pid > other.from_pid:
            return False
        else:
            return True

    def __str__(self):
        return "{} {}".format(self.from_pid, self.time)
