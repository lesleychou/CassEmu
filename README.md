# Cassandra Client

## Environment
Clean Ubuntu 18.04

## Installation
### Java8

    sudo apt-get update
    printf "Y" | sudo apt-get install software-properties-common
    printf "\n" | sudo add-apt-repository ppa:webupd8team/java
    sudo apt-get update
    sudo apt install openjdk-8-jdk openjdk-8-jre

### Cassandra's Python Client
    sudo dpkg-reconfigure dash
    sudo apt-get install python3-tk
    sudo apt-get update
    bash
    export LC_ALL=C
    sudo apt-get install python3-pip
    pip3 install cassandra-driver
    pip3 install Faker
    pip3 install datetime
  
### Get Cassandra Database (on client and replicas)
    cd /tmp/
    git clone https://github.com/hyperpro/CassSelect.git
    
    #client 1
    cd /tmp/CassSelect/cassandra-3.9/
    cp conf/cassandra1.yaml conf/cassandra.yaml
    cd bin
    sudo chmod 777 cassandra
    cd /tmp/CassSelect/cassandra-3.9/bin
    ./cassandra -f

    #client 2
    cd /tmp/CassSelect/cassandra-3.9/
    cp conf/cassandra2.yaml conf/cassandra.yaml
    cd bin
    sudo chmod 777 cassandra
    cd /tmp/CassSelect/cassandra-3.9/bin
    ./cassandra -f
    
    #client 3
    cd /tmp/CassSelect/cassandra-3.9/
    cp conf/cassandra3.yaml conf/cassandra.yaml
    cd bin
    sudo chmod 777 cassandra
    cd /tmp/CassSelect/cassandra-3.9/bin
    ./cassandra -f

### Cassndra Interface
    cd /tmp/CassSelect/cassandra-3.9/bin
    chmod 777 cqlsh
    ./cqlsh $thisIP 


## How to use

### Setup KeySpace
In Cassandra interface, we set

    create keyspace ycsb with replication = {'class':'SimpleStrategy', 'replication_factor':3};
    use ycsb;
    create table usertable (y_id varchar primary key,field0 varchar);


## Run experiments

Run a full experiment

    python3 new_client.py
    
You can see the terminal prints out the latency for the example requests.


