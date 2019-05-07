from selenium import webdriver
import datetime
import time
from Classes.DataReaders.config_ini import Config
import pandas as pd
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
        self.driver.get(self.section_value[25])

        username_field = self.driver.find_element_by_id("email")
        password_field = self.driver.find_element_by_id("pass")

        username_field.send_keys(username)
        self.driver.implicitly_wait(10)

        password_field.send_keys(password)
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_id("loginbutton").click()
        self.driver.implicitly_wait(10)

    def each_market_report_india(self):
        market_facebook_report_india = pd.read_csv(self.section_value[9] + "facebookmarketurlindia.csv")
        for i, j in zip(market_facebook_report_india.iloc[:, 2], market_facebook_report_india.iloc[:, 1]):
            self.driver.get(i)
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_id("export_button").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_xpath("//*[contains(text(), 'Export as .csv')]").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_class_name("_66ul").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_xpath("//*[contains(@class, '_271k _271m _1qjd layerConfirm')]").click()
            time.sleep(10)
            newest = max(glob.iglob(self.section_value[24] + '*.csv'), key=os.path.getctime)
            head, tail = os.path.split(newest)
            self.tail = tail
            self.head = head
            os.rename(os.path.join(self.head, self.tail), os.path.join(self.head,
                                                                       self.tail.replace(self.tail, j + ".csv")))

    def each_market_report_gds(self):
        market_facebook_report_india = pd.read_csv(self.section_value[9] + "facebookmarketurlgds.csv")
        for i, j in zip(market_facebook_report_india.iloc[:, 2], market_facebook_report_india.iloc[:, 1]):
            self.driver.get(i)
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_id("export_button").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_xpath("//*[contains(text(), 'Export as .csv')]").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_class_name("_66ul").click()
            self.driver.implicitly_wait(30)
            self.driver.find_element_by_xpath("//*[contains(@class, '_271k _271m _1qjd layerConfirm')]").click()
            time.sleep(10)
            # finding the latest modified file
            newest = max(glob.iglob(self.section_value[24] + '*.csv'), key=os.path.getctime)
            head, tail = os.path.split(newest)
            self.tail = tail
            self.head = head
            os.rename(os.path.join(self.head, self.tail), os.path.join(self.head,
                                                                       self.tail.replace(self.tail, j + ".csv")))

    def main(self):
        self.login_facebook("india.adops.sage@gmail.com", "Ogilvy@123")
        self.each_market_report_india()
        self.login_facebook("gds.sage.mahesh@gmail.com", "abc@12345")
        self.each_market_report_gds()


if __name__ == "__main__":
    object_twitter = Facebook()
    object_twitter.main()
