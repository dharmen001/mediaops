# !/usr/bin/python
# coding=utf-8

import pandas as pd
import datetime
from Classes.DataReaders.config_ini import Config
from Classes.LoggerFile.LogFile import logger


class NdpData(Config):
    def __init__(self):
        super(NdpData, self).__init__()
        now = datetime.datetime.now()
        last_month = now.month-1 if now.month > 1 else 12
        last_year = now.year if now.month > 1 else now.year - 1

        self.path = self.section_value[10] + "Data Audit_GDS_All_Markets-{}-{:02d}.xlsx".format(last_year, last_month)

        logger.info("Start creating NDPFile at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        self.writer_file = pd.ExcelWriter(self.path, engine="xlsxwriter", datetime_format="YYYY-MM-DD")

    def save_and_close_writer(self):
        """
        To finally Save and close file
        :return: Nothing
        """
        self.writer_file.save()
        self.writer_file.close()
        logger.info("File has been created at {}".format(self.path) + str(datetime.datetime.now().
                                                                          strftime("%Y-%m-%d %H:%M")))


if __name__ == "__main__":
    obj_npd_file = NdpData()
    obj_npd_file.save_and_close_writer()