#!/bin/bash

# clean
sudo mn -c

# launch ryu controller
ryu-manager ryu_controller_ddos.py --observe-links &

# Sleep so RYU controller have time to start
sleep 2

# launch topology and servers
sudo python2 network_topology.py