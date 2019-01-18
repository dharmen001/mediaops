# coding=utf-8
"""
Combining Xlsx File
"""
import pandas as pd
import glob
from Classes.DataReaders.config_ini import Config


class SageData(Config):

    def __init__(self):
        super(SageData, self).__init__()
        self.all_data = None
        self.writer = pd.ExcelWriter(self.section_value[8] + 'output.xlsx',
                                     engine="xlsxwriter", datetime_format="YYYY-MM-DD")

    def read_sage(self):
        all_data = pd.DataFrame()
        for f in glob.glob(self.section_value[7] + "*.xlsx"):
            df = pd.read_excel(f, sheet_name=None, ignore_index=None)
            all_data = all_data.append(df, ignore_index=True)

        self.all_data = all_data

    def dump_sage(self):

        df = self.all_data.to_excel(self.writer,
                                    index=False, header=True)

    def save_and_close_writer(self):
        self.writer.save()
        self.writer.close()

    def main(self):
        self.read_sage()
        self.dump_sage()
        self.save_and_close_writer()


if __name__ == "__main__":
    obj = SageData()
    obj.main()

















