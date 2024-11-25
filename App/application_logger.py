import os
import logging
from logging.handlers import RotatingFileHandler
import configparser

class ApplicationLogger:
    @classmethod
    def create_rotating_file_logger_with_stdout(cls, script_name):   
        # Get logging level from config
        config_reader = configparser.ConfigParser()
        config_reader.read("/home/user/app/util/config.ini")
        LEVEL = config_reader.get("LOGGING", "level")
        STREAM_LEVEL = config_reader.get("LOGGING", "stream_level")
        LOG_FILE_DIR = config_reader.get("LOGGING", "log_file_dir")

        logger      = logging.getLogger(script_name)
        log_format  = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Override with environment variable if it exists
        level_env = os.getenv('PXL_INFLUX_LOG_LEVEL')
        if level_env:
            LEVEL = level_env

        print("-------------------- GENERAL DEBUG LEVEL --------------------")
        print(level_env)
        print("-----------------------------------------------------")

        if LEVEL == "INFO":
            logger.setLevel(logging.INFO)
        elif LEVEL == "ERROR":
            logger.setLevel(logging.ERROR)
        else:
            logger.setLevel(logging.DEBUG)
        

        # Configure a rotating logger 
        log_file   = os.path.join(LOG_FILE_DIR, script_name + ".log")
        rotating_file_handler = RotatingFileHandler(log_file, mode="w", maxBytes=1000000 * 10, backupCount=7, encoding=None, delay=0)
        rotating_file_handler.setFormatter(log_format)
        rotating_file_handler.setLevel(logging.DEBUG)  # Levels: DEBUG < INFO < WARNING < ERROR
        
        logger.addHandler(rotating_file_handler)
        

        # Also print to stdout
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_format)


        print("-------------------- STREAM DEBUG LEVEL --------------------")
        print(level_env)
        print("-----------------------------------------------------")

        if STREAM_LEVEL == "INFO":
            stream_handler.setLevel(logging.INFO)
        elif STREAM_LEVEL == "ERROR":
            stream_handler.setLevel(logging.ERROR)
        else:
            stream_handler.setLevel(logging.DEBUG)

        logger.addHandler(stream_handler)

        return logger
