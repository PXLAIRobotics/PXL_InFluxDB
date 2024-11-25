#!/usr/bin/env python3

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/user/app')

from influx_handler import influx_handler

HOST = 'pxl_influxdb'
PORT = 8086

DB = ""
TABLE = ""

START_DATE = ""
END_DATE = ""


def query():
    print("Quering Influx...")
    query_result = influx_handler.query_database_with_range(PORT, DB, 'SELECT * FROM "' + TABLE + '"', "time", START_DATE, END_DATE)
        
    data = {
        "data": list(query_result.get_points(measurement=TABLE))
    }
    print("Returning data from Influx...")
    print(data)


# INITIAL QUERY
query()


print("...end")
