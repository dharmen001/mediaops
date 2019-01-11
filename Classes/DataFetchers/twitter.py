from selenium import webdriver
import datetime
import time
from Classes.DataReaders.config_ini import Config
import glob
import os


class Twitter(Config):

    def __init__(self):
        super(Twitter, self).__init__()
        self.driver = None
        self.tail = None
        self.head = None
        self.today = datetime.date.today()
        self.first = self.today.replace(day=1)
        self.last_day = self.first - datetime.timedelta(days=1)
        self.last_day_month = self.last_day.strftime("%Y-%m-%d")
        self.first_day_month = '01'
        self.last_month = self.last_day.strftime("%Y-%m")

    def login_twitter(self, username, password):
        chrome_options = webdriver.ChromeOptions()
        preference = {"download.default_directory": self.section_value[19]}

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

    def twitter_france(self):
        self.driver.get("https://ads.twitter.com/ads_manager/oz2mex/campaigns/?endDate={}&startDate={}-{}".
                        format(self.last_day_month, self.last_month, self.first_day_month))

        self.driver.find_element_by_class_name("src-views-ExportsDropdown-styles-module--textMargin").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("src-components-SelectDropdown-styles-module--labelWrapper").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("src-views-ExportsDropdown-styles-module--downloadButton").click()
        self.driver.implicitly_wait(10)
        time.sleep(10)
        self.driver.close()

    def twitter_za(self):
        self.driver.get("https://ads.twitter.com/ads_manager/18ce54aaxwm/campaigns/?endDate={}&startDate={}-{}".
                        format(self.last_day_month, self.last_month, self.first_day_month))

        self.driver.find_element_by_class_name("src-views-ExportsDropdown-styles-module--textMargin").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("src-components-SelectDropdown-styles-module--labelWrapper").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("src-views-ExportsDropdown-styles-module--downloadButton").click()
        self.driver.implicitly_wait(10)
        time.sleep(10)
        self.driver.close()

    def twitter_sage_middle_east(self):
        self.driver.get("https://ads.twitter.com/ads_manager/18ce54s3ejk/campaigns/?endDate={}&startDate={}-{}".
                        format(self.last_day_month, self.last_month, self.first_day_month))

        self.driver.find_element_by_class_name("src-views-ExportsDropdown-styles-module--textMargin").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("src-components-SelectDropdown-styles-module--labelWrapper").click()
        self.driver.implicitly_wait(10)

        self.driver.find_element_by_class_name("src-views-ExportsDropdown-styles-module--downloadButton").click()
        self.driver.implicitly_wait(10)
        time.sleep(10)
        self.driver.close()

    def get_latest_file(self):
        newest = max(glob.iglob(self.section_value[19] + '*.xlsx'), key=os.path.getctime)
        head, tail = os.path.split(newest)
        self.tail = tail
        self.head = head

    def rename_file_france(self):
        os.rename(os.path.join(self.head, self.tail), os.path.join(self.head,
                                                                   self.tail.replace(self.tail,
                                                                                     "Sage_twitter_france.xlsx")))

    def rename_file_za(self):
        os.rename(os.path.join(self.head, self.tail), os.path.join(self.head,
                                                                   self.tail.replace(self.tail,
                                                                                     "Sage_twitter_ZA.xlsx")))

    def rename_file_mea(self):
        os.rename(os.path.join(self.head, self.tail), os.path.join(self.head,
                                                                   self.tail.replace(self.tail,
                                                                                     "Sage_twitter_MEA.xlsx")))

    def main(self):
        self.login_twitter("india.adops.sage@gmail.com", "Ogilvy@123")
        self.twitter_france()
        self.get_latest_file()
        self.rename_file_france()
        self.login_twitter("india.adops.sage@gmail.com", "Ogilvy@123")
        self.twitter_za()
        self.get_latest_file()
        self.rename_file_za()
        self.login_twitter("india.adops.sage@gmail.com", "Ogilvy@123")
        self.twitter_sage_middle_east()
        self.get_latest_file()
        self.rename_file_mea()


if __name__ == "__main__":
    object_twitter = Twitter()
    object_twitter.main()
