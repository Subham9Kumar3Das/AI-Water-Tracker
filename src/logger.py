import logging

logging.basicConfig(
    level=logging.INFO, 
    filename='app.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def log_message(message):
    logging.info(message)

def log_error(message):
    logging.error(message)