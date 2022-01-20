import re
import json
import twint
import logging
import firebase_admin
from firebase_admin import credentials, db, firestore

cred = credentials.Certificate('./crypto-musk-firebase-adminsdk-ay1ha-12d4e67ca9.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://crypto-musk-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference('tweets')
db = firestore.client()

tweetdictlist = []
matches = ['shiba' , 'doge' , 'dogecoin' , 'bitcoin' , 'btc' , 'ethereum' , 'crypto' , 'cryptocurrency']
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def cleantweet(tweet): 
    # print('cleantweet\n')
    cleantweet = ''
    cleantweet = tweet.replace("&amp;", "&")
    usernameremovedtweet = re.sub(r'@\w+', '', cleantweet)
    if any(x in usernameremovedtweet for x in matches):
        return cleantweet
    else:
        return False

# Firebase RTDB
def getDataAndCheck(existingdata, newlypulleddataarr): 
    print('getDataAndCheck\n\n')
    insertlist = []
    for newitem in newlypulleddataarr:
        result = any(newitem["tweet"] in d.values() for d in existingdata.values())
        print(f'newitem: {newitem} - result: {result}')
        if(result == True): continue
        else:
            if(cleantweet(newitem["tweet"]) != False):
                newitem["tweet"] = cleantweet(newitem["tweet"])
                insertlist.append(newitem)
    return insertlist
def saveToRTDB(newlypulleddataarr): 
    existingdata = ref.get()
    print(f'existingdata: {existingdata}\n')

    if(existingdata != None):
        print(f'len(existingdata): {len(existingdata)} - len(newlypulleddataarr): {len(newlypulleddataarr)}\n')
        insertablearr = getDataAndCheck(existingdata, newlypulleddataarr)
    else:
        insertlist = []
        for newitem in newlypulleddataarr:
            if(cleantweet(newitem["tweet"]) != False):
                newitem["tweet"] = cleantweet(newitem["tweet"])
                insertlist.append(newitem)
        insertablearr = newlypulleddataarr
        
    for obj in insertablearr:
        ref.push().set(obj)
    print('saveToRTDB')

# Main Twint func
def tweet_handler(): 
    tweets = []
    full_tweet_data = []

    config = twint.Config()
    config.Username = "elonmusk"
    config.User_full = True 
    config.Search = "shiba OR doge OR dogecoin OR bitcoin OR btc OR ethereum OR crypto OR cryptocurrency"
    config.Lang = "en"
    config.Limit = 1000
    config.Since = "2017-01-01"
    config.Filter_retweets = True
    config.Store_object = True
    config.Store_object_tweets_list = tweets
    twint.run.Search(config)

    for tweet in tweets:
        # print ('Tweet: {}'.format(tweet))
        full_tweet_data.append({
            'id': tweet.id,
            'user_id': tweet.user_id, 
            'date': tweet.datestamp, 
            'time': tweet.timestamp, 
            'tweet': tweet.tweet, 
            'likes_count': tweet.likes_count, 
            'retweets_count': tweet.retweets_count, 
            'replies_count': tweet.replies_count, 
        })
    
    return {
        'statusCode': 200,
        'len': str(len(full_tweet_data)),
        'body': full_tweet_data
    }

def handler(event, context): 
    event = tweet_handler()
    print(f'event: {event}\n\n')
    logger.info(f'event: {event}\n\n')

    # ref.delete()

    recieved_data = []
    if type(event) is dict:
        recieved_data = event["body"] # event.responsePayload.body #event["responsePayload"]["body"] maybe?
    elif type(event) == list:
        recieved_data = event
    saveToRTDB(recieved_data)

    return {
        'statusCode': 200,
        'body': event
    }

if __name__ == '__main__':
    handler({}, {})