# names = ['Peter Parker', 'Clark Kent', 'Wade Wilson', 'Bruce wayne']
# heroes = ['Spiderman', 'Superman', 'Deadpool', 'Batman']
# universes = ['Marvel', 'DC', 'Marvel', 'DC']
#
# for name, hero, universe in zip(names, heroes, universes):
#     print('{} is actually {} from {}'.format(name, hero, universe))


# class Person(object):
#     pass
#
#
# person = Person()
#
# person_info = {'first': 'Corey', 'last': 'Schafer'}
#
# for key, value in person_info.items():
#     setattr(person, key, value)
#
# for key in person_info.keys():
#     print(getattr(person, key))

import sys
sys.path.append('C:/Python27/Lib/site-packages')
 # Replace this with the place you installed facebookads using pip
sys.path.append('C:/Python27/Lib/site-packages/facebook_business-3.2.13.dist-info') # same as above

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

my_app_id = 2836109913281404
my_app_secret = 'b75ec0b519b470cd1e75ba29ae407952'
my_access_token = 'EAAoTbUvs03wBAPjMUefpUZB4ZBiEZAgKgn2XRLmqbIdD3ZBLKYnaefwHeu4K0xSZBb01eQ66gxvUBj1B1vZBQjePu6P3RS6UFOtlfkqUfl9bX3ygsLJqSCFTfcsGrRnUudZB8Qa0DBoZBpgD5RXruMoY6U7uZCC9NOJVWKBYyplE505Q8C6R87B5A4kgszMfjAZBysDeQTBEo24QZDZD'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount(906794952681463)
campaigns = my_account
print(campaigns)