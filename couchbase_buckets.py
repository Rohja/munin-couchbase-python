#!/usr/bin/env python

import os
import sys
import requests

###
# TOOLS
###

def get_buckets_infos(config):
    url = "http://%s:%d/pools/default/buckets" % (config['host'], config['port'])
    r = requests.get(url, auth=(config['username'], config['password']))
    obj_data = r.json()
    return obj_data

def get_bucket_infos(config, name):
    url = "http://%s:%d/pools/default/buckets/%s/stats" % (config['host'], config['port'], name)
    r = requests.get(url, auth=(config['username'], config['password']))
    obj_data = r.json()
    return obj_data

def calc_average_list(data):
    icount = len(data)
    vcount = 0
    for e in data:
        vcount += float(e)
    val = vcount / icount
    return val

###
# CONFIG DISPLAY
###

def config_cache_miss(entry):
    print "multigraph couchbase_bucket_cache_miss_%s" % entry['name']
    print "graph_title Couchbase Cache Miss for bucket %s (%s)" % (entry['name'], entry["bucketType"])
    print "graph_order cache"
    # print "graph_args --base 1000"
    print "graph_vlabel Entry red from disk instead of cache"
    print "graph_category db"
    print "graph_info This graph shows the amount of entry red from the disk instead of the cache"
    print ""
    print "cache.min 0"
    print "cache.label count"
    print ""

def config_diskqueue_drain(entry):
    print "multigraph couchbase_bucket_diskqueue_drain_%s" % entry['name']
    print "graph_title Couchbase Disk Queue Drain for bucket %s (%s)" % (entry['name'], entry["bucketType"])
    print "graph_order queue"
    # print "graph_args --base 1000"
    print "graph_vlabel Disk operations pending in queue"
    print "graph_category db"
    print "graph_info This graph shows the amount of entry waiting in queue to be wrote on disk"
    print ""
    print "queue.min 0"
    print "queue.label operations"
    print ""

def display_config(config):
    obj_data = get_buckets_infos(config)
    #
    for entry in obj_data:
        config_cache_miss(entry)
        config_diskqueue_drain(entry)
###
# VALUES DISPLAY
###

def display_cache_miss(entry, name):
    rate_list = entry['op']['samples']['ep_cache_miss_rate']
    val = calc_average_list(rate_list)
    print "multigraph couchbase_bucket_cache_miss_%s" % name
    print "cache.value", val
    print ""

def display_diskqueue_drain(entry, name):
    rate_list = entry['op']['samples']['ep_diskqueue_drain']
    val = calc_average_list(rate_list)
    print "multigraph couchbase_bucket_diskqueue_drain_%s" % name
    print "queue.value", val
    print ""
    

###
# MAIN
###

def couchbase_buckets(config):
    obj_data = get_buckets_infos(config)
    #
    #
    for entry in obj_data:
        entry_obj = get_bucket_infos(config, entry['name'])
        # for i in entry_obj["op"]["samples"].keys():
        #     print "-", i
        # break
        display_cache_miss(entry_obj, entry['name'])

if __name__ == "__main__":
    # Init config
    config = {'host':     os.environ.get('host',     '127.0.0.1'),
              'port':     os.environ.get('port',      8091),
              'username': os.environ.get('username', 'admin'),
              'password': os.environ.get('password', 'password'),}
              
    # Display config
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        display_config(config)
        sys.exit(0)
    couchbase_buckets(config)

