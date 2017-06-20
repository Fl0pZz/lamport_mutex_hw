class Clock:
    def __init__(self):
        self.time = 0

    def increment(self):
        self.time += 1

    def update(self, clock):
        self.increment()
        self.time = max(self.time, clock + 1)
