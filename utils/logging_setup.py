# logging_setup.py
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name='sentiment_analysis_logger', log_file='logs/sentiment_analysis.log', level=logging.INFO):
    """Setup a shared logger."""
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Check if the logger already has handlers to avoid adding them multiple times
    if not logger.handlers:
        # Create a file handler that logs to a specific file
        handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        
        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # Add the handler to the logger
        logger.addHandler(handler)
    
    return logger
