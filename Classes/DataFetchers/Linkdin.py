from selenium import webdriver
import datetime
import time
from Classes.DataReaders.config_ini import Config
import pandas as pd
import glob
import os


class Linkedin(Config):

    def __init__(self):
        super(Linkedin, self).__init__()
        self.driver = None
        self.tail = None
        self.head = None
        self.today = datetime.date.today()
        self.first = self.today.replace(day=1)
        self.last_day = self.first - datetime.timedelta(days=1)
        self.last_day_month = self.last_day.strftime("%Y-%m-%d")
        self.first_day_month = '01'
        self.last_month = self.last_day.strftime("%Y-%m")

    def login_linkedin(self, username, password):
        chrome_options = webdriver.ChromeOptions()
        preference = {"download.default_directory": self.section_value[24]}

        chrome_options.add_experimental_option("prefs", preference)
        self.driver = webdriver.Chrome(self.section_value[20])
        self.driver.get(self.section_value[27])
        self.driver.implicitly_wait(10)

        username_field = self.driver.find_elements_by_id("username")
        password_field = self.driver.find_elements_by_id("password")

        self.driver.implicitly_wait(10)

        username_field.send_keys(username)
        self.driver.implicitly_wait(10)

        password_field.send_keys(password)
        self.driver.implicitly_wait(10)

    def main(self):
        self.login_linkedin("neo.ayush.sharma@gmail.com", "Neo@1100")


if __name__ == "__main__":
    object_linkedIn = Linkedin()
    object_linkedIn.main()