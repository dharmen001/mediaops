# coding=utf-8
# !/usr/bin/env python
# from config import Config
from NdpDataReader import NdpReader
from OutlookNdpDownload import Outlook
from NdpGdriveData import NdpGrdriveDate


if __name__ == "__main__":

    object_outlook = Outlook()
    object_outlook.main()

    object_Ndp_g_drive = NdpGrdriveDate()
    object_Ndp_g_drive.main()

    object_ndp_data_reader = NdpReader()
    object_ndp_data_reader.main()

    object_ndp_data_reader.save_and_close_writer()


