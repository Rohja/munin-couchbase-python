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

def config_cache_miss(entries):
    print "multigraph couchbase_bucket_cache_miss"
    print "graph_title Couchbase Cache Miss for buckets"
    print "graph_order cache"
    # print "graph_args --base 1000"
    print "graph_vlabel Entry red from disk instead of cache"
    print "graph_category db"
    print "graph_info This graph shows the amount of entry red from the disk instead of the cache"
    print ""
    for entry in entries:
        print "%s.min 0" % entry['name']
        print "%s.label count (%s/%s)" % (entry['name'], entry['name'], entry["bucketType"])
    print ""

def config_diskqueue_drain(entries):
    print "multigraph couchbase_bucket_diskqueue_drain"
    print "graph_title Couchbase Disk Queue Drain for buckets"
    print "graph_order queue"
    # print "graph_args --base 1000"
    print "graph_vlabel Disk operations pending in queue"
    print "graph_category db"
    print "graph_info This graph shows the amount of entry waiting in queue to be wrote on disk"
    print ""
    for entry in entries:
        print "%s.min 0" % entry['name']
        print "%s.label operations (%s/%s)" % (entry['name'], entry['name'], entry["bucketType"])
    print ""

def display_config(config):
    obj_data = get_buckets_infos(config)
    #
    config_cache_miss(obj_data)
    config_diskqueue_drain(obj_data)
###
# VALUES DISPLAY
###

def display_cache_miss(config, entries):
    print "multigraph couchbase_bucket_cache_miss"
    for entry in entries:
        name = entry['name']
        bucket = get_bucket_infos(config, name)
        rate_list = bucket['op']['samples']['ep_cache_miss_rate']
        val = calc_average_list(rate_list)
        print "%s.value" % name, val
    print ""

def display_diskqueue_drain(config, entries):
    print "multigraph couchbase_bucket_diskqueue_drain"
    for entry in entries:
        name = entry['name']
        bucket = get_bucket_infos(config, name)
        rate_list = bucket['op']['samples']['ep_diskqueue_drain']
        val = calc_average_list(rate_list)
        print "%s.value" % name, val
    print ""
    

###
# MAIN
###

def couchbase_buckets(config):
    obj_data = get_buckets_infos(config)
    #
    display_cache_miss(config, obj_data)
    display_diskqueue_drain(config, obj_data)

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

