# coding=utf-8
# !/usr/bin/env python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Classes.LoggerFile.LogFile import logger
from Classes.DataReaders.config_ini import Config
import datetime
import pandas as pd


class SendEmail(Config):

    def __init__(self):
        super(SendEmail, self).__init__()
        self.outlook_recipient = None
        self.outlook_subject = None

    def read_outlook_file(self):
        outlook_file = pd.read_csv(self.section_value[9] + "outlookReciepientsList.csv")
        outlook_recipient = outlook_file['Recipient']
        outlook_subject = outlook_file['Subject']
        self.outlook_recipient = outlook_recipient
        self.outlook_subject = outlook_subject

    def send_mail(self, recipient, subject, message):
        logger.info("Start Sending ")
        username = self.section_value[5]
        password = self.section_value[6]

        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        print('sending mail to ' + recipient + ' on ' + subject)
        mailServer = smtplib.SMTP('smtp-mail.outlook.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(username, password)
        mailServer.sendmail(username, recipient, msg.as_string())
        mailServer.close()

    def main(self):
        self.read_outlook_file()
        self.send_mail('Adops-India@neomediaworld.com',
                       "{}".format(), "Start Creating Report for {} ".format() +
                       str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "." + "\n" + "\n" +
                       "Thanks\nAdops-Team")


if __name__ == "__main__":
    Object_Email_Send = SendEmail()
    Object_Email_Send.main()