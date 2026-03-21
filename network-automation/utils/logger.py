import logging
from pathlib import Path
from datetime import datetime

def setup_logger(module_name):
    """Set up and return a logger that writes to both console and timestamped file."""
    # Ensure logs directory exists at project root
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"{module_name}_{timestamp}.log"
    
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    
    # Avoid attaching multiple handlers if called multiple times in a session
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        
        console_handler = logging.StreamHandler()
        # Keep console slightly cleaner
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    return logger
