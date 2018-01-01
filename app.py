import urllib.request
import urllib.parse
import json
import boto3
import ebaysdk
from ebaysdk.finding import Connection as finding
from ebaysdk.exception import ConnectionError
import os
import random
import logging
import pprint

def generate_speech(a, seller):
    speech = "<speak> Items sold by "+ seller + "<break time=\"1s\"/>"
    try:
        for index, item in enumerate(a['searchResult']['item']):
            speech += "{} is going for ${} <break time=\"1s\"/>".format(item['title'].replace('&','').replace('*',''), item['sellingStatus']['currentPrice']['value'])
            if index == 2:
               break
        return speech + "</speak>"
    except KeyError:
        return "<speak>Has no items for sale.</speak>"
    return "<speak>Has no items for sale.</speak>"
def generate_speech_card(a,seller):
    card_text = "Items sold by "+ seller
    try:
        for index, item in enumerate(a['searchResult']['item']):
            card_text += "{} is going for ${}<br>".format(item['title'], item['sellingStatus']['currentPrice']['value'])
            if index == 2:
               break
        return card_text
    except KeyError:
        return "Has no items for sale."
    return "Has no items for sale."
def search(name):
    try:
        api = finding(appid="BrianHer-Alexa-PRD-409141381-46692988",config_file=None, warnings=True)
        #searchResult.item.sellerInfo
        #  .sellerUserName     
        api_request = {
            'itemFilter': [
                {'name': 'Seller',
                    'value': name},
            ],
            'sortOrder':{'EndTimeSoonest'}
        }
    #https://www.bannedfromhalf.com/privacy.pdf
        response = api.execute('findItemsAdvanced', api_request)
        #print(api.response.dict())
        return generate_speech(api.response.dict(),name)
    
        #dump(api, full=True)
    except ConnectionError as e:

        print(e)
        print(e.response.dict())
def search_card(name):
    try:
        api = finding(appid="BrianHer-Alexa-PRD-409141381-46692988",config_file=None, warnings=True)
        #searchResult.item.sellerInfo
        #  .sellerUserName     
        api_request = {
            'itemFilter': [
                {'name': 'Seller',
                    'value': name},
            ],
            'sortOrder':{'EndTimeSoonest'}
        }
    #https://www.bannedfromhalf.com/privacy.pdf
        response = api.execute('findItemsAdvanced', api_request)
        #print(api.response.dict())
        return generate_speech_card(api.response.dict(),name)
    
        #dump(api, full=True)
    except ConnectionError as e:

        print(e)
        print(e.response.dict())
def get_random_tweet(session):
    """
    Grab token from session and get ebay item information!
    """
    access_token = session['user']['accessToken']
    url = 'https://api.amazon.com/auth/o2/tokeninfo?access_token='+urllib.parse.quote_plus(access_token)
    print(url)
    f = urllib.request.urlopen(url)
    d = json.loads(f.read().decode('utf-8'))
    if d['aud'] != 'amzn1.application-oa2-client.74e27ed5f3da48d18b60b6b156787d9a' :
        raise BaseException("Invalid Token") 
    url = 'https://api.amazon.com/user/profile?access_token='+urllib.parse.quote_plus(access_token)
    #print(url)
    f = urllib.request.urlopen(url)
    user = json.loads(f.read().decode('utf-8'))
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    response = table.get_item(
        Key={
            'uid': user['user_id'],
        }
    )
    item = response['Item']['following']
    #print(item)
    speech = ""
    card_text = ""
    for name in item:
        speech += search(name)
    for name in item:
        card_text += search_card(name)
    return {'speech': speech,'card_text': card_text}

def build_speechlet_response(output, card_title=' said...',
                             reprompt_text='', card_type='Simple',
                             should_end_session=True):
    """
    Build the JSON speechlet response.
    """
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': output
            },
            'card': {
                'type': card_type,
                'title': card_title,
                'content': card_text
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }
    }
def build_speechlet_response_card_text(output="test", card_title=' said...',
                             reprompt_text='', card_type='Simple', card_text = "",
                             should_end_session=True):
    """
    Build the JSON speechlet response.
    """
    return {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': output
            },
            'card': {
                'type': card_type,
                'title': card_title,
                'content': card_text
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': reprompt_text
                }
            },
            'shouldEndSession': should_end_session
        }
    }
def handle_session_end_request():
    """
    Thank the user and exit the skill.
    """
    card_title = "Session Ended"
    speech_output = "<speak>Thanks for trying auction buttler!</speak>"
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def build_tweet_response_card_text(session):
    """
    Build the response text for a Donald Trump tweet
    """


    resp = get_random_tweet(session)
    return build_speechlet_response_card_text(output=resp['speech'],
                                    card_title='Following users.',
                                    card_text=resp['card_text'],
                                    should_end_session=True)
def build_tweet_response(session):
    """
    Build the response text for a Donald Trump tweet
    """

    resp = get_random_tweet(session)
    
    return build_speechlet_response(output=resp['speech'],
                                    card_title='Following users.',
                                    should_end_session=True)

def on_launch(launch_request, session):
    """
    Called during default launch with no specific user intent
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # right now we have one default intent, so whatever, man...
    print (build_tweet_response_card_text(session))

    return build_tweet_response_card_text(session)

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    # right now we have one default intent, so whatever, man...
    return build_tweet_response_card_text(session)


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
def lambda_handler(event, context):
    """
    Main entry-point for the Lambda function.
    """
    ### Boilerplate from Amazon Lambda example
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(event)
    print(event)
    #print("event.session.application.applicationId=" +
    #     event['session']['application']['applicationId'])

    # Check if account is linked.
    if not event['session']['user'].get('accessToken',False):
        return build_speechlet_response_card_text(
            output="<speak>Please first link this skill using the Alexa app.</speak>",
            card_type='LinkAccount',card_text="Please first link this skill using the Alexa app.", card_title='Link your account')


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        print(on_launch(event['request'], event['session']))
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        print (on_intent(event['request'], event['session']))

        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
       print(on_session_ended(event['request'], event['session']))
       return on_session_ended(event['request'], event['session'])
    

