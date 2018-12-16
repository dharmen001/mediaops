import pandas as pd
import datetime
from config import Config
from LogFile import logger


class NdpDataFile(Config):
    def __init__(self):
        super(NdpDataFile, self).__init__()
        self.path = self.section_value[10] + "Data Audit_GDS_All_Markets for ({}-{}).xlsx".\
            format(datetime.datetime.now().year, datetime.datetime.now().month - 1)

        logger.info("Start creating NDPFile ")

        self.writer_file = pd.ExcelWriter(self.path, engine="xlsxwriter", datetime_format="YYYY-MM-DD")

    def save_and_close_writer(self):
        """
        To finally Save and close file
        :return: Nothing
        """
        self.writer_file.save()
        self.writer_file.close()
        logger.info("File has been create at {}".format(self.path))


if __name__ == "__main__":
    obj_npd_file = NdpDataFile()