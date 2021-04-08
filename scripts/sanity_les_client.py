from client_sender import ClientSender
from constant import QueryType
import time
import test
import sys
import math
import random
import collections
import string

# you should put the IPs of replicas in the hosts
hosts = ['10.52.1.99' ,'10.52.3.66' ,'10.52.3.5']
sender = ClientSender( hosts )
replica_num = 3


def replica_selection(queue_size_dict=None ,req_id=None):
    '''
    You can select replica server based on the latency history of each replica for request req_id
    '''
    # selected_req_id = req_id % 3
    # host = hosts[selected_req_id]
    # host = find_shortest_queue_size( queue_size_dict )
    host = hosts[0]
    return host


def find_shortest_queue_size(queue_size_dict):
    min_val = min( [len( queue_size_dict[ele] ) for ele in queue_size_dict] )
    for ele in queue_size_dict:
        if len( queue_size_dict[ele] ) == min_val:
            return ele


def sys_main():
    '''
    In this example function, we send insert request to the replica servers in a round-robin way.
    '''

    chars = string.ascii_letters + string.digits
    data_sample = []
    for i in range( 1000 ):
        data_sample.append( [''.join( random.choice( chars ) for _ in range( 6000 ) ) ,
                             ''.join( random.choice( chars ) for _ in range( int( 10000 ) ) )] )
    req_for_hosts = {}
    host_id = '10.52.1.99'

    for s in hosts:
        req_for_hosts[s] = []

    plot_queue = {}
    plot_delay = []

    start_time = time.time()
    for req_id in range( 0 ,1000):
        curr_time = time.time()
        # Prepare data to insert, You can replace the insert by any other operation (e.g., READ, UPDATE) you want.
        # In this example, we insert (y_id, field0) to the table
        random.seed(100 )
        # max key size 65555, max value size: 2GB (2e9)
        paras = data_sample[req_id]
        print( 'Insert data:' )
        # print(paras)
        # send request
        # decision_interval = 0.00001
        queue_value = sender.host_queues['10.52.1.99']
        plot_queue[str(req_id)]=len(queue_value)
        #print(queue_value, "-------queue size")
        #if (time.time() - curr_time) >= decision_interval:
        host_id = replica_selection( queue_size_dict=sender.host_queues ,req_id=req_id )

        print( host_id ,"---selected_id" )
        req_for_hosts[host_id].append( req_id )

        sender.sendOneRequest( host=host_id ,type=QueryType.INSERT ,db_data=paras ,req_id=str( req_id ) )
        time.sleep(0.0001)
        # print(sender.host_queues, "----queues")
    print( "--- %s seconds ---" % (time.time() - start_time) )

    #print( req_for_hosts )
    # print latency for each request. You can use this data to build latency profile for each replica server
    print( 'Here is latency:' )
    latency_array = sender.getLatencies()
    queue_log = {k: plot_queue[k] for k in sorted(plot_queue.keys())[200:]}
    latency_log = collections.OrderedDict(sorted(latency_array.items()))
    latency_log = {k: latency_log[k] for k in sorted(latency_log.keys())[200:]}
    print(queue_log)
    print(latency_log)
    # time.sleep(10)
    # latency_each_host = dict.fromkeys( (req_for_hosts) ,0 )
    # for i in req_for_hosts:
    #     for n in req_for_hosts[i]:
    #         latency_value = latency_array[str( n )]
    #         latency_each_host[i] += latency_value
    # print( latency_each_host )
    return 0


if __name__ == '__main__':
    sys_main()
