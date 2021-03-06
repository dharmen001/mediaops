#!/usr/bin/env python
# encoding=utf8
#
# Copyright 2019 Dharmendra. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This class file do data cleaning for all adwords account.

To get download adwords report fields, run GetAdwordsCampaign.py.

"""
import os
import datetime
import pandas.io.common
import pandas as pd
from Classes.DataManipulaters.RemoveExcelFiles import RemoveExcelFile

from Classes.LoggerFile.LogFile import logger
from Classes.DataReaders.config_ini import Config
import pandas.io.formats.excel
pandas.io.formats.excel.header_style = None


class AdwordsFileReader(Config):

    def __init__(self):
        super(AdwordsFileReader, self).__init__()

    def file_reader(self):
        logger.info("Start Reading:-  Adwords files at " +
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        path = self.section_value[35]
        report_path = self.section_value[37]
        files = os.listdir(path)

        files_csv = [f for f in files if f[-3:] == 'csv']

        for f in files_csv:
            logger.info('Start Reading filename: - ' + f)
            try:
                data = pd.read_csv(path + f, skiprows=1, skipfooter=1, engine='python', encoding="utf-8")
                data['WorkbookName'] = f
                data_new = pd.pivot_table(data, index=['Campaign'], values=['Clicks', 'Cost'], aggfunc=pd.np.sum)
                adwords_data = data_new.reset_index()
                adwords_data = adwords_data[(adwords_data[['Clicks']] != 0).all(axis=1)]
                adwords_data['Cost'] = adwords_data['Cost']/1000000
                adwords_file_creation = pd.ExcelWriter(report_path + os.path.splitext(f)[0] + ".xlsx", engine="xlsxwriter",
                                                       datetime_format="YYYY-MM-DD")
                adwords_data.to_excel(adwords_file_creation, index=False, startrow=6)

                data_info = pd.read_csv(self.section_value[34] + 'Client_id_mcc.csv', engine='python', encoding="utf-8")

                data_info = data_info.drop('MCCID', 1)
                # data_info_new = data_info.transpose()
                data_info_new = data_info.set_index('Client').T
                # data_info_new.reset_index()
                print(data_info_new)
                # exit()
                # for index, row in data_info.iterrows():
                data_info_new.to_excel(adwords_file_creation, index=True, startrow=0, startcol=0)
                workbook = adwords_file_creation.book
                worksheet = adwords_file_creation.sheets['Sheet1']
                worksheet.hide_gridlines(2)
                worksheet.set_zoom(75)
                format_header = workbook.add_format({"bold": True, "bg_color": "#00B0F0", "border": 1})
                worksheet.conditional_format(6, 0, 6, adwords_data.shape[1], {"type": "no_blanks",
                                                                              "format": format_header})

                border_row = workbook.add_format({"border": 1})
                bold_format = workbook.add_format({"bold": True, "bg_color": "#00B0F0", "border": 1,
                                                   "num_format": "#,##0"})
                worksheet.conditional_format(7, 0, adwords_data.shape[0]+7, adwords_data.shape[1],
                                             {"type": "no_blanks", "format": border_row})

                number_format = workbook.add_format({"num_format": "#,##0"})
                dollar_format = workbook.add_format({"num_format": "#,##0.00"})
                worksheet.conditional_format(7, 1, adwords_data.shape[0]+7, 1,
                                             {"type": "no_blanks", "format": number_format})

                worksheet.conditional_format(7, 2, adwords_data.shape[0] + 7, 2,
                                             {"type": "no_blanks", "format": dollar_format})

                worksheet.write_string(adwords_data.shape[0] + 7, 0, 'Total', bold_format)
                worksheet.write_string(0, 0, 'Client')
                worksheet.write_formula(adwords_data.shape[0] + 7, 1, '=SUM(B{}:B{})'.format(8,
                                                                                             adwords_data.shape[0]+7),
                                        bold_format)
                worksheet.write_formula(adwords_data.shape[0] + 7, 2, '=SUM(C{}:C{})'.format(8,
                                                                                             adwords_data.shape[0]+7),
                                        bold_format)

                adwords_file_creation.save()
                adwords_file_creation.close()
            except (pandas.io.common.EmptyDataError, KeyError):
                pass
                logger.error(f + "is empty")

            logger.info("Done Reading:-  Adwords file " + f + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))

    def remove_csv_files(self):
        csv_file = RemoveExcelFile(self.section_value[35], "*.csv")

    def main(self):
        self.file_reader()
        self.remove_csv_files()


if __name__ == "__main__":
    adwords_client = AdwordsFileReader()
    adwords_client.main()