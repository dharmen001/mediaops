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
CLIENT_SECRET_FILE = "client_secret.json"
APPLICATION_NAME = 'ps'


def get_credentials():
    '''Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    '''
    credential_path = 'mycreds.txt'
    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    '''Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    # service = discovery.build('gmail', 'v1', http=http)
    service = discovery.build('dfareporting', 'v3.3', http=http)
    csv_file = open("C:/mediaops/mapping/DCM/flood_create.csv", "r+")
    reader = csv.DictReader(csv_file)
    for r in reader:
        floodlight_activity = dict(r)
        profile_id = floodlight_activity["profileId"]
        # floodlight_activity[""]=floodlight_activity[""].split(",")
        print("floodlight_activity", floodlight_activity)
        request = service.floodlightActivities().insert(profileId=profile_id, body=floodlight_activity)
        _ = request.execute()


if __name__ == '__main__':
    main()
