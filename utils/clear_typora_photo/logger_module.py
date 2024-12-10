# logger_module.py

import logging
from datetime import datetime

class Logger:
    def __init__(self, save_log=True, log_file='logfile.log', log_level=logging.INFO):
        self.save_log = save_log
        
        if self.save_log:
            # Create a timestamped log file
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Get milliseconds
            self.log_file = f"logfile_{timestamp}.log"
            logging.basicConfig(
                filename=self.log_file,
                level=log_level,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            logging.info("Logger initialized.")
        else:
            # Set up logging to console
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            logging.info("Logger initialized. Logging to console.")


    def info(self, message):
        """Log an info message."""
        logging.info(message)


    def warning(self, message):
        """Log a warning message."""
        logging.warning(message)


    def error(self, message):
        """Log an error message."""
        logging.error(message)


    def debug(self, message):
        """Log a debug message."""
        logging.debug(message)


    def critical(self, message):
        """Log a critical message."""
        logging.critical(message)


    def get_log_file(self):
        """Return the name of the log file if logging to file."""
        if self.save_log:
            return self.log_file
        else:
            return None
        # return self.log_file if self.save_log else None