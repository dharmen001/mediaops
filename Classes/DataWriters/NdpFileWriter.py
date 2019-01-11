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

    def writing_publisher_internal(self):
        logger.info("Writing Internal Publisher Data")
        writing_internal_publisher = self.internal_publisher_data_new.to_excel(self.writer_file,
                                                                               index=False, sheet_name="Publisher "
                                                                                                       "Provided Data",
                                                                               startrow=1, startcol=1)

        logger.info("Done")

    def writing_publisher_market_other_us(self):
        logger.info("Writing Other than US/CA Publisher Data")

        writing_us_ca_publisher_other = self.market_publisher_other_than_us.to_excel(self.writer_file, index=False,
                                                                                     sheet_name=
                                                                                     "Publisher Provided Data",
                                                                                     startrow=1,
                                                                                     startcol=self.
                                                                                     internal_publisher_data_new.
                                                                                     shape[1]+2)
        logger.info("Done")

    def writing_publisher_market_us(self):
        logger.info("Writing US/CA Publisher Data")

        writng_us_ca_publisher_data = self.final_us_ca_publisher_data.to_excel(self.writer_file,
                                                                               index=False, sheet_name="Publisher "
                                                                                                       "Provided Data",
                                                                               startrow=self.
                                                                               internal_publisher_data_new.shape[0]+4,
                                                                               startcol=1)

        logger.info("Done")

    def writing_publisher_uk(self):

        logger.info("Writing UK Publisher Data")
        writing_uk_pub_data = self.uk_pub_data_reset.to_excel(self.writer_file, index=False,
                                                              sheet_name="Publisher Provided Data",
                                                              startrow=self.internal_publisher_data_new.shape[0]+4,
                                                              startcol=self.uk_pub_data_reset.shape[1]+4)

        logger.info("Done")

    def writing_social_internal(self):
        logger.info("Writing Social Data")
        writing_tableau_social_data = self.social_internal_pivot_reset.to_excel(self.writer_file,
                                                                                index=False,
                                                                                sheet_name="Social Performance",
                                                                                startrow=1, startcol=1)

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

    def formatting_publisher(self):
        workbook = self.writer_file.book
        worksheet = self.writer_file.sheets['Publisher Provided Data']
        worksheet.hide_gridlines(2)
        worksheet.set_column("A:A", 2)
        worksheet.set_zoom(75)
        merge_format = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'fg_color': 'yellow'})
        worksheet.merge_range("B1:H1", 'Internal Publisher Data', merge_format)
        worksheet.merge_range("J1:P1", 'Publisher Data', merge_format)
        worksheet.merge_range("B{}:F{}".format(self.internal_publisher_data_new.shape[0]+4,
                                               self.internal_publisher_data_new.shape[0]+4), "US CA Publisher Data",
                              merge_format)
        worksheet.merge_range("J{}:N{}".format(self.internal_publisher_data_new.shape[0]+4,
                                               self.internal_publisher_data_new.shape[0]+4), "UK Publisher Data",
                              merge_format)
        worksheet.freeze_panes(1, 1)
        border_row = workbook.add_format({"border": 1, "num_format": "#,##0"})
        format_header = workbook.add_format({"bold": True, "bg_color": "#00B0F0", "border": 1})

        worksheet.conditional_format(1, 1, 1,
                                     self.internal_publisher_data_new.shape[1]+1, {"type": "no_blanks",
                                                                                   "format": format_header})

        worksheet.conditional_format(1, 1, self.internal_publisher_data_new.shape[0]+1,
                                     self.internal_publisher_data_new.shape[1]+1, {"type":  "no_blanks",
                                                                                   "format": border_row})

        worksheet.conditional_format(1, self.internal_publisher_data_new.shape[1]+2, 1,
                                     self.internal_data_performance.shape[1] + 2 +
                                     self.market_publisher_other_than_us.shape[1]+2,
                                     {"type": "no_blanks", "format": format_header})

        worksheet.conditional_format(1, self.internal_publisher_data_new.shape[1]+2,
                                     self.market_publisher_other_than_us.shape[0]+1,
                                     self.internal_publisher_data_new.shape[1] + 2 +
                                     self.market_publisher_other_than_us.shape[0]+3, {"type": "no_blanks",
                                                                                      "format": border_row})

        worksheet.conditional_format(self.internal_publisher_data_new.shape[0]+4, 1,
                                     self.internal_publisher_data_new.shape[0]+4,
                                     self.final_us_ca_publisher_data.shape[1]+1, {"type": "no_blanks",
                                                                                  "format": format_header})

        worksheet.conditional_format(self.internal_publisher_data_new.shape[0]+4, 1,
                                     self.internal_publisher_data_new.shape[0] +
                                     self.final_us_ca_publisher_data.shape[0] + 5,
                                     self.final_us_ca_publisher_data.shape[1]+1, {"type": "no_blanks",
                                                                                  "format": border_row})

        worksheet.conditional_format(self.internal_publisher_data_new.shape[0]+4,
                                     self.final_us_ca_publisher_data.shape[1] + 4,
                                     self.internal_publisher_data_new.shape[0] + 4,
                                     self.final_us_ca_publisher_data.shape[1] + 5 + self.uk_pub_data_reset.shape[1],
                                     {"type": "no_blanks", "format": format_header})

        worksheet.conditional_format(self.final_us_ca_publisher_data.shape[1] + 5,
                                     self.final_us_ca_publisher_data.shape[1] + 4,
                                     self.internal_publisher_data_new.shape[0] +
                                     self.uk_pub_data_reset.shape[0] +
                                     5, self.final_us_ca_publisher_data.shape[1] + 5 +
                                     self.uk_pub_data_reset.shape[1],
                                     {"type": "no_blanks", "format": border_row})

    def formatting_social(self):
        workbook = self.writer_file.book
        worksheet = self.writer_file.sheets['Social Performance']
        worksheet.hide_gridlines(2)
        worksheet.set_column("A:A", 2)
        worksheet.set_zoom(75)
        merge_format = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'fg_color': 'yellow'})
        format_header = workbook.add_format({"bold": True, "bg_color": "#00B0F0", "border": 1})
        border_row = workbook.add_format({"border": 1, "num_format": "#,##0"})

        worksheet.merge_range("B1:G1", 'Internal Social Performance', merge_format)

        worksheet.conditional_format(1, 1, 1,
                                     self.social_internal_pivot_reset.shape[1] + 1,
                                     {"type": "no_blanks", "format": format_header})

        worksheet.conditional_format(2, 1, self.social_internal_pivot_reset.shape[0] + 2,
                                     self.social_internal_pivot_reset.shape[1] + 1, {"type": "no_blanks",
                                                                                     "format": border_row})

    def main(self):
        self.writing_conversion()
        self.writing_performance()
        self.writing_publisher_internal()
        self.writing_publisher_market_other_us()
        self.writing_publisher_market_us()
        self.writing_publisher_uk()
        self.writing_social_internal()
        self.formatting_conversions()
        self.formatting_performance()
        self.formatting_publisher()
        self.formatting_social()
        # self.save_and_close_writer()


if __name__ == "__main__":
    object_Ndp_writer = NdpFileWriter()
    object_Ndp_writer.main()
