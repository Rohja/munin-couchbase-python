#!/usr/bin/env python

import os
import sys
import requests

def display_config(config):
    ### OPS
    print "multigraph couchbase_ops"
    print "graph_title Couchbase Node Ops"
    print "graph_order ops"
    print "graph_args --base 1000"
    print "graph_vlabel Operations per \${graph_period}"
    print "graph_category db"
    print "graph_info This graph shows Operations/Sec for %s" % config['host']
    print ""
    print "ops.min 0"
    print "ops.label ops"
    print ""
    ### MEM_USED
    print "multigraph couchbase_memory_used"
    print "graph_title Couchbase Memory Used"
    print "graph_order mem"
    print "graph_args --base 1000"
    print "graph_category db"
    print ""
    print "mem.min 0"
    print "mem.label mem"
    print ""
    ### ITEMS
    print "multigraph couchbase_items"
    print "graph_title Couchbase Items Count"
    print "graph_order items"
    # print "graph_args --base 1000"
    print "graph_category db"
    print ""
    print "items.min 0"
    print "items.label items"
    print ""

def couchbase_node(config):
    url = "http://%s:%s/pools/default" % (config['host'], config['port'])
    r = requests.get(url, auth=(config['username'], config['password']))
    obj_data = r.json()
    #
    ops =        obj_data["nodes"][0]["interestingStats"]["ops"]
    print "multigraph couchbase_ops"
    print "ops.value", ops
    #
    mem_used =   obj_data["nodes"][0]["interestingStats"]["mem_used"]
    print "multigraph couchbase_memory_used"
    print "mem.value", mem_used
    #
    curr_items = obj_data["nodes"][0]["interestingStats"]["curr_items"]
    print "multigraph couchbase_items"
    print "items.value", int(curr_items)
    ####
    sys.exit(0)

if __name__ == "__main__":
    # Init config
    config = {'host':     os.environ.get('host',     '127.0.0.1'),
              'port':     os.environ.get('port',     '8091'),
              'username': os.environ.get('username', 'admin'),
              'password': os.environ.get('password', 'password'),}
              
    # Display config
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        display_config(config)
        sys.exit(0)
    couchbase_node(config)
