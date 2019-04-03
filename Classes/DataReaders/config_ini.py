# !/usr/bin/python
# coding=utf-8

"""Configuration of absolute paths"""
import configparser


class Config(object):
    """
    read mediaops.ini file
    """
    def __init__(self):
        """
        Path
        :return:
        """

        config_file = configparser.ConfigParser()
        config_file.read('/home/Dharmendra/mediaops/Classes/DataReaders/mediaops.ini')

        section_key = []
        section_value = []
        for each_section in config_file.sections():
            for (each_key, each_val) in config_file.items(each_section):
                section_key.append(str(each_key))
                section_value.append(str(each_val))

        self.section_key = section_key
        # print(self.section_key)
        # print(self.section_key[6])
        self.section_value = section_value
        # print(self.section_value[5])


if __name__ == "__main__":
    obj_read = Config()
