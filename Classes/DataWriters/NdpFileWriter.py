# !/usr/bin/python
# coding=utf-8

from Classes.LoggerFile.LogFile import logger
from Classes.DataManipulaters.NdpDataPlayer import NdpDataPlayer


class NdpFileWriter(NdpDataPlayer):

    def __init__(self):
        super(NdpFileWriter, self).__init__()

    def writing_conversion(self):
        logger.info("Start Writing Internal Conversions")
        write_internal_data = self.internal_conversions_new.to_excel(self.writer_file, sheet_name='Conversions',
                                                                     index=False, startrow=1, startcol=1)
        logger.info("Done")

        logger.info("Start Writing Static Conversion")
        writing_static_conversion = self.data_static_conversion_new.to_excel(self.writer_file, sheet_name='Conversions',
                                                                             index=False, startrow=1,
                                                                             startcol=self.internal_conversions_new.
                                                                             shape[1] + 2)

        logger.info("Done")

        logger.info("Start Writing Dynamic Conversion")
        writing_dynamic_conversion = self.dynamic_conversion.to_excel(self.writer_file, sheet_name='Conversions',
                                                                      index=False, startrow=1,
                                                                      startcol=self.internal_conversions_new.
                                                                      shape[1] + 2 + self.data_static_conversion_new.
                                                                      shape[1] + 1)
        logger.info("Done")

    def writing_performance(self):

        logger.info("Writing Internal Performance Data")
        writing_internal_performance = self.internal_data_performance.to_excel(self.writer_file,
                                                                               index=False, sheet_name=
                                                                               'Display Performance', startcol=1,
                                                                               startrow=1)

        logger.info("Done")

        logger.info("Writing DBM Performance Data")
        writing_dcm_performance = self.dbm_dcm_data.to_excel(self.writer_file, index=False,
                                                             sheet_name='Display Performance', startrow=1,
                                                             startcol=self.internal_data_performance.shape[1]+2)

        logger.info("Done")

    def formatting_conversions(self):
        workbook = self.writer_file.book
        worksheet = self.writer_file.sheets['Conversions']
        worksheet.hide_gridlines(2)
        worksheet.set_column("A:A", 2)
        worksheet.set_zoom(75)
        merge_format = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'fg_color': 'yellow'})
        worksheet.merge_range("B1:J1", 'Internal Conversion', merge_format)
        worksheet.merge_range("L1:S1", 'Static Conversion', merge_format)
        worksheet.merge_range("U1:AA1", 'Dynamic Conversion', merge_format)
        worksheet.freeze_panes(1, 1)
        border_row = workbook.add_format({"border": 1, "num_format": "#,##0"})
        format_header = workbook.add_format({"bold": True, "bg_color": "#00B0F0", "border": 1})

        worksheet.conditional_format(1, 1, 1, self.internal_conversions_new.shape[1], {"type": "no_blanks",
                                                                                       "format": format_header})

        worksheet.conditional_format(1, self.internal_conversions_new.shape[1] + 1, 1, 1 +
                                     self.internal_conversions_new.shape[1] + 1 +
                                     self.data_static_conversion_new.shape[1],
                                     {"type": "no_blanks", "format": format_header})

        worksheet.conditional_format(1, 1 + self.internal_conversions_new.shape[1] + 1 +
                                     self.data_static_conversion_new.shape[1] + 1, 1,
                                     self.internal_conversions_new.shape[1] + self.data_static_conversion_new.shape[1] +
                                     self.dynamic_conversion.shape[1] + 2,
                                     {"type": "no_blanks", "format": format_header})

        worksheet.conditional_format(2, 1, self.internal_conversions_new.shape[0] + 1,
                                     self.internal_conversions_new.shape[1],
                                     {"type": "no_blanks", "format": border_row})

        worksheet.conditional_format(2, self.internal_conversions_new.shape[1] + 1,
                                     self.data_static_conversion_new.shape[0] + 1,
                                     1 + self.internal_conversions_new.shape[1] + 1 +
                                     self.data_static_conversion_new.shape[1],
                                     {"type": "no_blanks", "format": border_row})

        worksheet.conditional_format(2, 1 + self.internal_conversions_new.shape[1] + 1 +
                                     self.data_static_conversion_new.shape[1] + 1,
                                     self.dynamic_conversion.shape[0] + 1,
                                     self.internal_conversions_new.shape[1] + self.data_static_conversion_new.shape[1] +
                                     self.dynamic_conversion.shape[1] + 2,
                                     {"type": "no_blanks", "format": border_row})

    def formatting_performance(self):
        workbook = self.writer_file.book
        worksheet = self.writer_file.sheets['Display Performance']
        worksheet.hide_gridlines(2)
        worksheet.set_column("A:A", 2)
        worksheet.set_zoom(75)
        merge_format = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'fg_color': 'yellow'})
        worksheet.merge_range("B1:E1", 'Internal Performance', merge_format)
        worksheet.merge_range("G1:J1", 'DBM Performance', merge_format)
        worksheet.freeze_panes(1, 1)
        border_row = workbook.add_format({"border": 1, "num_format": "#,##0"})
        format_header = workbook.add_format({"bold": True, "bg_color": "#00B0F0", "border": 1})

        worksheet.conditional_format(1, 1, self.internal_data_performance.shape[0]+1,
                                     self.internal_data_performance.shape[1] + 1, {"type": "no_blanks",
                                                                                   "format": border_row})

        worksheet.conditional_format(1, 1, 1, self.internal_data_performance.shape[1] + 1,
                                     {"type": "no_blanks", "format": format_header})

        worksheet.conditional_format(1, self.internal_data_performance.shape[1] + 2,
                                     1, self.internal_data_performance.shape[1] +
                                     2 + self.dbm_dcm_data.shape[1] + 1, {"type": "no_blanks",
                                                                          "format": format_header})

        worksheet.conditional_format(1, self.internal_data_performance.shape[1] + 2, self.dbm_dcm_data.shape[0]+1,
                                     self.internal_data_performance.shape[1] + 2 + self.dbm_dcm_data.shape[1] + 1,
                                     {"type": "no_blanks", "format": border_row})

    def main(self):
        self.writing_conversion()
        self.writing_performance()
        self.formatting_conversions()
        self.formatting_performance()
        self.save_and_close_writer()


if __name__ == "__main__":
    object_Ndp_writer = NdpFileWriter()
    object_Ndp_writer.main()
