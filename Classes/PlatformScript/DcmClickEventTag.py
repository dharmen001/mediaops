import argparse
import sys

import dfareporting_utils
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to add an event tag for')
argparser.add_argument(
    'campaign_id', type=int,
    help='The ID of the campaign to add an event tag for')


def main(argv):
  # Retrieve command line arguments.
  flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

  # Authenticate and construct service.
  service = dfareporting_utils.setup(flags)

  profile_id = flags.profile_id
  campaign_id = flags.campaign_id

  try:
    # Construct and save event tag.
    event_tag = {
        'campaignId': campaign_id,
        'name': 'Test Campaign Event Tag',
        'status': 'ENABLED',
        'type': 'CLICK_THROUGH_EVENT_TAG',
        'url': 'https://www.google.com'
    }

    request = service.eventTags().insert(profileId=profile_id, body=event_tag)

    # Execute request and print response.
    response = request.execute()

    print ('Created campaign event tag with ID %s and name "%s".'
           % (response['id'], response['name']))

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)