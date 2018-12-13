import email
import imaplib
import email.mime.multipart
from config import Config
import datetime
import os
import pandas as pd


class Outlook(Config):
    def __init__(self):
        super(Outlook, self).__init__()
        self.username = None
        self.password = None
        self.imap = None
        self.smtp = None
        self.data = None
        self.emails = []
        self.msg = []
        self.subject = []
        self.file_name = []

    def subject_line(self):
        subject_read = pd.read_csv(self.section_value[9] + 'outlookEmails.csv')
        subject = subject_read.iloc[:, 1].tolist()
        file_name = subject_read.iloc[:, 0].tolist()
        self.subject = subject
        self.file_name = file_name

    def close_connection(self):
        return self.imap.close()

    def login(self, username, password):
        self.username = username
        self.password = password
        while True:

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
        typ, data = self.imap.select("Inbox")
        print typ, data
        num_msgs = int(data[0])
        print 'There are {} messages in INBOX'.format(num_msgs)
        return self.imap.select("Inbox")

    @staticmethod
    def today():
        mydate = datetime.datetime.now()
        return mydate.strftime("%Y-%m-%d")

    def email_check(self):
        for i in self.subject:
            typ, msg_ids = self.imap.uid('search', None, '(SUBJECT "{}")'.format(i))
            print(i, msg_ids)
            inbox_item_list = msg_ids[0].split()
            print (inbox_item_list)
            most_recent = inbox_item_list[-1]
            print (typ, i, most_recent)
            if typ == "OK":
                for message in most_recent:
                    print 'Processing :', i
                    try:
                        typ, self.data = self.imap.uid('fetch', message, '(RFC822)')
                        self.msg = email.message_from_string(self.data[0][1])
                    except:
                        print(self.msg)

                    if not isinstance(self.msg, str):
                        self.emails.append(self.msg)
                    response, self.data = self.imap.uid('store', message, '-FLAGS', '\\Seen')
                    print(self.emails)
                    print(self.data)
                    exit()
        return self.msg

    def save_attachment(self, msg, download_folder):
        att_path = "No attachment found"
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            print(filename)
            exit()

            att_path = os.path.join(download_folder, filename)

            if not os.path.isfile(att_path):
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
                
        return att_path

    def main(self):
        self.subject_line()
        self.login(self.section_value[5], self.section_value[6])
        self.inbox()
        self.save_attachment(self.email_check(), self.section_value[12])
        self.close_connection()


if __name__ == "__main__":
    obj = Outlook()
    obj.main()