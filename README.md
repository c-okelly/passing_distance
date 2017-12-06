# passing_distance
Gather data on the passing distance of vehicles from a bicycle.

This code should proivde the ability to run one or more sensors that aim to gather a varity of data on passing distance of vehicles and other road data.

# Running the code

The code can be run be excuting the run file in bin/

This will first check the the correct libraries are installed and then run the main for this folder. Defailt configuraiton of sensors and their revlevent pins is explained below.

This will output collected data into data/ and output and related logs into logs/

# Configuring 

The current configuration has a single echo sensor connected to the 16 (TRIG), 19 (ECHO) pins for a raspberry pi. 

# Overview

Tha main collection code is executed from passing_distance/main.py
