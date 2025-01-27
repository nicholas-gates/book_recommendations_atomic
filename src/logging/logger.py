import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict, Any
import json
from datetime import datetime
import pytz

class Logger:
    def __init__(self, name: str = __name__, log_file: str = 'app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Configure Eastern Time zone
        self.tz = pytz.timezone('America/New_York')

        # Setup file handler with rotation
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024*1024*5,  # 5MB
            backupCount=3
        )

        # Custom formatter that just uses the message (since we're logging JSON)
        file_handler.setFormatter(logging.Formatter('%(message)s'))

        self.logger.addHandler(file_handler)

    def log(self,
            log_level: str = 'info',
            message: str = '',
            json_data: Optional[Dict[str, Any]] = None) -> None:

        # Validate log level
        if log_level.lower() not in ['debug', 'info', 'error']:
            raise ValueError(f"Invalid log level: {log_level}")

        # Create log entry structure
        log_entry = {
            "date": datetime.now(self.tz).strftime('%Y-%m-%d %H:%M:%S:%f')[:-3],
            "log_level": log_level.upper(),
            "msg": message,
            "data": json_data if json_data else None
        }

        # Convert to JSON string with proper formatting
        json_log = json.dumps(log_entry, ensure_ascii=False, indent=2, sort_keys=True)

        # Log with appropriate level
        if log_level.lower() == 'debug':
            self.logger.debug(json_log)
        elif log_level.lower() == 'info':
            self.logger.info(json_log)
        elif log_level.lower() == 'error':
            self.logger.error(json_log)