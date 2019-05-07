# coding=utf-8
# !/usr/bin/env python
# from config import Config
from Classes.DataManipulaters.RemoveExcelFiles import RemoveExcelFile
from Classes.DataReaders.OutlookNdpDownload import Outlook
from Classes.DataReaders.NdpGdriveData import NdpGrdriveDate
from Classes.DataWriters.NdpFileWriter import NdpFileWriter
# from Classes.DataFetchers.twitter import Twitter
# from Classes.DataFetchers.Facebook import Facebook
from Classes.DataReaders.config_ini import Config
from Classes.LoggerFile.LogFile import logger


if __name__ == "__main__":
    C = Config()
    logger.info("Making UK Folder Empty")
    object_remove_uk = RemoveExcelFile(C.section_value[14], '*.xlsx')
    logger.info("Done UK Folder Empty")

    logger.info("Start Downloading UK Files from google drive")
    object_Ndp_g_drive = NdpGrdriveDate()
    object_Ndp_g_drive.main()
    logger.info("Done Downloading UK Files from google drive")

    logger.info("Start Downloading Emails Files from Scheduled Emails")
    object_outlook = Outlook()
    object_outlook.main()
    logger.info("Done Downloading Emails Files from Scheduled Emails")

    # logger.info("Making Twitter Folder Empty")
    # object_remove_twitter = RemoveExcelFile(C.section_value[19], '*.xlsx')
    # logger.info("Done Twitter Folder Empty")
    # logger.info("Start Downloading Twitter Files from Twitter")
    # object_Ndp_twitter = Twitter()
    # object_Ndp_twitter.main()
    # logger.info("Done Downloading Twitter Files from Twitter")
    #
    # logger.info("Making Facebook Folder Empty")
    # object_remove_facebook = RemoveExcelFile(C.section_value[24], '*.csv')
    # logger.info("Done Facebook Folder Empty")
    # logger.info("Start Downloading Facebook Files from Facebook")
    # object_Ndp_Facebook = Facebook()
    # object_Ndp_Facebook.main()
    # logger.info("Done Downloading Facebook Files from Facebook")

    object_ndp_data_writer = NdpFileWriter()
    object_ndp_data_writer.main()

    object_ndp_data_writer.save_and_close_writer()


