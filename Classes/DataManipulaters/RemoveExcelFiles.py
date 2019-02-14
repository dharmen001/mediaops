#!/usr/bin/env python
import glob
import os
from Classes.DataReaders.config_ini import Config


class RemoveExcelFile(Config):

    def __init__(self, directory, file_extension):
        super(RemoveExcelFile, self).__init__()
        # directory = self.section_value[14]
        os.chdir(directory)
        files = glob.glob(file_extension)
        for filename in files:
            os.unlink(filename)


if __name__ == "__main__":
    object_remove = RemoveExcelFile("C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/NDPdataDump/UK Google Drive Files/",
                                    '*.xlsx')
