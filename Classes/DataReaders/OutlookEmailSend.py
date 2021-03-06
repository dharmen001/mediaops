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
        self.username = 'dharmendra.mishra@neomediaworld.com'
        self.password = 'Password5'
        self.file_name = None

    def get_contacts(self, filename):
        """
            Return two lists names, emails containing names and email addresses
            read from a file specified by filename.
        """
        # logger.info('Start Reading : {} '.format(filename))
        file_name = pd.read_csv(filename)
        body = file_name['Body'].tolist()
        names = file_name['Name'].tolist()
        emails = file_name['Email'].tolist()
        subjects = file_name['Subject'].tolist()
        attachments = file_name['FileName'].tolist()
        cc = file_name['CarbonC'].tolist()
        self.file_name = filename
        return body, names, emails, subjects, attachments, cc

    def main(self, file_path):
        body, names, emails, subjects, attachments, cc = self.get_contacts('/home/groupm/datadump/billingdata/'
                                                                           'outlookReciepientsList.csv')  # read contacts

        # set up the SMTP server
        logger.info('Setting up server with: {} '.format(self.username))
        s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(self.username, self.password)
        # For each contact, send the email:
        attachment = ''
        try:
            for msg_body, name, email, subject, attachment, cc in zip(body, names, emails, subjects, attachments, cc):
                print(file_path+attachment, emails, cc)
                msg = MIMEMultipart()  # create a message

                # setup the parameters of the message
                msg['From'] = self.username
                msg['To'] = email
                msg['Subject'] = subject
                msg['Cc'] = cc

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(open(file_path + attachment, 'rb').read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=attachment)

                msg.attach(part)

                # add in the message body
                msg.attach(MIMEText(msg_body, 'plain'))
                print(email, cc)
                # send the message via the server set up earlier.
                # logger.info('Sending email with Subject: {} to {} '.format(subject, email))
                s.sendmail(msg['From'], (email, cc), msg.as_string())
                # logger.info('Email sent to {}: '.format(name))
        except OSError as e:
            logger.error(str(e) + attachment)
            pass
        # Terminate the SMTP session and close the connection
        s.close()


if __name__ == "__main__":
    Object_Email_Send = SendEmail()
    path = '/home/groupm/datadump/billingdata/'
    Object_Email_Send.main(path)
