import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
api = finding(config_file='ebay.yaml', warnings=True)
#searchResult.item.sellerInfo
#  .sellerUserName
api_request = {
    'itemFilter': [
        {'name': 'Seller',
            'value': 'homerun103'},
    ],
}

response = api.execute('findItemsAdvanced', api_request)
speech = ""
for item in api.response.dict()['searchResult']['item']:
    speech += "{} {}".format(item['title'], item['sellingStatus']['currentPrice']['value'])
print(speech)