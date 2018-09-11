#!/usr/bin/python

# Project 3 for CS 6250: Computer Networks
#
# This how you run the topology and have it execute the Bellman-Ford algorithm.
# Generically, it is run as follows:
#     python run_topo.py <topology_file> <log_file>
# For instance, to run topo1.py and log to topo1.log that we created, use the following:
#     python run_topo.py topo1 topo1.log
# Note how the topology file doesn't have the .py extension.
#
# Students should not modify this file.
#
# Copyright 2015 Sean Donovan


import sys
from Topology import *
from Node import *
from helpers import *
from validate_answers import run_validation

# if len(sys.argv) != 3:
#     print("Syntax:")
#     print("    python run_topo.py <topology_file> <log_file>")
#     exit()

import os
files = os.listdir('.')
files = list(filter(lambda f: 'Topo.txt' in f, files)) + ['SimpleNegativeCycle.txt']

for file in files:
    print("running {}".format(file))
    try:
        file, _ = file.split(".")
        # Start up the logfile
        open_log('MyAnswers/{}.log'.format(file))
        # Populate the topology
        topo = Topology('Topologies/{}.txt'.format(file))
        # Run the topology.
        topo.run_topo()
        # Close the logfile
        finish_log()
    except Exception as e:
        print(e)
run_validation()