#!/usr/bin/env python3

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/user/app')

from influxdb import InfluxDBClient

HOST = 'pxl_influxdb'
PORT = 8086
DB_NAME = 'test_conn'

print("Connecting to Influx on " + HOST + ": " + str(PORT))

try:
    client = InfluxDBClient(host=HOST, port=PORT, database=DB_NAME)
    client.create_database(DB_NAME)
    client.switch_database(DB_NAME)
    print("connected")
except Exception as e:
    print("Exception when creating Influx DB client: " + str(e))

print("...end")
