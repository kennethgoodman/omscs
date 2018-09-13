#!/usr/bin/python

import sys
from Topology import *
from Node import *
from helpers import *
from validate_answers import run_validation
import os

files = os.listdir('Topologies')

for file in files:
    if "." == file[0]:
        continue
    print("running {}".format(file))
    try:
        file, _ = file.split(".")
        # Start up the logfile
        open_log('MyAnswers/{}.log'.format(file), should_print_it=False)
        # Populate the topology
        topo = Topology('Topologies/{}.txt'.format(file))
        # Run the topology.
        topo.run_topo()
        # Close the logfile
        finish_log()
    except Exception as e:
        print(e)
run_validation()
