# !/usr/bin/python
# coding=utf-8

import pandas as pd
from LogFile import logger
from NdpDataReader import NdpReader


class NdpWriter(NdpReader):

    def __init__(self):
        # Inheriting Reader Class
        super(NdpWriter, self).__init__()

    def internal_data(self):
        # Removing unconditional rows from NDP Tableau Raw Data

        logger.info()
        remove_row_channel = self.read_ndp_data[self.read_ndp_data['Channel'].isin(['CONTENT SYNDICATION', 'OTHER',
                                                                                    'LEAD AGGREGATOR'])]
        self.read_ndp_data = self.read_ndp_data.drop(remove_row_channel.index, axis=0)

        remove_row_market = self.read_ndp_data[self.read_ndp_data['Market'].isin(['BR'])]

        self.read_ndp_data = self.read_ndp_data.drop(remove_row_market.index, axis=0)

    def market_mapping_internal_data(self):
        pass


if __name__ == "__main__":
    object_ndp_writer = NdpWriter()
    object_ndp_writer.internal_data()
