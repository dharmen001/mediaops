# coding=utf-8
# !/usr/bin/env python

from Advertiser_list import AdvertiserList
from JiraWrapper import Jira
from config_ini import Config


if __name__ == "__main__":
    obj_read = Config()

    object_Advertiser = AdvertiserList()
    object_Advertiser.main()

    object_JiraWrapper = Jira(username=obj_read.section_value[5], password=obj_read.section_value[6])
    object_JiraWrapper.main()
