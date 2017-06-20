import fcntl
import random
import socket
import time

from clock.clock import Clock
from configutation.reader import сonfig_reader
from logs.loggercreater import setup_logger
from mutex.lamport import LamportMutex
from rpc.message import Message
from rpc.nodelistener import NodeListenerThread
from rpc.serializer import serialize


class Node:
    def __init__(self, pid, configfile):
        self.nodes = сonfig_reader(configfile)
        self.pid = pid
        self.pids = [pid for pid in self.nodes.keys() if pid != self.pid]
        self.address = self.nodes[pid][0]
        self.port = self.nodes[pid][1]
        self.logic_time = Clock()
        self.logger = setup_logger('node#{}_logger'.format(self.pid), "logs/node{}.log".format(self.pid))
        self.mutex = LamportMutex(self)
        NodeListenerThread(self).start()

    def run(self, manual_mode=False):

        time.sleep(2)
        while True:
            if manual_mode:
                input('Press enter to continue')
            self.logger.info("{} {} {} {}".format('request', round(time.time(), 5), self.logic_time.time, self.pid))
            while not self.mutex.try_acquire():
                time.sleep(random.randint(1, 50) / 10.)
                self.logger.info("{} {} {} {}".format('request', round(time.time(), 5), self.logic_time.time, self.pid))
            logic_time = self.logic_time.time
            self.logger.info("{} {} {} {}".format('acquire', round(time.time(), 5), self.logic_time.time, self.pid))
            with open('logs/mutex.txt', 'a') as f:
                try:
                    fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    f.write("{} {} {}\n".format(self.pid, logic_time, self.logic_time.time))
                except IOError:
                    print('error')
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
            self.mutex.release()
            self.multicast("release")
            self.logger.info("{} {} {} {}".format('release', round(time.time(), 5), self.logic_time.time, self.pid))

    def service(self, msg):
        self.logic_time.update(msg.time)
        if msg.type == 'request':
            self.send_to(msg.from_pid, 'reply')
        elif msg.type == 'release':
            self.mutex.release(msg)
        elif msg.type == 'reply':
            self.mutex.reply_request()

    def send_to(self, to, type):
        msg = Message(to, self.pid, self.logic_time.time, type)
        if type == 'reply':
            self.logic_time.increment()

        if type == 'request' and to == self.pid:
            self.mutex.request(msg)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect(self.nodes[to])
                data = serialize(msg)
                sock.send(data)
            finally:
                sock.close()

    def multicast(self, type):
        self.logic_time.increment()
        if type == 'request':
            self.send_to(self.pid, type)
        for pid in self.nodes.keys():
            if pid != self.pid:
                self.send_to(pid, type)
