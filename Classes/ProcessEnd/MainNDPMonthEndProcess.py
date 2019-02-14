# coding=utf-8
# !/usr/bin/env python
# from config import Config
from Classes.DataManipulaters.RemoveExcelFiles import RemoveExcelFile
from Classes.DataReaders.OutlookNdpDownload import Outlook
from Classes.DataReaders.NdpGdriveData import NdpGrdriveDate
from Classes.DataWriters.NdpFileWriter import NdpFileWriter
from Classes.DataFetchers.twitter import Twitter
from Classes.DataFetchers.Facebook import Facebook
from Classes.DataReaders.config_ini import Config


if __name__ == "__main__":
    C = Config()
    object_outlook = Outlook()
    object_outlook.main()

    object_remove_uk = RemoveExcelFile(C.section_value[14], '*.xlsx')
    object_Ndp_g_drive = NdpGrdriveDate()
    object_Ndp_g_drive.main()

    object_remove_twitter = RemoveExcelFile(C.section_value[19], '*.xlsx')
    object_Ndp_twitter = Twitter()
    object_Ndp_twitter.main()

    object_remove_facebook = RemoveExcelFile(C.section_value[24], '*.csv')
    object_Ndp_Facebook = Facebook()
    object_Ndp_Facebook.main()

    object_ndp_data_writer = NdpFileWriter()
    object_ndp_data_writer.main()

    object_ndp_data_writer.save_and_close_writer()


