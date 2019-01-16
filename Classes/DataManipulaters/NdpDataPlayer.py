# !/usr/bin/python
# coding=utf-8

import pandas as pd
from Classes.DataReaders.NdpDataReader import NdpReader
from functools import reduce
import numpy as np
from Classes.LoggerFile.LogFile import logger


class NdpDataPlayer(NdpReader):

    def __init__(self):
        # Inheriting Reader Class
        super(NdpDataPlayer, self).__init__()
        self.merged_internal_data_advertiser = None
        self.static_conversions_report = None
        self.internal_conversions_new = None
        self.activity_with_static_conversion = None
        self.data_static_conversion_new = None
        self.dynamic_conversion = None
        self.final_dcm_data = None
        self.final_dbm_data = None
        self.dynamic_conversion_df = None
        self.dbm_dcm_data = None
        self.internal_data_performance = None
        self.merged_publisher_data_advertiser = None
        self.read_ndp_data_platform = None
        self.read_ndp_data_publisher = None
        self.internal_publisher_data_new = None
        self.read_publisher_data_other_us = None
        self.market_publisher_other_than_us = None
        self.read_lead_content_us = None
        self.read_lead_content_us_new = None
        self.final_us_ca_publisher_data = None
        self.publisher_data_uk_new = None
        self.uk_pub_data_reset = None
        self.read_ndp_data_social = None
        self.social_internal_pivot_reset = None
        self.twitter_data_player_reset = None
        self.internal_data()
        self.market_mapping_internal_data()
        self.internal_performance_data()
        self.market_mapping_static_conversion()
        self.add_conversion_static_column()
        self.platform_mapping_dynamic()
        self.add_conversion_dynamic()
        self.performance_data()
        self.merge_performance_data()
        self.internal_publisher_data()
        self.internal_publisher_data_process()
        self.market_publisher_data_other_us()
        self.market_publisher_data_us()
        self.pub_data_uk()
        self.social_npd_data()
        self.twitter_data_player()

    def internal_data(self):
        # Removing unconditional rows from NDP Tableau Raw Data
        logger.info("Start removing channel from tableau data")
        self.read_ndp_data_platform = self.read_ndp_data
        remove_row_channel = self.read_ndp_data_platform[self.read_ndp_data_platform['Channel'].isin([
            'CONTENT SYNDICATION', 'OTHER', 'LEAD AGGREGATOR'])]
        self.read_ndp_data_platform = self.read_ndp_data_platform.drop(remove_row_channel.index, axis=0)

        logger.info("Start removing BR Market from tableau data")
        remove_row_market = self.read_ndp_data_platform[self.read_ndp_data_platform['Market'].isin(['BR'])]

        self.read_ndp_data_platform = self.read_ndp_data_platform.drop(remove_row_market.index, axis=0)

    def market_mapping_internal_data(self):
        internal_data_merge_platform = [self.read_ndp_data_platform, self.read_tableau_platform_mapping]
        merged_internal_data = reduce(lambda left, right: pd.merge(left, right, on='Channel'),
                                      internal_data_merge_platform)

        internal_data_merge_market = [merged_internal_data, self.read_tableau_advertiser_mapping]
        merged_internal_data_advertiser = reduce(lambda left, right: pd.merge(left, right, on='Market'),
                                                 internal_data_merge_market)

        self.merged_internal_data_advertiser = merged_internal_data_advertiser

        internal_conversions = pd.pivot_table(self.merged_internal_data_advertiser, values=['Application',
                                                                                            'Contact', 'Download'
            , 'Free Trial', 'Purchase',
                                                                                            'Other Activity',
                                                                                            'Other Dynamic Floodlight'],
                                              index=['New Market', 'Platform'], aggfunc=np.sum)

        internal_conversions_new = internal_conversions.reset_index()
        internal_conversions_new.rename(columns={"New Market": "Market"}, inplace=True)

        self.internal_conversions_new = internal_conversions_new

    def internal_performance_data(self):
        internal_performance = pd.pivot_table(self.merged_internal_data_advertiser, index=['New Market', 'Platform'],
                                              values=['Impressions', 'Clicks', 'Spend Local'], aggfunc=np.sum)

        internal_data_performance = internal_performance.reset_index()
        internal_data_performance.rename(columns={"New Market": "Market"}, inplace=True)
        internal_data_performance_display = internal_data_performance[(internal_data_performance['Platform']
                                                                       == 'Display')]

        internal_data_performance_final = internal_data_performance_display[['Market', 'Clicks', 'Impressions',
                                                                             'Spend Local']]
        self.internal_data_performance = internal_data_performance_final

    def market_mapping_static_conversion(self):
        """Advertiser Which needs to count"""
        static_conversion_merge_advertiser = [self.read_conversion_raw_file, self.read_advertiser_mapping]
        advertiser_with_static_conversion = reduce(lambda left, right: pd.merge(left, right, on='Advertiser'),
                                                   static_conversion_merge_advertiser)
        """Site Which needs to count"""
        static_conversion_merge_platform = [advertiser_with_static_conversion, self.read_site_dcm_platform_mapping]

        platform_with_static_conversion = reduce(lambda left, right: pd.merge(left, right, on='Site (DCM)'),
                                                 static_conversion_merge_platform)

        """Activity Which Needs to count"""
        static_conversion_merge_activity = [platform_with_static_conversion, self.read_static_site_conversion]

        activity_with_static_conversion = reduce(lambda left, right: pd.merge(left, right, on='Activity'),
                                                 static_conversion_merge_activity)

        self.activity_with_static_conversion = activity_with_static_conversion

        # static_site_conversion = merged_static_site[merged_static_site['Site'].isnull()]

    def add_conversion_static_column(self):
        mask_cont = self.activity_with_static_conversion['ActivityName'].str.contains('_CONT_')
        mask_download = self.activity_with_static_conversion['ActivityName'].str.contains('_DOWN_')
        mask_application = self.activity_with_static_conversion['ActivityName'].str.contains('_APPL_')
        mask_itrs = self.activity_with_static_conversion['ActivityName'].str.contains('_ITRS_')
        mask_ibuy = self.activity_with_static_conversion['ActivityName'].str.contains('_IBUY_')

        choice_cont = self.activity_with_static_conversion['Total Conversions']
        choice_download = self.activity_with_static_conversion['Total Conversions']
        choice_application = self.activity_with_static_conversion['Total Conversions']
        choice_itrs = self.activity_with_static_conversion['Total Conversions']
        choice_ibuy = self.activity_with_static_conversion['Total Conversions']
        choice_other = self.activity_with_static_conversion['Total Conversions']

        """Creating Columns in Static Conversions"""
        self.activity_with_static_conversion['Application'] = np.select([mask_application], [choice_application],
                                                                        default=0)
        self.activity_with_static_conversion['Contact'] = np.select([mask_cont], [choice_cont], default=0)
        self.activity_with_static_conversion['Download'] = np.select([mask_download], [choice_download], default=0)
        self.activity_with_static_conversion['Purchase'] = np.select([mask_ibuy], [choice_ibuy], default=0)
        self.activity_with_static_conversion['Free Trial'] = np.select([mask_itrs], [choice_itrs], default=0)
        self.activity_with_static_conversion['Others'] = self.activity_with_static_conversion['Application'] + \
                                                         self.activity_with_static_conversion['Contact'] + \
                                                         self.activity_with_static_conversion['Download'] + \
                                                         self.activity_with_static_conversion['Purchase'] + \
                                                         self.activity_with_static_conversion['Free Trial']

        self.activity_with_static_conversion['Other Conversions'] = np.select(
            [self.activity_with_static_conversion['Others'] == 0],
            [choice_other], default=0)

        data_static_conversion = pd.pivot_table(self.activity_with_static_conversion, index=['Country', 'Platform'],
                                                values=['Application', 'Contact', 'Download', 'Purchase',
                                                        'Free Trial', 'Other Conversions'],
                                                aggfunc=np.sum)

        data_static_conversion_new = data_static_conversion.reset_index()
        data_static_conversion_new.rename(columns={"Country": "Market"}, inplace=True)

        self.data_static_conversion_new = data_static_conversion_new

    def platform_mapping_dynamic(self):
        dynamic_platform_df = [self.dynamic_df, self.read_site_dcm_platform_mapping]
        dynamic_conversion_df = reduce(lambda left, right: pd.merge(left, right, on='Site (DCM)'),
                                       dynamic_platform_df)

        dynamic_conversion_df['Form_lead_type (string)'] = dynamic_conversion_df['Form_lead_type (string)'].fillna('')

        self.dynamic_conversion_df = dynamic_conversion_df

    def add_conversion_dynamic(self):
        mask_sub = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_SUB_')
        mask_quo = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_QUO_')
        mask_eml = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_EML_')
        mask_res = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_RES_')
        mask_add = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_ADD_')
        mask_ot = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_OT_')
        mask_con = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_CON_')
        mask_eve = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_EVE_')
        mask_art = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_ART_')
        mask_pdf = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_PDF_')
        mask_vid = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_VID_')
        mask_inf = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_INF_')
        mask_img = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_IMG_')
        mask_temp = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_TEMP_')
        mask_dem = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_DEM_')
        mask_trl = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_TRL_')
        mask_tool = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_TOOL_')
        mask_ibuy = self.dynamic_conversion_df['Form_lead_type (string)'].str.contains('_IBUY_')

        choice_sub = self.dynamic_conversion_df['Total Conversions']
        choice_quo = self.dynamic_conversion_df['Total Conversions']
        choice_eml = self.dynamic_conversion_df['Total Conversions']
        choice_res = self.dynamic_conversion_df['Total Conversions']
        choice_add = self.dynamic_conversion_df['Total Conversions']
        choice_ot = self.dynamic_conversion_df['Total Conversions']
        choice_con = self.dynamic_conversion_df['Total Conversions']
        choice_eve = self.dynamic_conversion_df['Total Conversions']
        choice_art = self.dynamic_conversion_df['Total Conversions']
        choice_pdf = self.dynamic_conversion_df['Total Conversions']
        choice_vid = self.dynamic_conversion_df['Total Conversions']
        choice_inf = self.dynamic_conversion_df['Total Conversions']
        choice_img = self.dynamic_conversion_df['Total Conversions']
        choice_temp = self.dynamic_conversion_df['Total Conversions']
        choice_dem = self.dynamic_conversion_df['Total Conversions']
        choice_trl = self.dynamic_conversion_df['Total Conversions']
        choice_tool = self.dynamic_conversion_df['Total Conversions']
        choice_ibuy = self.dynamic_conversion_df['Total Conversions']

        self.dynamic_conversion_df['Sub'] = np.select([mask_sub], [choice_sub], default=0)
        self.dynamic_conversion_df['Quo'] = np.select([mask_quo], [choice_quo], default=0)
        self.dynamic_conversion_df['Eml'] = np.select([mask_eml], [choice_eml], default=0)
        self.dynamic_conversion_df['Res'] = np.select([mask_res], [choice_res], default=0)
        self.dynamic_conversion_df['Add'] = np.select([mask_add], [choice_add], default=0)
        self.dynamic_conversion_df['Ot'] = np.select([mask_ot], [choice_ot], default=0)
        self.dynamic_conversion_df['Con'] = np.select([mask_con], [choice_con], default=0)
        self.dynamic_conversion_df['Eve'] = np.select([mask_eve], [choice_eve], default=0)
        self.dynamic_conversion_df['Art'] = np.select([mask_art], [choice_art], default=0)
        self.dynamic_conversion_df['Pdf'] = np.select([mask_pdf], [choice_pdf], default=0)
        self.dynamic_conversion_df['Vid'] = np.select([mask_vid], [choice_vid], default=0)
        self.dynamic_conversion_df['Inf'] = np.select([mask_inf], [choice_inf], default=0)
        self.dynamic_conversion_df['Img'] = np.select([mask_img], [choice_img], default=0)
        self.dynamic_conversion_df['Temp'] = np.select([mask_temp], [choice_temp], default=0)
        self.dynamic_conversion_df['Dem'] = np.select([mask_dem], [choice_dem], default=0)
        self.dynamic_conversion_df['Trl'] = np.select([mask_trl], [choice_trl], default=0)
        self.dynamic_conversion_df['Tool'] = np.select([mask_tool], [choice_tool], default=0)
        self.dynamic_conversion_df['Ibuy'] = np.select([mask_ibuy], [choice_ibuy], default=0)

        self.dynamic_conversion_df['Contact'] = self.dynamic_conversion_df['Sub'] + self.dynamic_conversion_df['Quo'] + \
                                                self.dynamic_conversion_df['Eml'] + self.dynamic_conversion_df['Res'] + \
                                                self.dynamic_conversion_df['Add'] + self.dynamic_conversion_df['Ot'] + \
                                                self.dynamic_conversion_df['Con'] + self.dynamic_conversion_df['Eve']

        self.dynamic_conversion_df['Download'] = self.dynamic_conversion_df['Art'] + self.dynamic_conversion_df['Pdf'] + \
                                                 self.dynamic_conversion_df['Vid'] + self.dynamic_conversion_df['Inf'] + \
                                                 self.dynamic_conversion_df['Img'] + self.dynamic_conversion_df['Temp']

        self.dynamic_conversion_df['Free Trial'] = self.dynamic_conversion_df['Dem'] + self.dynamic_conversion_df[
            'Trl'] + \
                                                   self.dynamic_conversion_df['Tool']

        self.dynamic_conversion_df['Purchase'] = self.dynamic_conversion_df['Ibuy']

        self.dynamic_conversion_df['Total'] = self.dynamic_conversion_df['Contact'] + self.dynamic_conversion_df[
            'Download'] + \
                                              self.dynamic_conversion_df['Free Trial'] + self.dynamic_conversion_df[
                                                  'Purchase']

        self.dynamic_conversion_df['Other Dynamic Conversions'] = np.select([self.dynamic_conversion_df['Total'] == 0],
                                                                            [self.dynamic_conversion_df[
                                                                                 'Total Conversions']],
                                                                            default=0)

        dynamic_conversion_final = pd.pivot_table(self.dynamic_conversion_df, index=['Market', 'Platform'],
                                                  values=['Contact', 'Download', 'Free Trial', 'Purchase',
                                                          'Other Dynamic Conversions'], aggfunc=np.sum)

        dynamic_conversion = dynamic_conversion_final.reset_index()

        self.dynamic_conversion = dynamic_conversion

    def performance_data(self):
        # self.read_dbm_data.columns = [col.encode('ascii', 'ignore') for col in self.read_dbm_data]
        # self.read_dmc_data.columns = [col.encode('ascii', 'ignore') for col in self.read_dmc_data]

        # self.read_dmc_data["Date"] = self.read_dmc_data["Date"].astype(str)
        # self.read_dmc_data["Placement ID"] = self.read_dmc_data["Placement ID"].astype(str)

        # self.read_dmc_data["Pl_Date"] = self.read_dmc_data[['Placement ID', 'Date']].apply(lambda x: " ".join(x),
        #                                                                                    axis=1)
        dmc_platform_mapping = [self.read_dmc_data, self.read_site_display_mapping]

        merge_platform_dmc = reduce(lambda left, right: pd.merge(left, right, on='Site (DCM)'),
                                    dmc_platform_mapping)

        dmc_market_mapping = [merge_platform_dmc, self.read_advertiser_mapping]

        merge_market_platform_dmc = reduce(lambda left, right: pd.merge(left, right, on='Advertiser'),
                                           dmc_market_mapping)

        dcm_data = pd.pivot_table(merge_market_platform_dmc, index=['Country', 'Placement ID'],
                                  values=['Impressions', 'Clicks', 'Media Cost'], aggfunc=np.sum)

        dcm_data_final = dcm_data.reset_index()

        # self.read_dbm_data['Date'] = self.read_dbm_data["Date"].astype(str)
        # self.read_dbm_data['CM Placement ID'] = self.read_dbm_data['CM Placement ID'].astype(str)
        # self.read_dbm_data['CM Placement ID'] = self.read_dbm_data['CM Placement ID'].str.replace('.0', '')

        # self.read_dbm_data['Pl_Date'] = self.read_dbm_data[['CM Placement ID', 'Date']].apply(lambda x: " ".join(x),
        #                                                                                       axis=1)

        final_dcm_data = dcm_data_final[['Country', 'Placement ID', 'Impressions', 'Clicks', 'Media Cost']]

        dbm_data = pd.pivot_table(self.read_dbm_data, index=['CM Placement ID'],
                                  values=['Total Media Cost (Advertiser Currency)'], aggfunc=np.sum)

        dbm_data_final = dbm_data.reset_index()

        dbm_data_final.rename(columns={"CM Placement ID": "Placement ID"}, inplace=True)

        final_dbm_data = dbm_data_final[['Placement ID', 'Total Media Cost (Advertiser Currency)']]

        self.final_dcm_data = final_dcm_data
        self.final_dbm_data = final_dbm_data

    def merge_performance_data(self):
        dbm_dcm_data = self.final_dcm_data.merge(self.final_dbm_data, how='left', on='Placement ID')
        dbm_dcm_data['Total Media Cost (Advertiser Currency)'] = dbm_dcm_data['Total Media Cost (Advertiser Currency)'] \
            .fillna(value=dbm_dcm_data['Media Cost'])

        dbm_dcm_data.rename(columns={"Total Media Cost (Advertiser Currency)": "Spend Local",
                                     "Country": "Market"}, inplace=True)

        dbm_data_new = pd.pivot_table(dbm_dcm_data, index=['Market'], values=['Impressions', 'Clicks', 'Spend Local'],
                                      aggfunc=np.sum)

        dbm_data_reset = dbm_data_new.reset_index()

        self.dbm_dcm_data = dbm_data_reset

    def internal_publisher_data(self):
        self.read_ndp_data_publisher = self.read_ndp_data
        remove_row_channel_publisher = self.read_ndp_data_publisher[self.read_ndp_data_publisher['Channel'].isin(
            ['DISPLAY', 'SEARCH', 'SOCIAL'])]
        self.read_ndp_data_publisher = self.read_ndp_data_publisher.drop(remove_row_channel_publisher.index, axis=0)

        logger.info("Start removing BR Market from tableau data")
        remove_row_market_publisher = self.read_ndp_data_publisher[self.read_ndp_data_publisher['Market'].isin(['BR'])]

        self.read_ndp_data_publisher = self.read_ndp_data_publisher.drop(remove_row_market_publisher.index, axis=0)

        publisher_data_merge_platform = [self.read_ndp_data_publisher, self.read_tableau_platform_mapping]
        merged_internal_data_publisher = reduce(lambda left, right: pd.merge(left, right, on='Channel'),
                                                publisher_data_merge_platform)

        publisher_data_merge_market = [merged_internal_data_publisher, self.read_tableau_advertiser_mapping]
        merged_publisher_data_advertiser = reduce(lambda left, right: pd.merge(left, right, on='Market'),
                                                  publisher_data_merge_market)

        self.merged_publisher_data_advertiser = merged_publisher_data_advertiser

    def internal_publisher_data_process(self):
        internal_publisher_data = pd.pivot_table(self.merged_publisher_data_advertiser,
                                                 index=['New Market', 'Platform', 'Publisher'],
                                                 values=['Impressions', 'Clicks', 'Conversions',
                                                         'Spend Local'], aggfunc=np.sum)

        internal_publisher_data_new = internal_publisher_data.reset_index()

        internal_publisher_data_new.rename(columns={"New Market": "Market", "Publisher": "Site"}, inplace=True)

        self.internal_publisher_data_new = internal_publisher_data_new

    def market_publisher_data_other_us(self):
        self.read_publisher_data_other_us = self.read_publisher_data
        self.read_publisher_data_other_us = self.read_publisher_data_other_us[(self.read_publisher_data_other_us
                                                                               ['Date'].dt.year == self.last_year) &
                                                                              (self.read_publisher_data_other_us
                                                                               ['Date'].dt.month ==
                                                                               self.last_month)]
        publisher_data_other_us = [self.read_publisher_data_other_us, self.read_tableau_advertiser_mapping]
        merged_publisher_market_other_us = reduce(lambda left, right: pd.merge(left, right, on='Market'),
                                                  publisher_data_other_us)

        merged_publisher_market_other_us.rename(columns={"Site/Partner": "Site",
                                                         "Spend_In_Local_Currency": "Spend Local"}, inplace=True)

        market_publisher_data = pd.pivot_table(merged_publisher_market_other_us, index=['New Market', 'Channel',
                                                                                        'Site'],
                                               values=['Impressions', 'Clicks', 'Conversions',
                                                       'Spend Local'], aggfunc=np.sum)

        market_publisher_data_reset = market_publisher_data.reset_index()
        remove_row_platform = market_publisher_data_reset[market_publisher_data_reset['Channel'].isin(['Display',
                                                                                                       'Search',
                                                                                                       'Social'])]

        market_publisher_data_reset = market_publisher_data_reset.drop(remove_row_platform.index, axis=0)
        market_publisher_data_reset.rename(columns={"New Market": "Market", "Channel": "Platform"}, inplace=True)
        self.market_publisher_other_than_us = market_publisher_data_reset

    def market_publisher_data_us(self):
        self.read_lead_content_us = self.read_lead_content
        self.read_lead_content_us = self.read_lead_content_us[(self.read_lead_content_us['Date'].dt.year ==
                                                               self.last_year) &
                                                              (self.read_lead_content_us['Date'].dt.month ==
                                                               self.last_month)]

        us_publisher_data = [self.read_lead_content_us, self.read_tableau_advertiser_mapping]
        merged_us_publisher_data = reduce(lambda left, right: pd.merge(left, right, on='Market'), us_publisher_data)

        us_ca_publisher_data = pd.pivot_table(merged_us_publisher_data, index=['New Market', 'Channel', 'Site'],
                                              values=['Conversions', 'Spend Local'], aggfunc=np.sum)

        us_ca_publisher_data_reset = us_ca_publisher_data.reset_index()
        remove_row_platform_us = us_ca_publisher_data_reset[us_ca_publisher_data_reset['Channel'].isin(['Display',
                                                                                                        'Search',
                                                                                                        'Social'])]

        us_ca_publisher_data_reset = us_ca_publisher_data_reset.drop(remove_row_platform_us.index, axis=0)
        us_ca_publisher_data_reset.rename(columns={"New Market": "Market", "Channel": "Platform"}, inplace=True)
        self.final_us_ca_publisher_data = us_ca_publisher_data_reset

    def pub_data_uk(self):
        self.publisher_data_uk.rename(columns={"NewWeek": "Week", "WorkbookName": "Account Name",
                                               "NConversions": "Conversions"}, inplace=True)
        self.uk_pub_data_reset = self.publisher_data_uk

        # uk_pub_data = pd.pivot_table(self.publisher_data_uk,
        #                              index=['Market', 'NewWeek', 'WorkbookName'], values=['Delivered Budget',
        #                                                                                   'NConversions'],
        #                              aggfunc=np.sum)
        #
        # uk_pub_data_reset = uk_pub_data.reset_index()
        # print(list(uk_pub_data_reset))
        # exit()
        # # uk_pub_data_reset = uk_pub_data_reset[(self.read_lead_content_us['Year'].dt.year == self.last_year)]
        # uk_pub_data_reset.rename(columns={"NewWeek": "Week", "WorkbookName": "Account Name"}, inplace=True)
        #
        # self.uk_pub_data_reset = uk_pub_data_reset

    def social_npd_data(self):
        self.read_ndp_data_social = self.read_ndp_data

        internal_data_merge_social = [self.read_ndp_data_social, self.read_tableau_platform_mapping]
        merged_internal_data_social = reduce(lambda left, right: pd.merge(left, right, on='Channel'),
                                             internal_data_merge_social)

        internal_data_merge_market = [merged_internal_data_social, self.read_tableau_advertiser_mapping]
        merged_internal_advertiser_social = reduce(lambda left, right: pd.merge(left, right, on='Market'),
                                                   internal_data_merge_market)

        internal_data_merge_social_platform = [merged_internal_advertiser_social, self.read_social_site_platform]

        merged_internal_social = reduce(lambda left, right: pd.merge(left, right, on='Publisher'),
                                        internal_data_merge_social_platform)

        internal_data_social = merged_internal_social[(merged_internal_social['Platform'] == 'Social')]

        social_internal_pivot = pd.pivot_table(internal_data_social, index=['New Market', 'Social Platform'],
                                               values=['Impressions', 'Clicks', 'Spend Local', 'Conversions'],
                                               aggfunc=np.sum)

        social_internal_pivot_reset = social_internal_pivot.reset_index()

        social_internal_pivot_reset.rename(columns={"New Market": "Market"}, inplace=True)

        self.social_internal_pivot_reset = social_internal_pivot_reset

    def twitter_data_player(self):
        twitter_data_player = pd.pivot_table(self.twitter_data, index=['Market'], values=['Impressions',
                                                                                          'Clicks',
                                                                                          'Spend',
                                                                                          'Conversions'],
                                             aggfunc=np.sum)

        twitter_data_player_reset = twitter_data_player.reset_index()

        self.twitter_data_player_reset = twitter_data_player_reset


if __name__ == "__main__":
    object_ndp_writer = NdpDataPlayer()
