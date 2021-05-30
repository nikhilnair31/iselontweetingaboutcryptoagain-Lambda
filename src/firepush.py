import json
import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate('keys/crypto-musk-firebase-adminsdk-ay1ha-12d4e67ca9.json')
firebase_admin.initialize_app(cred, {'storageBucket': 'crypto-musk.appspot.com' })
db = firestore.client()

tweetdictlist = []

def firestore_del():
    print('Deleting documents one by one')
    docs = db.collection('pushertest').stream()
    for doc in docs:
        doc.reference.delete()

def firestore_push(obj):
    db.collection('pushertest').add(obj)

def storagedel():
    bucket = storage.bucket()
    blob = bucket.blob('tweetdictlist.json')
    if blob.exists():
        blob.delete()
    
def objToDict(tweetObj):
    tweetdictlist.append(tweetObj)

def uploadToStorage():
    bucket = storage.bucket()
    blob = bucket.blob('tweetdictlist.json')
    outfile='/tmp/tweetdictlist.json'
    blob.upload_from_filename(outfile)

def handler(event, context): 
    # firestore_del()
    # for obj in event:
    #     firestore_push(obj)

    storagedel()
    for obj in event:
        objToDict(obj)
    with open('/tmp/tweetdictlist.json', 'w') as f:
        json.dump(tweetdictlist , f)
    uploadToStorage() 

    return {
        'statusCode': 200,
        'body': event
    }