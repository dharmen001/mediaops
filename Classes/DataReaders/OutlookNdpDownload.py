import email
import imaplib
import email.mime.multipart
from Classes.DataReaders.config_ini import Config
import os
import pandas as pd
from Classes.LoggerFile.LogFile import logger
import datetime


class Outlook(Config):
    def __init__(self):
        super(Outlook, self).__init__()
        self.username = None
        self.password = None
        self.imap = None
        self.subject = None
        self.file_name = None
        self.s = None
        self.att_path = "No attachment found"

    def subject_line(self):
        subject_read = pd.read_csv(self.section_value[9] + 'outlookEmails.csv')
        subject = subject_read.iloc[:, :]
        self.s = subject
        self.subject = subject.iloc[:, 1]
        self.file_name = subject.iloc[:, 0]

    def close_connection(self):
        return self.imap.close()

    def login(self, username, password):
        # IMAP Settings
        self.username = username
        self.password = password
        while True:
            # Connect to the server
            try:
                self.imap = imaplib.IMAP4_SSL("imap-mail.outlook.com", port=993)
                r, d = self.imap.login(username, password)
                assert r == 'OK', 'login failed'
                print(" > Sign as ", d)
            except imaplib.IMAP4.error:
                print(" > Sign In ...")
                continue
            break

    def inbox(self):
        # selecting the inbox
        typ, data = self.imap.select("Inbox")
        print (typ, data)
        num_msgs = int(data[0])
        print ('There are {} messages in INBOX'.format(num_msgs))
        return self.imap.select("Inbox")

    def email_check(self, download_folder):
        # fetch the email body (RFC822) for the given ID
        try:
            for i, j in zip(self.subject, self.file_name):
                print ('Subject {}'.format(i))
                # typ, msg_ids = self.imap.uid('search', None, 'SUBJECT {}'.format(i))
                typ, msg_ids = self.imap.uid('search', None, '(SUBJECT "{}")'.format(i))
                inbox_item_list = msg_ids[0].split()
                most_recent = inbox_item_list[-1]
                print (most_recent)
                if typ == "OK":
                    ret, data = self.imap.uid('fetch', most_recent, '(RFC822)')
                    raw_data = data[0][1]
                    # converts byte literal to string removing b''
                    raw_data_string = raw_data.decode('utf-8')
                    msg = email.message_from_string(raw_data_string)
                    # downloading attachments
                    # print(msg)
                    print('Subject:' + msg['Subject'])
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        filename = part.get_filename()
                        print("filename:" + filename)
                        filename = j
                    # if there is no filename, we create one with a counter to avoid duplicates
                        self.att_path = os.path.join(download_folder, filename)
                        # Check if its already there
                        # if not os.path.isfile(self.att_path):
                        fp = open(self.att_path, 'wb')
                        fp.write(part.get_payload(decode=True))
                        fp.close()

        except (imaplib.IMAP4.error, TypeError) as e:
            logger.error(str(e))
            pass

    def main(self):
        self.subject_line()
        self.login(self.section_value[5], 'Password5')
        self.inbox()
        logger.info('start downloading emails at ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.email_check(self.section_value[12])
        self.close_connection()
        logger.info('Emails Downloaded ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))


if __name__ == "__main__":
    obj = Outlook()
    obj.main()