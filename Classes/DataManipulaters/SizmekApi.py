import urllib3
import requests
import json
url = 'https://adapi.sizmek.com/sas/login/login/'
Key = '6KWoIwGArAiZtu48sseMu7qIXbmWQOe3'
urllib3.disable_warnings()
metrics = {"name": "Test_Amit", "rootContainer": {"type": "In Banner",
                                                  "childRotationType": "EvenDistribution",
                                                  "subContainers": [], "childOptimizationMetric": '',
                                                  "childConversionTagId": '', "childConversionTagName": ''},
           "campaignId": 1073915600, "campaignName": "Test_IBM-Adops_Amit Raut"}

headers = {'content-type': 'application/json'}
data = metrics
params = {'sessionKey': Key, 'format': 'json'}
r = requests.post(url, params=params, data=json.dumps(data), headers=headers,
                  auth=('Kshitij.Bhati_IBMGlobal_API', 'Password10'))
print(r.status_code)

# import requests
# from requests.auth import HTTPBasicAuth
#
# auth_token = '6KWoIwGArAiZtu48sseMu7qIXbmWQOe3'
# user_name = 'Kshitij.Bhati_IBMGlobal_API'
# base_url = 'https://mdx.sizmek.com/'
# session = requests.session()
# resp = session.get(base_url + '#/spa/campaign/1073929134/deliveryGroups', auth=HTTPBasicAuth(user_name, auth_token))
# print(resp.status_code)