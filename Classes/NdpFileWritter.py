# !/usr/bin/python
# coding=utf-8

import pandas as pd
from LogFile import logger
from NdpDataReader import NdpReader
from functools import reduce
import numpy as np


class NdpWriter(NdpReader):

    def __init__(self):
        # Inheriting Reader Class
        super(NdpWriter, self).__init__()
        self.merged_internal_data_advertiser = None
        self.static_conversions_report = None
        self.internal_conversions_new = None
        self.activity_with_static_conversion = None
        self.data_static_conversion_new = None

    def internal_data(self):
        # Removing unconditional rows from NDP Tableau Raw Data

        remove_row_channel = self.read_ndp_data[self.read_ndp_data['Channel'].isin(['CONTENT SYNDICATION', 'OTHER',
                                                                                    'LEAD AGGREGATOR'])]
        self.read_ndp_data = self.read_ndp_data.drop(remove_row_channel.index, axis=0)

        remove_row_market = self.read_ndp_data[self.read_ndp_data['Market'].isin(['BR'])]

        self.read_ndp_data = self.read_ndp_data.drop(remove_row_market.index, axis=0)

    def market_mapping_internal_data(self):
        internal_data_merge_platform = [self.read_ndp_data, self.read_tableau_platform_mapping]
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

        self.internal_conversions_new = internal_conversions_new

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
        self.activity_with_static_conversion['Application'] = np.select([mask_application], [choice_application], default=0)
        self.activity_with_static_conversion['Contact'] = np.select([mask_cont], [choice_cont], default=0)
        self.activity_with_static_conversion['Download'] = np.select([mask_download], [choice_download], default=0)
        self.activity_with_static_conversion['Purchase'] = np.select([mask_ibuy], [choice_ibuy], default=0)
        self.activity_with_static_conversion['Free Trial'] = np.select([mask_itrs], [choice_itrs], default=0)
        self.activity_with_static_conversion['Others'] = self.activity_with_static_conversion['Application'] + \
                                                         self.activity_with_static_conversion['Contact'] + \
                                                         self.activity_with_static_conversion['Download'] + \
                                                         self.activity_with_static_conversion['Purchase'] + \
                                                         self.activity_with_static_conversion['Free Trial']

        self.activity_with_static_conversion['Other Conversions'] = np.select([self.activity_with_static_conversion['Others']==0],
                                                                              [choice_other],default=0)


        data_static_conversion = pd.pivot_table(self.activity_with_static_conversion, index=['Country', 'Platform'],
                                                values=['Application', 'Contact', 'Download', 'Purchase',
                                                        'Free Trial','Other Conversions'],
                                                aggfunc=np.sum)

        data_static_conversion_new = data_static_conversion.reset_index()

        self.data_static_conversion_new = data_static_conversion_new

    def platfrom_mapping_dynamic(self):
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

        self.dynamic_conversion_df['Sub'] = np.select([mask_sub],[choice_sub],default=0)
        self.dynamic_conversion_df['Quo'] = np.select([mask_quo],[choice_quo],default=0)
        self.dynamic_conversion_df['Eml'] = np.select([mask_eml],[choice_eml],default=0)
        self.dynamic_conversion_df['Res'] = np.select([mask_res],[choice_res],default=0)
        self.dynamic_conversion_df['Add'] = np.select([mask_add],[choice_add],default=0)
        self.dynamic_conversion_df['Ot'] = np.select([mask_ot],[choice_ot],default=0)
        self.dynamic_conversion_df['Con'] = np.select([mask_con],[choice_con],default=0)
        self.dynamic_conversion_df['Eve'] = np.select([mask_eve],[choice_eve],default=0)
        self.dynamic_conversion_df['Art'] = np.select([mask_art],[choice_art],default=0)
        self.dynamic_conversion_df['Pdf'] = np.select([mask_pdf],[choice_pdf],default=0)
        self.dynamic_conversion_df['Vid'] = np.select([mask_vid],[choice_vid],default=0)
        self.dynamic_conversion_df['Inf'] = np.select([mask_inf],[choice_inf],default=0)
        self.dynamic_conversion_df['Img'] = np.select([mask_img],[choice_img],default=0)
        self.dynamic_conversion_df['Temp'] = np.select([mask_temp],[choice_temp], default=0)
        self.dynamic_conversion_df['Dem'] = np.select([mask_dem],[choice_dem], default=0)
        self.dynamic_conversion_df['Trl'] = np.select([mask_trl],[choice_trl],default=0)
        self.dynamic_conversion_df['Tool'] = np.select([mask_tool],[choice_tool],default=0)
        self.dynamic_conversion_df['Ibuy'] = np.select([mask_ibuy],[choice_ibuy],default=0)

        self.dynamic_conversion_df['Contact'] = self.dynamic_conversion_df['Sub'] + self.dynamic_conversion_df['Quo'] + \
                                                self.dynamic_conversion_df['Eml'] + self.dynamic_conversion_df['Res'] + \
                                                self.dynamic_conversion_df['Add'] + self.dynamic_conversion_df['Ot'] + \
                                                self.dynamic_conversion_df['Con'] + self.dynamic_conversion_df['Eve']

        self.dynamic_conversion_df['Download'] = self.dynamic_conversion_df['Art'] + self.dynamic_conversion_df['Pdf'] + \
                                                 self.dynamic_conversion_df['Vid'] + self.dynamic_conversion_df['Inf'] + \
                                                 self.dynamic_conversion_df['Img'] + self.dynamic_conversion_df['Temp']

        self.dynamic_conversion_df['Free Trial'] = self.dynamic_conversion_df['Dem'] + self.dynamic_conversion_df['Trl'] + \
                                                   self.dynamic_conversion_df['Tool']

        self.dynamic_conversion_df['Purchase'] = self.dynamic_conversion_df['Ibuy']

        self.dynamic_conversion_df['Total'] = self.dynamic_conversion_df['Contact'] + self.dynamic_conversion_df['Download'] + \
                                              self.dynamic_conversion_df['Free Trial'] + self.dynamic_conversion_df['Purchase']

        self.dynamic_conversion_df['Other Dynamic Conversions'] = np.select([self.dynamic_conversion_df['Total']==0],
                                                                            [self.dynamic_conversion_df['Total Conversions']],
                                                                            default=0)


        dynamic_conversion_final = pd.pivot_table(self.dynamic_conversion_df, index=['Market', 'Platform'],
                                                  values=['Contact', 'Download', 'Free Trial', 'Purchase',
                                                          'Other Dynamic Conversions'], aggfunc=np.sum)

        dynamic_conversion = dynamic_conversion_final.reset_index()

        self.dynamic_conversion = dynamic_conversion

    def writing_conversion(self):
        start_col_internal = self.internal_conversions_new.shape[1]
        start_col_static  = self.data_static_conversion_new.shape[1]
        write_internal_data = self.internal_conversions_new.to_excel(self.writer_file, sheet_name='Conversions',
                                                                     index=False, startrow=1, startcol=1)

        writing_static_conversion = self.data_static_conversion_new.to_excel(self.writer_file, sheet_name='Conversions',
                                                                    index=False, startrow=1,
                                                                    startcol=start_col_internal+2)

        writing_dynamic_conversion = self.dynamic_conversion.to_excel(self.writer_file, sheet_name = 'Conversions',
                                                             index=False, startrow = 1,
                                                             startcol = start_col_internal+2+start_col_static+1)

        workbook = self.writer_file.book
        worksheet = self.writer_file.sheets['Conversions']
        worksheet.hide_gridlines(2)
        worksheet.set_column("A:A", 2)
        worksheet.set_zoom(75)
        merge_format = workbook.add_format({'bold': 1,'border': 1,'align': 'center','valign': 'vcenter','fg_color': 'yellow'})
        worksheet.merge_range("B1:J1", 'Internal Conversion', merge_format)
        worksheet.merge_range("L1:S1", 'Static Conversion', merge_format)
        worksheet.merge_range("U1:AA1", 'Dynamic Conversion', merge_format)

    def main(self):
        self.internal_data()
        self.market_mapping_internal_data()
        self.market_mapping_static_conversion()
        self.add_conversion_static_column()
        self.platfrom_mapping_dynamic()
        self.add_conversion_dynamic()
        self.writing_conversion()
        self.save_and_close_writer()


if __name__ == "__main__":
    object_ndp_writer = NdpWriter()
    object_ndp_writer.main()
