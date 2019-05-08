import time
# from __future__ import print_function
import httplib2
import os
import csv
import sys
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/dfareporting',
          'https://www.googleapis.com/auth/dfatrafficking']
CLIENT_SECRET_FILE = '/home/groupm/mediaops-project/mediaops/Classes/DcmPlatform/client_secret.json'
APPLICATION_NAME = 'ps'


def get_credentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    credential_path = '/home/groupm/mediaops-project/mediaops/Classes/DcmPlatform/credentials.json'
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    '''Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    service1 = discovery.build('dfareporting', 'v3.3', http=http)
    csvfile = open("/home/groupm/mediaops-project/mediaops/mapping/DCM/eventtag.csv", "r+")
    reader = csv.DictReader(csvfile)
    for r in reader:
        eventtag_activity_3 = dict(r)
        p = eventtag_activity_3["profileId"]
        s = eventtag_activity_3["id"]
        eventtag_activity_3["eventTagOverrides"] = [eval(i) for i in
                                                    eventtag_activity_3["eventTagOverrides"].split("|")]
        print("eventtag_activity_3", eventtag_activity_3)
        request3 = service1.ads().patch(profileId=p, id=s, body=eventtag_activity_3)
        response3 = request3.execute()


if __name__ == '__main__':
    main()
