# coding=utf-8
# !/usr/bin/env python
from config import Config
from NdpDataFile import NdpDataFile
from NdpDataReader import NdpDataReader


if __name__ == "__main__":
    obj_read = Config()

    object_NdpDataFile = NdpDataFile()
    object_NdpDataFile.save_and_close_writer()
