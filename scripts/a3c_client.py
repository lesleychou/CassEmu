import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import matplotlib.pyplot as plt
import numpy as np
from load_balance_actor_agent import *
import tensorflow as tf
from param import *

from client_sender import ClientSender
from constant import QueryType
import time
import test
import sys
import math
import random
import string
import threading
import queue

# you should put the IPs of replicas in the hosts
hosts = ['10.52.1.99' ,'10.52.3.66' ,'10.52.3.5']
sender = ClientSender( hosts )
replica_num = 3

all_hosts_queue_size = {}
act = 0
shouldRun = True

my_queue = queue.Queue()
def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper

def find_shortest_queue_size(queue_size_dict):
    min_val = min( [len( queue_size_dict[ele] ) for ele in queue_size_dict] )
    for ele in queue_size_dict:
        if len( queue_size_dict[ele] ) == min_val:
            return ele

@storeInQueue
def run_client(data_sample, num_exp=100):
    # # set up environment
    # env = envs.make(args.env)
    global all_hosts_queue_size
    global act
    global shouldRun

    all_total_reward = []
    req_for_hosts = {}

    for s in hosts:
        req_for_hosts[s] = []
    start_time = time.time()
    # run experiment
    for req_id in range( 0 ,num_exp ):
        # Prepare data to insert, You can replace the insert by any other operation (e.g., READ, UPDATE) you want.
        # In this example, we insert (y_id, field0) to the table
        random.seed(100)
        # max key size 65555, max value size: 2GB (2e9)
        paras = data_sample[req_id]
        # print( 'Insert data:' )
        # send request
        all_hosts_queue_size = sender.host_queues
        print( all_hosts_queue_size )
        host_id = hosts[act]
        print( host_id ,"---selected_id" )
        req_for_hosts[host_id].append( req_id )

        sender.sendOneRequest( host=host_id ,type=QueryType.INSERT ,db_data=paras ,req_id=str( req_id ) )
        # print( sender.host_queues ,"----queues" )
        total_reward = 0

        # state = env.observe()
        # TODO: state = queue_size, 1

        all_total_reward.append( total_reward )
    shouldRun = False
    print( "--- %s seconds ---" % (time.time() - start_time) )

    return all_total_reward ,req_for_hosts


def run_rl_agent(agent):
    global all_hosts_queue_size
    global act
    global shouldRun

    while shouldRun:
        each_queue_lengths = {k: len( v ) for k ,v in all_hosts_queue_size.items()}
        state = list( each_queue_lengths.values() )
        state.append( 1 )

        act = agent.get_action( state )
        print(state, act, "---state, act")
        time.sleep(0.00001)


def main():
    # Performance monitoring
    # all_rl_mean = []

    sess = tf.Session()
    np.random.seed( args.seed )
    tf.set_random_seed( args.seed )

    # set up central session
    # set up actor agent in master thread
    actor_agent = ActorAgent( sess )

    # initialize model parameters
    sess.run( tf.global_variables_initializer() )

    # set up logging processes
    saver = tf.train.Saver( max_to_keep=args.num_saved_models )

    # load trained model
    if args.saved_model is not None:
        saver.restore( sess ,args.saved_model )

    # for i in np.arange( 100 ,5100 ,500 ):
    #     args.job_size_max = i

    # ---- start testing process ----
    chars = string.ascii_letters + string.digits
    data_sample = []
    for i in range( 100 ):
        data_sample.append( [''.join( random.choice( chars ) for _ in range( 6000 ) ) ,
                             ''.join( random.choice( chars ) for _ in range( int( 1000 ) ) )] )

    t1 = threading.Thread( target=run_client, args=(data_sample,) )
    t2 = threading.Thread( target=run_rl_agent, args=(actor_agent,) )
    # creating two threads here t1 & t2
    t1.start()
    t2.start()
    # starting threads here parallel by using start function.
    # t1.join()
    # # this join() will wait until the cal_square() function is finished.
    # t2.join()
    # this join() will wait unit the cal_cube() function is finished.

    test_result ,req_for_hosts = my_queue.get()
    #test_mean = np.mean( test_result )
    # all_rl_mean.append(test_mean)

    print( 'Here is latency:' )
    latency_array = sender.getLatencies()
    # time.sleep(10)
    latency_each_host = dict.fromkeys( (req_for_hosts) ,0 )
    for i in req_for_hosts:
        for n in req_for_hosts[i]:
            latency_value = latency_array[str( n )]
            latency_each_host[i] += latency_value
    print( latency_each_host )
    # print( test_mean ,"------rl, baseline" )
    # sess.close()

    # print(all_rl_mean)


if __name__ == '__main__':
    main()
