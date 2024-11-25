import json
import pandas as pd

from datetime import datetime, timedelta

from requests import get as rget

import os
from application_logger import ApplicationLogger

from influxdb import InfluxDBClient

from util import config

# Logger
logger = ApplicationLogger.create_rotating_file_logger_with_stdout(str(os.path.basename(__file__)).split(".")[0])

#
# ### Influx
#

CONFIG_SECTION = "INFLUX"
CONFIG_DB_NAMES = "db_names"
CONFIG_INFLUX_HOSTNAME = "influx_hostname"

# This class handles all InfluxDB communcations.
# Tables are hard coded, ports are patient specific.
# 
class InfluxHandler:
    def __init__(self):
        self.DB_NAMES = config.config_reader.get_list(CONFIG_SECTION, 
            CONFIG_DB_NAMES, 
            ["test"])
        self.influx_clients = {}
    
    def get_influx_client(self, port):
        if port not in self.influx_clients:
            try:
                logger.info('No influx client for port ' + str(port) + ' yet, creating new client')

                influx_hostname = config.config_reader.get(CONFIG_SECTION, CONFIG_INFLUX_HOSTNAME, "pxl_influxdb")
                new_client = InfluxDBClient(host=influx_hostname, port=port, database=self.DB_NAMES[0])

                [new_client.create_database(db_name) for db_name in self.DB_NAMES]

                # switch to sleep database by default
                new_client.switch_database(self.DB_NAMES[0])
                self.influx_clients[port] = new_client

                logger.info('New influx client created for port ' + str(port))
            except Exception as e:
                logger.error("Exception when creating Influx DB client: " + str(e))
                return None
            
        return self.influx_clients[port]

    def switch_database(self, port, db):
        try:
            logger.info("Switching to db " + db)
            client = self.get_influx_client(port)
            client.switch_database(db)
        except Exception as e:
            logger.error("Exception when switching to database " + db + ": " + str(e))
            return False
        return True

    def query_database(self, port, db, query):
        try:
            logger.info("Querying Influx DB: " + query)
            client = self.get_influx_client(port)
            result = client.query(query, database=db)
            logger.debug(result)
        except Exception as e:
            logger.error("Exception when querying Influx DB: " + str(e))
            return []
        return result

    def query_database_with_condition(self, port, db, query_prefix, variable, condition):
        try:
            query = query_prefix + ' WHERE ' + variable + ' = $condition'
            bind_params = {'condition': condition + ' 00:00:00'}

            logger.info("Querying Influx DB: " + query + " with params: " + str(bind_params))

            client = self.get_influx_client(port)
            result = client.query(query, bind_params=bind_params, database=db)
            logger.debug(result)
            return result
        except Exception as e:
            logger.error("Exception when querying Influx DB: " + str(e))
            return []

    def query_database_with_range(self, port, db, query_prefix, variable, start_date_str, end_date_str, end_time_str="00:00:00"):
        try:
            query = query_prefix + ' WHERE ' + variable + ' >= $start_time and ' + variable + ' <= $end_time'
            bind_params = {'start_time': start_date_str + ' 00:00:00', 'end_time': end_date_str + ' ' + end_time_str}

            logger.info("Querying Influx DB: " + query + " with params: " + str(bind_params))

            client = self.get_influx_client(port)
            result = client.query(query, bind_params=bind_params, database=db)
            logger.debug(result)
            return result
        except Exception as e:
            logger.error("Exception when querying Influx DB: " + str(e))
            return []

    def query_database_with_range_and_conditions(self, port, db, query_prefix, condition_variables, conditions, variable, start_date_str, end_date_str, end_time_str="00:00:00"):
        try:
            query = query_prefix + ' WHERE ('
            first = True
            bind_params = {}
            for condition_variable, condition in zip(condition_variables, conditions):
                # TODO: this solution is ugly as f*ck, 
                # but it's because sometimes the condition names have spaces in them
                condition_var_name = condition.replace(" ", "_")
                if first:
                    first = False
                    query = query + '"' + condition_variable + '" = $' + condition_var_name
                else:
                    query = query + ' OR ' + '"' + condition_variable + '" = $' + condition_var_name

                bind_params[condition_var_name] = condition
                    
            query = query + ") AND "
            query = query + variable + ' >= $start_time AND ' + variable + ' <= $end_time'
            bind_params['start_time'] = start_date_str + ' 00:00:00'
            bind_params['end_time'] = end_date_str + ' ' + end_time_str

            logger.info("Querying Influx DB: " + query + " with params: " + str(bind_params))

            client = self.get_influx_client(port)
            result = client.query(query, bind_params=bind_params, database=db)
            logger.debug(result)
            return result
        except Exception as e:
            logger.error("Exception when querying Influx DB: " + str(e))
            return []

    def write_to_db(self, port, db, points):
        try:
            #logger.info("Writing to Influx DB...")
            #logger.debug(points)

            client = self.get_influx_client(port)
            client.write_points(points, database=db)
            return True
        except Exception as e:
            logger.error("Exception when writing to Influx DB: " + str(e))
            return False

influx_handler = InfluxHandler()