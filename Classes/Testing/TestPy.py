import http.client

conn = http.client.HTTPConnection("adapi,sizmek,com")

payload = "{\"username\":\"Kshitij.Bhati_IBMGlobal_API\", \"password\":\"Password10\", \"redirected_url\":\"https://adapi.sizmek.com/sas/deliveryGroups/\",\r\n  \"entities\": [\r\n    {\r\n      \"type\": \"DeliveryGroup\",\r\n      \"id\": null,\r\n      \"relationsBag\": null,\r\n      \"version\": null,\r\n      \"createdBy\": null,\r\n      \"createdByName\": null,\r\n      \"createdByAccount\": null,\r\n      \"createdByAccountName\": null,\r\n      \"createdOn\": null,\r\n      \"lastUpdatedBy\": null,\r\n      \"lastUpdatedByName\": null,\r\n      \"lastUpdatedByAccount\": null,\r\n      \"lastUpdatedByAccountName\": null,\r\n      \"lastUpdateOn\": null,\r\n      \"name\": \"Amit_Test_API\",\r\n      \"subContainers\": null,\r\n      \"placementType\": null,\r\n      \"width\": 1007514647,\r\n      \"height\": -788198688,\r\n      \"rootContainer\": {\r\n        \"type\": \"RootContainer\",\r\n        \"id\": null,\r\n        \"relationsBag\": null,\r\n        \"version\": null,\r\n        \"childRotationType\": \"EvenDistribution\",\r\n        \"subContainers\": [],\r\n        \"childOptimizationMetric\": null,\r\n        \"childConversionTagId\": null,\r\n        \"childConversionTagName\": null\r\n      },\r\n      \"timeZone\": -2017946709,\r\n      \"servingSetting\": {\r\n        \"type\": \"APIServingSetting\",\r\n        \"impressionsPerUser\": 5,\r\n        \"impressionsPerDay\": 37,\r\n        \"timeBetweenAds\": 8,\r\n        \"frequencyCappingLevel\": true,\r\n        \"serveDefaultImage\": true\r\n      },\r\n      \"rotationAds\": [],\r\n      \"placements\": [],\r\n      \"defaultAds\": [],\r\n      \"campaignId\": 1073913578,\r\n      \"campaignName\": \"Test_Saas training\",\r\n      \"targetAudiencePriority\": 1155983754,\r\n      \"targetAudienceId\": null,\r\n      \"targetingTypeId\": 0,\r\n      \"geoTargetingTypeId\": -1,\r\n      \"geoTargetingCountryId\": -1,\r\n      \"aosCrossPlacement\": 1,\r\n      \"aoMethodTypeId\": -1,\r\n      \"gmt\": -1,\r\n      \"hideDisableAds\": false,\r\n      \"targetAudienceName\": null,\r\n      \"strategyId\": null,\r\n      \"strategyName\": null,\r\n      \"automaticOptimization\": false,\r\n      \"published\": false,\r\n      \"sequenceLevelCrossPlacementSupport\": true,\r\n      \"aoMethodType\": -1\r\n    }\r\n  ]\r\n}\r\n\r\n"

headers = {
    'Access-Control-Allow-Origin': "*",
    'Content-Type': "application/json",
    'api-key': "6KWoIwGArAiZtu48sseMu7qIXbmWQOe3",
    'Authorization': "Basic S3NoaXRpai5CaGF0aV9JQk1HbG9iYWxfQVBJOlBhc3N3b3JkMTA=",
    'cache-control': "no-cache",
    'Postman-Token': "6cca04fa-8ba7-494f-81f9-516e171793a1"
    }

conn.request("POST", "sas,deliveryGroups,", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))