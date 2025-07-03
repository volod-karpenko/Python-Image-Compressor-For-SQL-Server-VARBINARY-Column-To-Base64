import logging

def setup_logger(level = logging.INFO):
    logging.basicConfig(
        filename='logs.log',             
        filemode='a',                   
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        level=level
    )