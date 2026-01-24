# ==========================================
# BACKEND - backend/app/utils/logger.py
# ==========================================
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..config import get_settings

def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a logger with both file and console handlers.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    settings = get_settings()
    logger = logging.getLogger(name)
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Create logs directory
    log_file = Path(settings.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger