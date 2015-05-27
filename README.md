# munin-couchbase-python
Munin plugin for Couchbase using python-requests

## Installation

Go to your /opt directory and clone this repository.
Once done, move to /etc/munin/plugins and execute the following command:

```bash
chmod +x /opt/munin-couchbase-python/couchbase_node.py
ln -s /opt/munin-couchbase-python/couchbase_node.py couchbase_node
```

## Munin-node configuration

Edit the file /etc/munin/plugin-conf.d/munin-node and add the following text:

```
[couchbase_]
user munin
env.host localhost
env.port 8091
env.username admin
env.password admin
```