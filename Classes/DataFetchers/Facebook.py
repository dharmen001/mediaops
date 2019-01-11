from selenium import webdriver
import datetime
import time
from Classes.DataReaders.config_ini import Config
import glob
import os


class Facebook(Config):

    def __init__(self):
        super(Facebook, self).__init__()
        self.driver = None
        self.tail = None
        self.head = None
        self.today = datetime.date.today()
        self.first = self.today.replace(day=1)
        self.last_day = self.first - datetime.timedelta(days=1)
        self.last_day_month = self.last_day.strftime("%Y-%m-%d")
        self.first_day_month = '01'
        self.last_month = self.last_day.strftime("%Y-%m")

    def login_facebook(self, username, password):
        chrome_options = webdriver.ChromeOptions()
        preference = {"download.default_directory": self.section_value[24]}

        chrome_options.add_experimental_option("prefs", preference)
        self.driver = webdriver.Chrome(self.section_value[20], chrome_options=chrome_options)
        self.driver.get(self.section_value[21])

        username_field = self.driver.find_element_by_class_name("js-username-field")
        password_field = self.driver.find_element_by_class_name("js-password-field")

        username_field.send_keys(username)
        self.driver.implicitly_wait(10)

        password_field.send_keys(password)
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("EdgeButtom--medium").click()
        self.driver.implicitly_wait(10)


if __name__ == "__main__":
    object_twitter = Facebook()
    object_twitter.login_facebook("india.adops.sage@gmail.com", "Ogilvy@123")
