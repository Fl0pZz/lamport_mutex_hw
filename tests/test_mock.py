import unittest

from clock.clock import Clock
from mutex.lamport import LamportMutex
from rpc.message import Message


class MockNode:
    def __init__(self, pid):
        self.nodes = {}
        self.pid = pid
        self.pids = []
        self.logic_time = Clock()
        self.mutex = LamportMutex(self)

    def service(self, msg):
        self.logic_time.update(msg.time)
        if msg.type == 'request':
            self.send_to(msg.from_pid, 'reply')
        elif msg.type == 'release':
            self.mutex.release(msg)
        elif msg.type == 'reply':
            self.mutex.reply_request()

    def send_to(self, to, type):
        if type == 'reply':
            self.logic_time.increment()
        msg = Message(to, self.pid, self.logic_time.time, type)

        if type == 'request' and to == self.pid:
            self.mutex.request(msg)
        else:
            self.nodes[to].service(msg)

    def multicast(self, type):
        self.logic_time.increment()
        if type == 'request':
            self.send_to(self.pid, type)
        for pid in self.nodes.keys():
            if pid != self.pid:
                self.send_to(pid, type)


class LMTests(unittest.TestCase):
    def test_single(self):
        n = MockNode(1)
        self.assertTrue(n.mutex.try_acquire())
        self.assertEqual(n.logic_time.time, 1)
        n.mutex.release()
        n.multicast("release")
        self.assertEqual(n.logic_time.time, 2)

    def test_multi(self):
        nodes = {0: MockNode(0), 1: MockNode(1)}
        nodes[0].nodes = nodes
        nodes[1].nodes = nodes
        nodes[0].pids = [1]
        nodes[1].pids = [0]
        self.assertTrue(nodes[0].mutex.try_acquire())
        self.assertEqual(nodes[0].logic_time.time, 4)
        self.assertEqual(nodes[1].logic_time.time, 3)
        nodes[0].mutex.release()
        nodes[0].multicast("release")
        self.assertTrue(nodes[0].mutex.try_acquire())
        self.assertEqual(nodes[0].logic_time.time, 9)
        self.assertEqual(nodes[1].logic_time.time, 8)


if __name__ == '__main__':
    unittest.main()
