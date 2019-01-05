# !/usr/bin/python
# coding=utf-8

import pandas as pd
import os
import zipfile
import xlrd

from Classes.LoggerFile.LogFile import logger
import datetime
import Classes.DataWriters.NdpDataFile
import pandas.io.formats.excel

pandas.io.formats.excel.header_style = None


class NdpReader(Classes.DataWriters.NdpDataFile.NdpData):
    def __init__(self):

        super(NdpReader, self).__init__()
        # print(self.section_value[9] + "NdpRawDataFile.csv")
        self.now = datetime.datetime.now()
        self.last_month = self.now.month - 1 if self.now.month > 1 else 12
        self.last_year = self.now.year - 1
        self.read_ndp_data = None
        self.read_dmc_data = None
        self.read_dbm_data = None
        self.read_publisher_data = None
        self.read_lead_content = None
        self.publisher_data_uk = None
        self.dynamic_df = None
        self.read_static_site_conversion = None
        self.read_site_dcm_platform_mapping = None
        self.read_advertiser_mapping = None
        self.read_conversion_raw_file = None
        self.read_tableau_advertiser_mapping = None
        self.read_tableau_platform_mapping = None
        self.read_site_display_mapping = None
        self.data_reader_ndp_raw()
        self.ndp_static_conversion_reader()
        self.ndp_dynamic_conversion_reader()
        self.ndp_mapping_reader()
        self.dcm_data_reader()
        self.dbm_data_reader()
        self.publisher_data_read()
        self.lead_content_read()
        self.uk_publisher_data()

    def data_reader_ndp_raw(self):

        logger.info("Start Reading:- NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_ndp_data = pd.read_csv(self.section_value[9] + "NdpRawDataFile.csv", encoding="ISO-8859-1")
        logger.info("Done Reading:- NdpRawDataFile.csv at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.read_ndp_data = read_ndp_data

    def ndp_static_conversion_reader(self):
        logger.info("Start Reading:- DMC_Static_Conversions.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_conversion_raw_file = pd.read_csv(self.section_value[12] + "DMC_Static_Conversions.csv")

        logger.info("Done Reading:- DMC_Static_Conversions.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        self.read_conversion_raw_file = read_conversion_raw_file

    def ndp_dynamic_conversion_reader(self):

        raw_dynamic_conversion_us = pd.read_csv(self.section_value[12] + "DynamicUS.csv", engine='python',
                                                skipfooter=1, skiprows=13)

        raw_dynamic_conversion_uk = pd.read_csv(self.section_value[12] + "DynamicUK.csv", engine='python',
                                                skipfooter=1, skiprows=18)

        raw_dynamic_conversion_spain = pd.read_csv(self.section_value[12] + "DynamicSpain.csv", engine='python',
                                                   skipfooter=1, skiprows=12)

        raw_dynamic_conversion_germany = pd.read_csv(self.section_value[12] + "DynamicGermany.csv", engine='python',
                                                     skipfooter=1, skiprows=13)

        raw_dynamic_conversion_france = pd.read_csv(self.section_value[12] + "DynamicFrance.csv", engine='python',
                                                    skiprows=12, skipfooter=1)

        raw_dynamic_conversion_us['Market'] = 'USA'
        raw_dynamic_conversion_uk['Market'] = 'UK'
        raw_dynamic_conversion_spain['Market'] = 'Spain'
        raw_dynamic_conversion_germany['Market'] = 'Germany'
        raw_dynamic_conversion_france['Market'] = 'France'

        dynamic_df = pd.concat([raw_dynamic_conversion_us,
                                raw_dynamic_conversion_uk.rename(columns={'Form_lead_type (string)': 'Form_lead_type (string)'}),
                                raw_dynamic_conversion_spain.rename(columns={'Form_lead_type (string)': 'Form_lead_type (string)'}),
                                raw_dynamic_conversion_germany.rename(columns={'Formleadtype (string)': 'Form_lead_type (string)'}),
                                raw_dynamic_conversion_france.rename(columns={'form_solution_lead_type (string)': 'Form_lead_type (string)'})],
                               axis=0, sort=True, ignore_index=True)

        self.dynamic_df = dynamic_df


    def criteo_data_reader(self):
        pass

    def ndp_mapping_reader(self):

        logger.info("Start Reading:- staticActivityConversionMapping.csv at " + str(datetime.datetime.now().
                                                                                      strftime("%Y-%m-%d %H:%M")))
        read_static_site_conversion = pd.read_csv(self.section_value[9] + "staticActivityConversionMapping.csv")

        logger.info("Done Reading:- staticActivityConversionMapping.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info("Start Reading:- siteStaticConversionMapping.csv at " + str(datetime.datetime.now().
                                                                                      strftime("%Y-%m-%d %H:%M")))
        read_site_dcm_platform_mapping = pd.read_csv(self.section_value[9] + "siteStaticConversionMapping.csv")

        logger.info("Done Reading:- siteStaticConversionMapping.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info("Start Reading:- advertiserMarketMapping.csv at " + str(datetime.datetime.now().
                                                                           strftime("%Y-%m-%d %H:%M")))

        read_advertiser_mapping = pd.read_csv(self.section_value[9] + "advertiserMarketMapping.csv")

        logger.info("Done Reading:- advertiserMarketMapping.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info("Start Reading:- advertiserMappingTableau.csv at " + str(datetime.datetime.now().
                                                                            strftime("%Y-%m-%d %H:%M")))
        read_tableau_advertiser_mapping = pd.read_csv(self.section_value[9] + "advertiserMappingTableau.csv")

        logger.info("Done Reading:- advertiserMappingTableau.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info("Start Reading:- tableauPlatformMapping.csv at " + str(datetime.datetime.now().
                                                                            strftime("%Y-%m-%d %H:%M")))
        read_tableau_platform_mapping = pd.read_csv(self.section_value[9] + "tableauPlatformMapping.csv")

        logger.info("Done Reading:- tableauPlatformMapping.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info("Start Reading:- siteDisplayPerformanceMapping.csv at " + str(datetime.datetime.now().
                                                                           strftime("%Y-%m-%d %H:%M")))
        read_site_display_mapping = pd.read_csv(self.section_value[9] + "siteDisplayPerformanceMapping.csv")

        logger.info("Done Reading:- siteDisplayPerformanceMapping.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        self.read_static_site_conversion = read_static_site_conversion
        self.read_site_dcm_platform_mapping = read_site_dcm_platform_mapping
        self.read_advertiser_mapping = read_advertiser_mapping
        self.read_tableau_advertiser_mapping = read_tableau_advertiser_mapping
        self.read_tableau_platform_mapping = read_tableau_platform_mapping
        self.read_site_display_mapping = read_site_display_mapping

    def dcm_data_reader(self):

        logger.info("Start Reading:- DMC_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        read_dmc_data_zf = zipfile.ZipFile(self.section_value[12] + "DMC_Report.zip")
        read_dmc_data = pd.read_csv(read_dmc_data_zf.open(zipfile.ZipFile.namelist(read_dmc_data_zf)[0]),
                                    skiprows=9, skipfooter=1, engine='python', encoding="utf-8",
                                    parse_dates=['Date'])

        read_dmc_data = read_dmc_data[(read_dmc_data['Date'].dt.year == self.last_year) &
                                      (read_dmc_data['Date'].dt.month == self.last_month)]

        logger.info("Done Reading:- DMC_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.read_dmc_data = read_dmc_data

    def dbm_data_reader(self):

        logger.info("Start Reading:- DBM_Report.zip at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        read_dbm_data_zf = zipfile.ZipFile(self.section_value[12] + "DBM_Report.zip")
        read_dbm_data = pd.read_csv(read_dbm_data_zf.open(zipfile.ZipFile.namelist(read_dbm_data_zf)[0]),
                                    engine='python', encoding="utf-8", error_bad_lines=False)

        read_dbm_data = read_dbm_data[:read_dbm_data['Date'].isnull().idxmax()]
        read_dbm_data['Date'] = pd.to_datetime(read_dbm_data['Date'])

        read_dbm_data = read_dbm_data[(read_dbm_data['Date'].dt.year == self.last_year) &
                                      (read_dbm_data['Date'].dt.month == self.last_month)]

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
        # x = self.publisher_data_uk.to_excel(self.writer_file, sheet_name='UKPublisherData')
        # self.save_and_close_writer()

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

    # def main(self):
    #     self.data_reader_ndp_raw()
    #     self.ndp_static_conversion_reader()
    #     self.ndp_dynamic_conversion_reader()
    #     self.ndp_mapping_reader()
    #     self.dcm_data_reader()
    #     self.dbm_data_reader()
    #     self.publisher_data_read()
    #     self.lead_content_read()
    #     self.uk_publisher_data()


if __name__ == "__main__":
    obj_NdpDataReader = NdpReader()
    # obj_NdpDataReader.main()
