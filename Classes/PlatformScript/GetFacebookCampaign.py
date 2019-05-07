# This program downloads all relevent Facebook traffic info as a csv file
# This program requires info from the Facebook Ads API: https://github.com/facebook/facebook-python-ads-sdk

# Import all the facebook mumbo jumbo
from facebookads.api import FacebookAdsApi
from facebookads.adobjects.adsinsights import AdsInsights
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.business import Business

# Import th csv writer and the date/time function
import datetime
import csv

# Set the info to get connected to the API. Do NOT share this info
my_app_id = 2836109913281404
my_app_secret = 'b75ec0b519b470cd1e75ba29ae407952'
my_access_token = 'EAAoTbUvs03wBAI3WhpWF9aUHSvZBfoEmXaS1HplRtFOjZCVz0Gg0viXG94LLxEb4COtCoEcs3gBeZAemr7DSafRMY10PpfcYjZARmHMVy3OmozyuQNnN7Rm9XzCzVCBJWBPNRjxMUG8nmShFYaulyiX83OaCiRMqgHI06MYwt0nUqdqW1GB1AZC9pASX9Ys9tlZAOSeGevJgZDZD'

# Start the connection to the facebook API
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)

# Create a business object for the business account
business = Business(906794952681463)

# Get yesterday's date for the filename, and the csv data
yesterdaybad = datetime.datetime.now() - datetime.timedelta(days=1)
yesterdayslash = yesterdaybad.strftime('%m/%d/%Y')
yesterdayhyphen = yesterdaybad.strftime('%m-%d-%Y')

# Define the destination filename
filename = yesterdayhyphen + '_fb.csv'
filelocation = "C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/facebook/" + filename

# Get all ad accounts on the business account
accounts = business.get_owned_ad_accounts(fields=[AdAccount.Field.id])

# Open or create new file

csvfile = open(filelocation, 'w+', 0o777)
filewriter = csv.writer(csvfile, delimiter=',')

# To keep track of rows added to file
rows = 0

# Iterate through the adaccounts
for account in accounts:
    # Create an addaccount object from the adaccount id to make it possible to get insights
    tempaccount = AdAccount(account[AdAccount.Field.id])

    # Grab insight info for all ads in the adaccount
    ads = tempaccount.get_insights(params={'date_preset': 'yesterday',
                                           'level': 'ad'
                                           },
                                   fields=[AdsInsights.Field.account_id,
                                           AdsInsights.Field.account_name,
                                           AdsInsights.Field.ad_id,
                                           AdsInsights.Field.ad_name,
                                           AdsInsights.Field.adset_id,
                                           AdsInsights.Field.adset_name,
                                           AdsInsights.Field.campaign_id,
                                           AdsInsights.Field.campaign_name,
                                           AdsInsights.Field.cost_per_outbound_click,
                                           AdsInsights.Field.outbound_clicks,
                                           AdsInsights.Field.spend,
                                           AdsInsights.Field.clicks,
                                           AdsInsights.Field.impressions
                                           ]
                                   )

    # Iterate through all accounts in the business account
    for ad in ads:
        # Set default values in case the insight info is empty
        date = yesterdayslash
        accountid = ad[AdsInsights.Field.account_id]
        accountname = ""
        adid = ""
        adname = ""
        adsetid = ""
        adsetname = ""
        campaignid = ""
        campaignname = ""
        costperoutboundclick = ""
        outboundclicks = ""
        spend = ""
        clicks = ""
        impressions = ""

        # Set values from insight data
        if ('account_id' in ad):
            accountid = ad[AdsInsights.Field.account_id]
        if ('account_name' in ad):
            accountname = ad[AdsInsights.Field.account_name]
        if ('ad_id' in ad):
            adid = ad[AdsInsights.Field.ad_id]
        if ('ad_name' in ad):
            adname = ad[AdsInsights.Field.ad_name]
        if ('adset_id' in ad):
            adsetid = ad[AdsInsights.Field.adset_id]
        if ('adset_name' in ad):
            adsetname = ad[AdsInsights.Field.adset_name]
        if ('campaign_id' in ad):
            campaignid = ad[AdsInsights.Field.campaign_id]
        if ('campaign_name' in ad):
            campaignname = ad[AdsInsights.Field.campaign_name]
        if ('cost_per_outbound_click' in ad):  # This is stored strangely, takes a few steps to break through the layers
            costperoutboundclicklist = ad[AdsInsights.Field.cost_per_outbound_click]
            costperoutboundclickdict = costperoutboundclicklist[0]
            costperoutboundclick = costperoutboundclickdict.get('value')
        if ('outbound_clicks' in ad):  # This is stored strangely, takes a few steps to break through the layers
            outboundclickslist = ad[AdsInsights.Field.outbound_clicks]
            outboundclicksdict = outboundclickslist[0]
            outboundclicks = outboundclicksdict.get('value')
        if ('spend' in ad):
            spend = ad[AdsInsights.Field.spend]

        # Write all ad info to the file, and increment the number of rows that will display
        filewriter.writerow([date, accountid, accountname, adid, adname, adsetid, adsetname, campaignid, campaignname,
                             costperoutboundclick, outboundclicks, spend, clicks, impressions])
        rows += 1

csvfile.close()

# Print report
print (str(rows) + " rows added to the file " + filename)
