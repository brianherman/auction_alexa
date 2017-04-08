
import datetime

from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

try:
    api = Connection(appid="")
    response = api.execute('findItemsAdvanced',{'keywords':'legos'})

except ConnectionError as e:
    print(e)
    print(e.response.dict())
    

def lambda_handler(event, context):
    print("Event: %s" % event)