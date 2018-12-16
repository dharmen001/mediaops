import pandas as pd
from LogFile import logger
from NdpDataFile import NdpDataFile
import datetime


class NdpDataReader(NdpDataFile):
    def __init__(self):
        super(NdpDataReader, self).__init__()
        print(self.section_value[9] + "NdpRawDataFile.csv")
        self.read_ndp_data = None

    def data_reader_ndp(self):
        logger.info("Start Reading NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_ndp_data = pd.read_csv(self.section_value[9] + "NdpRawDataFile.csv")
        read_ndp_data.to_excel(self.writer_file)
        logger.info("Done Reading NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.read_ndp_data = read_ndp_data

    def main(self):
        self.data_reader_ndp()


if __name__ == "__main__":
    obj_NdpDataReader = NdpDataReader()
    obj_NdpDataReader.main()