# coding=utf-8
#! /usr/bin/env python3
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Classes.DataReaders.config_ini import Config
from email import encoders
import pandas as pd
from Classes.LoggerFile.LogFile import logger


class SendEmail(Config):

    def __init__(self):
        super(SendEmail, self).__init__()
        self.username = 'harmeet.singh@neomediaworld.com'
        self.password = '98266@raMbo'
        self.file_name = None

    def get_contacts(self, filename):
        """
            Return two lists names, emails containing names and email addresses
            read from a file specified by filename.
        """
        logger.info('Start Reading : {} '.format(filename))
        file_name = pd.read_csv(filename)
        body = file_name['Body']
        names = file_name['Name']
        emails = file_name['Email']
        subjects = file_name['Subject']
        attachments = file_name['FileName']
        self.file_name = filename
        return body, names, emails, subjects, attachments

    def main(self, file_path):
        body, names, emails, subjects, attachments = self.get_contacts(self.section_value[9] +
                                                                       'outlookReciepientsList.csv')  # read contacts

        # set up the SMTP server
        logger.info('Setting up server with: {} '.format(self.username))
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.username, self.password)

        # For each contact, send the email:
        for msg_body, name, email, subject, attachment in zip(body, names, emails, subjects, attachments):
            print(file_path+attachment)
            msg = MIMEMultipart()  # create a message

            # setup the parameters of the message
            msg['From'] = self.username
            msg['To'] = email
            msg['Subject'] = subject

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file_path + attachment, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=attachment)

            msg.attach(part)

            # add in the message body
            msg.attach(MIMEText(msg_body, 'plain'))

            # send the message via the server set up earlier.
            logger.info('Sending email with Subject: {} to {} '.format(subject, email))
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            logger.info('Email sent to {}: '.format(name))
        # Terminate the SMTP session and close the connection
        s.close()


if __name__ == "__main__":
    Object_Email_Send = SendEmail()
    path = '/home/groupm/datadump/billingdata/'
    Object_Email_Send.main(path)
