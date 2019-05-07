# coding=utf-8

"""
logging Class
"""
import logging
from Classes.DataReaders.config_ini import Config
c = Config()

logger = logging.getLogger('{}'.format('App'))
logger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler which logs even debug messages
fh = logging.FileHandler('/home/groupm/mediaops-project/mediaops/logfolder/logfile.log')
fh.setLevel(logging.ERROR)
fh.setFormatter(formatter)
logger.addHandler(fh)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)



