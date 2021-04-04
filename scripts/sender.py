from cassandra import ProtocolVersion
from cassandra.cluster import Cluster
from  cassandra.policies import (HostFilterPolicy, RoundRobinPolicy, HostDistance)
from constant import QueryType
import constant
import random
import string
import time


class Sender:

    def __init__(self, host_address):
        self.host_address = host_address
        self.cluster = self.generateCluster()
        self.session = self.cluster.connect()
        self.ids = []
        self.session.set_keyspace(constant.KEY_SPACE)
        self.session.execute('use ' + constant.KEY_SPACE)

    def isAddressAccepted(self, host):
        return host.address == self.host_address

    def generateCluster(self):
        filter_policy = HostFilterPolicy(
            child_policy=RoundRobinPolicy(),
            predicate=self.isAddressAccepted
        )
        cluster = Cluster(
            [self.host_address],
            load_balancing_policy=filter_policy
        )
        return cluster


    def getSession(self):
        return self.session


    def executeRequest(self, type, callback, db_data, req_id):
        if (type == QueryType.READ):
            self.sendReadRequest(callback, db_data, req_id)
        elif (type == QueryType.SCAN):
            self.sendScanReqest(callback, db_data, req_id)
        elif (type == QueryType.UPDATE):
            self.sendUpdateReqest(callback, db_data, req_id)
        elif (type == QueryType.INSERT):
            self.sendInsertReqest(callback, db_data, req_id)


    def sendAsyncRequest(self, query, callback, req_id, param=None):

        future = self.session.execute_async(query, param)
        ResultHandler(future, callback, time.time(), req_id)

    def sendReadRequest(self, callback, db_data, req_id):
        query = constant.READ_query
        self.sendAsyncRequest(query=query, callback=callback, req_id=req_id, param=db_data)


    def sendScanReqest(self, callback, db_data, req_id):
        query = constant.SCAN_query
        self.sendAsyncRequest(query=query, callback=callback, req_id=req_id, param=db_data)


    def sendUpdateReqest(self, callback, db_data, req_id):
        query = constant.UPDATE_query
        self.sendAsyncRequest(query=query, callback=callback, req_id=req_id, param=db_data)

    def sendInsertReqest(self, callback, db_data, req_id):
        query = constant.INSERT_query
        self.sendAsyncRequest(query=query, callback=callback, req_id=req_id, param=db_data)

    def shutdown(self):
        self.cluster.shutdown()


class ResultHandler:
    def __init__(self, future, callback, start_time, req_id):
        self.callback = callback
        self.future = future
        self.start_time = start_time
        self.req_id = req_id
        self.future.add_callbacks(callback=self.handle_success, errback=self.handle_error)

    def handle_success(self, rows):
        self.callback(time.time() - self.start_time, self.req_id)
        self.callback(time.time() - self.start_time, self.req_id)

    def handle_error(self, exception):
        print(exception)
        self.callback(-1)
