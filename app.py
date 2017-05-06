import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
from flask import Flask
from flask_ask import Ask, statement, session
import boto3
import logging
app = Flask(__name__)
ask = Ask(app, '/')
#https://github.com/Miserlou/Zappa
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
def account_is_linked():
    if hasattr(session, 'user') and hasattr(session.user, 'accessToken'):
        return True
    else:
        return False

@ask.launch
def launch():
    return get_value()
def generate_speech(a):
     speech = ""
    for item in a['searchResult']['item']:
        speech += "{} is going for ${} <break time=\"1s\"/> ".format(item['title'], item['sellingStatus']['currentPrice']['value'])
    return statement(speech)
@ask.intent("GetValueIntent")
def get_value():
    if account_is_linked():
        at = session.user.accessToken
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
            generate_speech(api.response.dict())
        #https://www.bannedfromhalf.com/privacy.pdf
            response = api.execute('findItemsAdvanced', api_request)
           
            #dump(api, full=True)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
    else:
         return statement().simple_card('LinkAccount')
        