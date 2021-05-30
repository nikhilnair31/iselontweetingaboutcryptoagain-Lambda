import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('keys/crypto-musk-firebase-adminsdk-ay1ha-12d4e67ca9.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def firestore_del():
    print('Deleting documents one by one')
    docs = db.collection('pushertest').stream()
    for doc in docs:
        doc.reference.delete()

def firestore_push(obj):
    db.collection('pushertest').add(obj)

def handler(event, context): 
    firestore_del()
    
    for obj in event:
        firestore_push(obj)
        
    return {
        'statusCode': 200,
        'body': event
    }