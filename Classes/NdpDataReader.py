# !/usr/bin/python
# coding=utf-8

import pandas as pd
import os
import zipfile

import xlrd

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
        self.read_dmc_data = None
        self.read_dbm_data = None
        self.read_publisher_data = None
        self.read_lead_content = None
        self.df = None
        self.publisher_data_uk = None

    def data_reader_ndp_raw(self):

        logger.info("Start Reading:- NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_ndp_data = pd.read_csv(self.section_value[9] + "NdpRawDataFile.csv", encoding="ISO-8859-1")
        logger.info("Done Reading:- NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.read_ndp_data = read_ndp_data

    def dcm_data_reader(self):

        logger.info("Start Reading:- DMC_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_dmc_data_zf = zipfile.ZipFile(self.section_value[12] + "DMC_Report.zip")
        read_dmc_data = pd.read_csv(read_dmc_data_zf.open(zipfile.ZipFile.namelist(read_dmc_data_zf)[0]),
                                    skiprows=11, skipfooter=1, engine='python', encoding="ISO-8859-1")

        logger.info("Done Reading:- DMC_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.read_dmc_data = read_dmc_data

    def dbm_data_reader(self):

        logger.info("Start Reading:- DBM_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        read_dbm_data_zf = zipfile.ZipFile(self.section_value[12] + "DBM_Report.zip")
        read_dbm_data = pd.read_csv(read_dbm_data_zf.open(zipfile.ZipFile.namelist(read_dbm_data_zf)[0]),
                                    engine='python', encoding="ISO-8859-1", error_bad_lines=False)
        read_dbm_data = read_dbm_data[:read_dbm_data['Date'].isnull().idxmax()]
        read_dbm_data['Date'] = pd.to_datetime(read_dbm_data['Date'])

        logger.info("Done Reading:- DBM_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        self.read_dbm_data = read_dbm_data

    def publisher_data_read(self):

        logger.info("Start Reading:- Sage Global - Publisher Data - Daily.xlsx at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        read_publisher_data = pd.read_excel(self.section_value[12] + "Sage Global - Publisher Data - Daily.xlsx",
                                            sheet_name='Publisher Provided Data Sheet')

        read_publisher_data = read_publisher_data[:read_publisher_data['Date'].isnull().idxmax()]

        logger.info("Done Reading:- Sage Global - Publisher Data - Daily.xlsx at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        self.read_publisher_data = read_publisher_data

    def lead_content_read(self):

        logger.info("Start Reading:-  NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        read_lead_content = pd.read_excel(self.section_value[12] + "NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx")

        logger.info("Done Reading:-  NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        self.read_lead_content = read_lead_content

    def uk_publisher_data(self):

        logger.info("Start Reading:-  UK Publisher files at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        path = self.section_value[14]
        files = os.listdir(path)

        files_xlsx = [f for f in files if f[-4:] == 'xlsx']

        df = pd.DataFrame()
        for f in files_xlsx:
            logger.info('Start Reading filename: -' + f + 'Sheet Name -  Sheet1')
            try:
                data = pd.read_excel(self.section_value[14] + f, 'Sheet1')
                df = df.append(data,  ignore_index=True, sort=True)
            except xlrd.biffh.XLRDError as e:
                pass
                logger.error('Sheet Name Not available at file ' + f + str(e))

            logger.info("Done Reading:-  UK Publisher file" + f + 'Sheet Name -  Sheet1' +
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        uk_publisher_data = df.dropna(how='all')
        self.publisher_data_uk = uk_publisher_data

        # instruction_df = pd.DataFrame()
        #
        # for g in files_xlsx:
        #     logger.info('Start Reading filename:- ' + g + ' Sheet Name -  Instructions')
        #     try:
        #         instruction_data = pd.read_excel(self.section_value[14] + g, 'Instructions', skiprows=14)
        #         instruction_df = instruction_df.append(instruction_data,  ignore_index=True, sort=True)
        #     except xlrd.biffh.XLRDError as e:
        #         pass
        #         logger.error('Sheet Name Not available at file ' + g + str(e))
        #
        #     logger.info("Done Reading:-  UK Publisher file" + g + 'Sheet Name -  Instructions' +
        #                 str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        # print(instruction_df.tail())

    def main(self):
        self.data_reader_ndp_raw()
        self.dcm_data_reader()
        self.dbm_data_reader()
        self.publisher_data_read()
        self.lead_content_read()
        self.uk_publisher_data()


if __name__ == "__main__":
    obj_NdpDataReader = NdpReader()
    obj_NdpDataReader.main()
