import json
import twint
import logging
import firebase_admin
from firebase_admin import credentials, db, firestore, storage

cred = credentials.Certificate('./keys/crypto-musk-firebase-adminsdk-ay1ha-12d4e67ca9.json')
# firebase_admin.initialize_app(cred, {'storageBucket': 'crypto-musk.appspot.com' })
firebase_admin.initialize_app(cred, {'databaseURL': 'https://crypto-musk-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference('tweets')
db = firestore.client()

tweetdictlist = []
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Firebase storage thing
def storagedel():
    bucket = storage.bucket()
    blob = bucket.blob('tweetdictlist.json')
    logger.info(f'blob.exists(): {blob.exists()}')
    if blob.exists():
        blob.delete()
def objToDict(tweetObj):
    logger.info(f'tweetObj: {tweetObj}')
    tweetdictlist.append(tweetObj)
def uploadToStorage():
    bucket = storage.bucket()
    blob = bucket.blob('tweetdictlist.json')
    outfile='/tmp/tweetdictlist.json'
    blob.upload_from_filename(outfile)
  
# Firebase RTDB
def nukeRTDB(): 
    print('deleted full RTDB')
    ref.delete()
def saveToRTDB(jsonarray): 
    nukeRTDB()
    for obj in jsonarray:
        ref.push().set(obj)
    print('saved to RTDB')

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
        print ('Tweet: {}'.format(tweet))
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

    recieved_data = []
    if type(event) is dict:
        recieved_data = event["body"] # event.responsePayload.body #event["responsePayload"]["body"] maybe?
    elif type(event) == list:
        recieved_data = event

    saveToRTDB(recieved_data)
    
    # storagedel()
    # for obj in recieved_data:
    #     objToDict(obj)
    # with open('/tmp/tweetdictlist.json', 'w') as f:
    #     json.dump(tweetdictlist , f)
    # uploadToStorage() 

    return {
        'statusCode': 200,
        'body': event
    }

if __name__ == '__main__':
    handler({}, {})