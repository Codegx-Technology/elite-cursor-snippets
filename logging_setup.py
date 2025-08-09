import logging
import os
from logging.handlers import RotatingFileHandler
from config_loader import get_config

def setup_logging():
    config = get_config().logging

    # Create logs directory if it doesn't exist
    logs_dir = os.path.dirname(config.log_file)
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(config.level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # File Handler
    file_handler = RotatingFileHandler(
        config.log_file,
        maxBytes=config.max_bytes,
        backupCount=config.backup_count
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Stream Handler (console output)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    # Prevent duplicate logs from imported modules
    root_logger.propagate = False

def get_logger(name):
    return logging.getLogger(name)

# Setup logging when the module is imported
setup_logging()
