# !/usr/bin/python
# coding=utf-8

import pandas as pd
import os
import zipfile
import xlrd
import glob

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
        self.read_social_site_platform = None
        self.twitter_data_fr = None
        self.twitter_data_mea = None
        self.twitter_data_za = None
        self.twitter_data = None
        self.facebook_data_es_final = None
        self.facebook_data_de_final = None
        self.facebook_data_fr_final = None
        self.facebook_data_mea_final = None
        self.facebook_data_pt_final = None
        self.facebook_data_uk_final = None
        self.facebook_data_us_final = None
        self.data_reader_ndp_raw()
        self.ndp_static_conversion_reader()
        self.ndp_dynamic_conversion_reader()
        self.ndp_mapping_reader()
        self.dcm_data_reader()
        self.dbm_data_reader()
        self.publisher_data_read()
        self.lead_content_read()
        self.uk_publisher_data()
        self.twitter_data_reader_france()
        self.twitter_data_reader_mea()
        self.twitter_data_reader_za()
        self.final_twitter_data()
        self.facebook_data_reader()

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

    def ndp_mapping_reader(self):

        logger.info("Start Reading:- staticActivityConversionMapping.csv at " + str(datetime.datetime.now().
                                                                                      strftime("%Y-%m-%d %H:%M")))
        read_static_site_conversion = pd.read_csv(self.section_value[9] + "staticActivityConversionMapping.csv")

        logger.info("Done Reading:- staticActivityConversionMapping.csv at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        logger.info("Start Reading:- socialplatformtableumapping.csv at " + str(datetime.datetime.now().
                                                                                    strftime("%Y-%m-%d %H:%M")))

        read_social_site_platform = pd.read_csv(self.section_value[9] + "socialplatformtableumapping.csv")

        logger.info("Done Reading:- socialplatformtableumapping.csv at " +
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
        self.read_social_site_platform = read_social_site_platform

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

        try:
            logger.info("Start Reading:- Sage Global - Publisher Data - Daily.xlsx at " +
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

            read_publisher_data = pd.read_excel(self.section_value[12] + "Sage Global - Publisher Data - Daily.xlsx",
                                                sheet_name='Publisher Provided Data Sheet')

            read_publisher_data = read_publisher_data[:read_publisher_data['Date'].isnull().idxmax()]

            logger.info("Done Reading:- Sage Global - Publisher Data - Daily.xlsx at " +
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

            self.read_publisher_data = read_publisher_data

        except IOError as e:
            logger.error(str(e))
            pass

    def lead_content_read(self):

        try:
            logger.info("Start Reading:-  NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx at " +
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

            read_lead_content = pd.read_excel(self.section_value[12] + "NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx")

            logger.info("Done Reading:-  NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx at " +
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

            read_lead_content.rename(columns={"Region": "Market",
                                              "Media Type": "Channel", "Vendor": "Site",
                                              "Leads": "Conversions", "Spend": "Spend Local"}, inplace=True)

            self.read_lead_content = read_lead_content

        except IOError as e:
            logger.error(str(e))
            pass

    def uk_publisher_data(self):

        logger.info("Start Reading:-  UK Publisher files at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        path = self.section_value[14]
        files = os.listdir(path)

        files_xlsx = [f for f in files if f[-4:] == 'xlsx']

        df = pd.DataFrame()
        for f in files_xlsx:
            logger.info('Start Reading filename: - ' + f + ' Sheet Name -  Sheet1 ')
            try:
                data = pd.read_excel(self.section_value[14] + f, 'Sheet1')
                data['WorkbookName'] = f
                df = df.append(data,  ignore_index=True, sort=True)
            except xlrd.biffh.XLRDError as e:
                pass
                logger.error('Sheet Name Not available at file ' + f + str(e))

            logger.info("Done Reading:-  UK Publisher file " + f + ' Sheet Name -  Sheet1 ' +
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

        df['Week'] = df.loc[:, 'Week Number'].astype(str)
        df['NewWeek'] = df['Week'].str.extract('(\d+)').astype(float)
        df = df.dropna(subset=['Market'], how='all')
        # df['Year'] = df['Year'].astype(datetime)
        # df = df[(df['Year'].dt.year == self.last_year)]
        df.rename(columns={"Inquiries/Leads Delivered": "Conversions",
                           "Inquiries/Leads ACCEPTED": "Leads ACCEPTED",
                           "Inquiries/Leads Booked": "Leads Booked"}, inplace=True)

        df['NConversions'] = df['Conversions'].str.replace('["/" " "]', '-')
        df['NConversions'].fillna((df['Conversions']), inplace=True)
        df.fillna(0, inplace=True)
        self.publisher_data_uk = df.loc[:, ['NewWeek', 'Market', 'WorkbookName', 'Delivered Budget', 'NConversions']]
        # x = self.publisher_data_uk.to_excel(self.writer_file, sheet_name='UKPublisherData')
        # self.save_and_close_writer()
        # exit()
        # instruction_df = pd.DataFrame()
        #
        # for g in files_xlsx:
        #     logger.info('Start Reading filename:- ' + g + ' Sheet Name -  Instructions')
        #     try:
        #         instruction_data = pd.read_excel(self.section_value[14] + g, sheet_name=['Instructions'], skiprows=15)
        #         print(instruction_data)
        #         exit()
        #         instruction_df = instruction_df.append(instruction_data,  ignore_index=True, sort=True)
        #     except xlrd.biffh.XLRDError as e:
        #         pass
        #         logger.error('Sheet Name Not available at file ' + g + str(e))
        #
        #     logger.info("Done Reading:-  UK Publisher file" + g + 'Sheet Name -  Instructions' +
        #                 str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        #
        #     print(instruction_df.tail())
        #
        # exit()

    def twitter_data_reader_france(self):
        twitter_data_fr = pd.read_excel(self.section_value[19] + 'Sage_twitter_france.xlsx')
        twitter_data_fr['Market'] = 'France'
        self.twitter_data_fr = twitter_data_fr

    def twitter_data_reader_mea(self):
        twitter_data_mea = pd.read_excel(self.section_value[19] + 'Sage_twitter_MEA.xlsx')
        twitter_data_mea['Market'] = 'MEA'
        self.twitter_data_mea = twitter_data_mea
        # print(self.twitter_data_mea)

    def twitter_data_reader_za(self):
        twitter_data_za = pd.read_excel(self.section_value[19]+'Sage_twitter_ZA.xlsx')
        twitter_data_za['Market'] = 'ZA'
        self.twitter_data_za = twitter_data_za

    def final_twitter_data(self):
        twitter_data = self.twitter_data_za.append([self.twitter_data_mea, self.twitter_data_fr], sort=True)
        twitter_data.fillna(0, inplace=True)
        twitter_data['Clicks'] = twitter_data['Clicks'].replace('-', 0)
        twitter_data['Conversions'] = twitter_data['Sign ups'] + twitter_data['Site visits'] \
                                      + twitter_data['Custom events'] \
                                      + twitter_data['Downloads']
        twitter_data_final = twitter_data.loc[:, ['Market', 'Impressions', 'Clicks', 'Spend', 'Conversions']]
        self.twitter_data = twitter_data_final

    def facebook_data_reader(self):
        facebook_data_es = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'ES*.csv')], sort=True)
        facebook_data_es = facebook_data_es.dropna(axis=0, subset=['Campaign name'])
        facebook_data_es.fillna(value=0, inplace=True)
        facebook_data_es.rename(columns={"Clicks (all)": "Clicks", "Amount spent (EUR)": "Local Spend"}, inplace=True)
        facebook_data_es['Market'] = 'Spain'
        facebook_data_es['Conversion'] = facebook_data_es['Leads']

        facebook_data_es_final = facebook_data_es.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                          'Clicks', 'Conversion']]

        facebook_data_de = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'DE*.csv')], sort=True)
        facebook_data_de = facebook_data_de.dropna(axis=0, subset=['Campaign name'])
        facebook_data_de.fillna(value=0, inplace=True)
        facebook_data_de.rename(columns={"Clicks (all)": "Clicks", "Amount spent (EUR)": "Local Spend"}, inplace=True)
        facebook_data_de['Market'] = 'Germany'
        facebook_data_de['Conversion'] = facebook_data_de['Leads (form)']

        facebook_data_de_final = facebook_data_de.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                          'Clicks', 'Conversion']]

        facebook_data_fr = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'FR*.csv')], sort=True)
        facebook_data_fr = facebook_data_fr.dropna(axis=0, subset=['Campaign name'])
        facebook_data_fr.fillna(value=0, inplace=True)
        facebook_data_fr.rename(columns={"Clicks (all)": "Clicks", "Amount spent (EUR)": "Local Spend"}, inplace=True)
        facebook_data_fr['Market'] = 'France'
        facebook_data_fr['Conversion'] = 0

        facebook_data_fr_final = facebook_data_fr.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                          'Clicks', 'Conversion']]

        facebook_data_mea = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'MEA*.csv')],
                                      sort=True)
        facebook_data_mea = facebook_data_mea.dropna(axis=0, subset=['Campaign name'])
        facebook_data_mea.fillna(value=0, inplace=True)
        facebook_data_mea.rename(columns={"Clicks (all)": "Clicks", "Amount spent (ZAR)": "Local Spend"}, inplace=True)
        facebook_data_mea['Market'] = 'MEA'
        facebook_data_mea['Conversion'] = facebook_data_mea['Leads (form)']

        facebook_data_mea_final = facebook_data_mea.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                            'Clicks', 'Conversion']]

        facebook_data_pt = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'PT*.csv')], sort=True)
        facebook_data_pt = facebook_data_pt.dropna(axis=0, subset=['Campaign name'])
        facebook_data_pt.fillna(value=0, inplace=True)
        facebook_data_pt.rename(columns={"Clicks (all)": "Clicks", "Amount spent (EUR)": "Local Spend"}, inplace=True)
        facebook_data_pt['Market'] = 'Portugal'
        facebook_data_pt['Conversion'] = facebook_data_pt['Leads']

        facebook_data_pt_final = facebook_data_pt.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                          'Clicks', 'Conversion']]

        facebook_data_uk = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'UK*.csv')], sort=True)
        facebook_data_uk = facebook_data_uk.dropna(axis=0, subset=['Campaign name'])
        facebook_data_uk.fillna(value=0, inplace=True)
        facebook_data_uk.rename(columns={"Clicks (all)": "Clicks", "Amount spent (GBP)": "Local Spend"}, inplace=True)
        facebook_data_uk['Market'] = 'UK'
        facebook_data_uk['Conversion'] = facebook_data_uk['Website payment info adds'] + \
                                         facebook_data_uk['Website purchases'] + \
                                         facebook_data_uk['Adds of payment info'] + \
                                         facebook_data_uk['Adds to cart'] + \
                                         facebook_data_uk['Adds to wishlist'] + \
                                         facebook_data_uk['Checkouts initiated'] + \
                                         facebook_data_uk['Registrations completed'] + \
                                         facebook_data_uk['Download'] + \
                                         facebook_data_uk['Download [On ad]']

        facebook_data_uk_final = facebook_data_uk.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                          'Clicks', 'Conversion']]

        facebook_data_us = pd.concat([pd.read_csv(f) for f in glob.glob(self.section_value[24] + 'US*.csv')], sort=True)
        facebook_data_us = facebook_data_us.dropna(axis=0, subset=['Campaign name'])
        facebook_data_us.fillna(value=0, inplace=True)
        facebook_data_us.rename(columns={"Clicks (all)": "Clicks", "Amount spent (USD)": "Local Spend"}, inplace=True)
        facebook_data_us['Market'] = 'US'
        facebook_data_us['Conversion'] = 0

        facebook_data_us_final = facebook_data_us.loc[:, ['Market', 'Impressions', 'Local Spend',
                                                          'Clicks', 'Conversion']]

        self.facebook_data_es_final = facebook_data_es_final
        self.facebook_data_de_final = facebook_data_de_final
        self.facebook_data_fr_final = facebook_data_fr_final
        self.facebook_data_mea_final = facebook_data_mea_final
        self.facebook_data_pt_final = facebook_data_pt_final
        self.facebook_data_uk_final = facebook_data_uk_final
        self.facebook_data_us_final = facebook_data_us_final


if __name__ == "__main__":
    obj_NdpDataReader = NdpReader()
    # obj_NdpDataReader.main()
