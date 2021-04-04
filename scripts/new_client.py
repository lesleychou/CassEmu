from client_sender import ClientSender
from constant import QueryType
import time
import test
import sys
import math
import random
import string


# you should put the IPs of replicas in the hosts
hosts = ['155.98.39.45', '155.98.39.55', '155.98.39.46']
sender = ClientSender(hosts)
replica_num = 3


def replica_selection(latency_profile=None, req_id=None):
    '''
    You can select replica server based on the latency history of each replica for request req_id
    '''

    selected_req_id = req_id % 3
    return selected_req_id


def sys_main():
    '''
    In this example function, we send insert request to the replica servers in a round-robin way.
    '''

    for req_id in range(0, 20):

        # Prepare data to insert, You can replace the insert by any other operation you want.
        # In this example, we insert (y_id, field0) to the table
        random.seed(time.time())
        paras = [''.join(random.sample(string.ascii_letters + string.digits, 20)), '1']

        # send request
        sender.sendOneRequest(host=replica_selection(req_id=req_id), type=QueryType.INSERT, db_data=paras, req_id=req_id)
        # print latency for each request

    latency_array = sender.getLatencies()
    for i in latency_array:
        print('Latency for request' + str(i) + ':' + str(latency_array[i]))

    return 0


if __name__ == '__main__':
    sys_main()


