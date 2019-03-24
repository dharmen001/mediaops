#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generates refresh token for AdWords using the Installed Application flow."""

import sys

from oauth2client import client

from django.conf import settings

# Your OAuth 2.0 Client ID and Secret. If you do not have an ID and Secret yet,
# please go to https://console.developers.google.com and create a set.
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

# The AdWords API OAuth 2.0 scope.
SCOPE = u'https://www.googleapis.com/auth/adwords'


def main():
    """Retrieve and display the access and refresh token."""
    flow = client.OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=[SCOPE],
        user_agent='Ads Python Client Library',
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    authorize_url = flow.step1_get_authorize_url()

    print('Log into the Google Account you use to access your AdWords account'
          'and go to the following URL: \n{}\n'.format(authorize_url))
    print('After approving the token enter the verification code (if specified).')
    code = input('Code: ').strip()

    try:
        credential = flow.step2_exchange(code)
    except client.FlowExchangeError as e:
        print('Authentication has failed: {}'.format(e))
        sys.exit(1)
    else:
        print('OAuth 2.0 authorization successful!\n\n'
              'Your access token is:\n {}\n\nYour refresh token is:\n {}'.format(
            credential.access_token, credential.refresh_token))


if __name__ == '__main__':
    main()
