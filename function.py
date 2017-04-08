import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
def dump(api, full=False):

    print("\n")

    if api.warnings():
        print("Warnings" + api.warnings())

    if api.response.content:
        print("Call Success: %s in length" % len(api.response.content))

    print("Response code: %s" % api.response_code())
    print("Response DOM1: %s" % api.response_dom())  # deprecated
    print("Response ETREE: %s" % api.response.dom())

    if full:
        print(api.response.content)
        print(api.response.json())
        print("Response Reply: %s" % api.response.reply)
    else:
        dictstr = "%s" % api.response.dict()
        print("Response dictionary: %s..." % dictstr[:150])
        replystr = "%s" % api.response.reply
        print("Response Reply: %s" % replystr[:150])
try:
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
    import pdb; pdb.set_trace()
    #api.response.dict()['searchResult']['item'][0]['sellingStatus']['currentPrice']['value']
    dump(api, full=True)
except ConnectionError as e:
    print(e)
    print(e.response.dict())

def lambda_handler(event, context):
    print("Event: %s" % event)