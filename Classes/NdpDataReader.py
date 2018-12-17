# !/usr/bin/python
# coding=utf-8

import pandas as pd
from LogFile import logger
import datetime
import NdpDataFile
import pandas.io.formats.excel
pandas.io.formats.excel.header_style = None


class NdpReader(NdpDataFile.NdpData):
    def __init__(self):
        super(NdpReader, self).__init__()
        print(self.section_value[9] + "NdpRawDataFile.csv")
        self.read_ndp_data = None

    def data_reader_ndp(self):
        logger.info("Start Reading NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_ndp_data = pd.read_csv(self.section_value[9] + "NdpRawDataFile.csv", encoding="ISO-8859-1")
        logger.info("Done Reading NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.read_ndp_data = read_ndp_data

    def main(self):
        self.data_reader_ndp()


if __name__ == "__main__":
    obj_NdpDataReader = NdpReader()
    obj_NdpDataReader.main()
