import configparser

import os
from application_logger import ApplicationLogger

# Logger
logger = ApplicationLogger.create_rotating_file_logger_with_stdout(str(os.path.basename(__file__)).split(".")[0])

class ConfigReader():
    def __init__(self):
        self.config_reader = configparser.ConfigParser()
        self.config_reader.read("/home/user/app/util/config.ini")

        # print("#########################################")
        # print(self.config_reader.sections())

        # for x in self.config_reader["STEPS"]:
        #     print(x)


    # If the field is in the DEFAULT section, return this
    # Else return the given default value
    def get(self, section, field, default_value):
        try:
            if not self.config_reader.has_section(section):
                logger.warning("Section: " + section + " not found in config, reverting to DEFAULT section")
                value = self.config_reader.get("DEFAULT", field)
                logger.warning("DEFAULT section value: " + value)
                return value
            else:
                value = self.config_reader.get(section, field)
                logger.info("(" + section + "," + field + "): " + value)
                return value
        except Exception as e:
            logger.error(e)
            logger.warning("Field: " + field + " not found in config, returning default value: " + str(default_value))
            return default_value

    def get_int(self, section, field, default_value):
        value = self.get(section, field, default_value)
        return int(value)

    # Return jsonified list representation of the value string
    def get_list(self, section, field, default_value):
        value = self.get(section, field, default_value)
        
        if type(value) == str:
            lis = value.split(",")
            return lis
        else:
            return value


config_reader = ConfigReader()