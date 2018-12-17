import os
import datetime
from config_ini import Config
from LogFile import logger
# current_day = datetime.datetime.now().day
# current_month = datetime.datetime.now().month
# current_year = datetime.datetime.now().year

c = Config()


def year_creation():
    current_year = c.section_value[3] + str(datetime.datetime.now().year) + "/"
    if not os.path.exists(current_year):
        os.mkdir(current_year)
    else:
        logger.info("{} Directory already exists".format(current_year))

    return current_year


def month_creation():
    current_month = "{}-{}".format(str(datetime.datetime.now().year), str(datetime.datetime.now().
                                                                                            month-1)) + "/"
    if not os.path.exists(current_month):
        os.mkdir(current_month)
    else:
        logger.info("{} Directory already exists")

    return current_month

