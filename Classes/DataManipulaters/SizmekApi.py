import requests
import json

payload = {'username': 'Kshitij.Bhati_IBMGlobal_API', 'password': 'Password10',
           'redirect_url': 'https://adapi.sizmek.com/sas/deliveryGroups/',
           'entities': [{'type': 'DeliveryGroup',
                         'name': 'Amit_Test_API',
                         'campaignId': 1073913578,
                         'campaignName': 'Test_Saas training'}]}

url = "https://adapi.sizmek.com/sas/login/login/"
s = requests.session()

headers = {
    'Access-Control-Allow-Origin': "*",
    'Content-Type': "application/json",
    'api-key': "6KWoIwGArAiZtu48sseMu7qIXbmWQOe3",
    'Authorization': "Basic S3NoaXRpai5CaGF0aV9JQk1HbG9iYWxfQVBJOlBhc3N3b3JkMTA=",
    'cache-control': "no-cache",
    'Postman-Token': "b4c9dde2-e163-452d-88c0-3d7cf5830b05"
}

response = s.post(url, data=json.dumps(payload), headers=headers, verify=True)

# my_data = json.load(response.json())
# with open('data.json', 'w') as outfile:
#     json.dump(my_data, outfile,  indent=4)
#
print(response.status_code)
# print(json.dumps(response._content.decode("utf-8"), indent=4, sort_keys=True))
from pprint import pprint

pprint(response.json(), indent=4)
# print(json.dumps(response.json(), indent=4), file=open('alok.json', 'w')))
