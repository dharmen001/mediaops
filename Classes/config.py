# !/usr/bin/python
# coding=utf-8

"""Configuration of absolute paths"""
import configparser


class Config(object):
    """
    read bi.ini file
    """
    def __init__(self):
        """
        Path
        :return:
        """
        config_file = configparser.ConfigParser()
        config_file.read('C:/mediaops/config/mediaops.ini')

        self.sqlPath = config_file['mediaops-properties']['sqlPath']
        self.mazdaInputPath = config_file['mediaops-properties']['mazdaInputPath']

        section_key = []
        section_value = []
        for each_section in config_file.sections():
            for (each_key, each_val) in config_file.items(each_section):
                section_key.append(str(each_key))
                section_value.append(str(each_val))

        self.section_key = section_key
        # print(self.section_key)
        # print(self.section_key[2])
        self.section_value = section_value
        # print(self.section_value[2])


if __name__ == "__main__":
    obj_read = Config()
