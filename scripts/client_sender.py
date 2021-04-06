import random
import time
from sender import Sender


class ClientSender:

    def __init__(self, hosts):
        self.num_async_request = 0
        self.senders = {}
        self.latencies = {}
        self.latencies_array = []
        self.hosts = hosts
        self.host_queues = {}
        for host in hosts:
            self.senders[host] = Sender(host)
            self.host_queues[host] = []

    def executeQueryAsync(self, host, type, db_data, req_id):
        if host in self.hosts:
            self.num_async_request = self.num_async_request + 1
            self.host_queues[host].append(req_id)
            return self.senders[host].executeRequest(type, self.nonBlockCallback, db_data, req_id)

    def nonBlockCallback(self, time, req_id):
        self.latencies[req_id] = time
        self.latencies_array.append(time)
        for host in self.host_queues:
            # you might need an if to check if the req_id is in the host
            if str(req_id) in self.host_queues[host]:
                print(req_id, "###########remove here")
                self.host_queues[host].remove(str(req_id))

    def getLatencies(self):
        while len(self.latencies) < self.num_async_request:
            time.sleep(0.0001)
        return self.latencies

    def sendOneRequest(self, host, type, db_data, req_id):
        self.executeQueryAsync(host, type, db_data, req_id)

    def clearLatencyTable(self):
        self.latencies.clear()
        self.latencies_array.clear()
        self.num_async_request = 0

    def shutdown(self):
        self.clearLatencyTable()
        for host in self.hosts:
            self.senders[host].shutdown()
