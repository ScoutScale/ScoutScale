import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
data = {
'Weight': "weight",
'Date' : "capture_date",
'Zone' : "zone"
}
doc_ref = db.collection('PythonApp').document()
doc_ref.set(data)
        
#google.api_core.exceptions.RetryError: Timeout of 60.0s exceeded, last exception: 503 Getting metadata from plugin failed with error:
# ('invalid_grant: Invalid JWT: Token must be a short-lived token (60 minutes) and in a reasonable timeframe. 
#Check your iat and exp values in the JWT claim.', {'error': 'invalid_grant', 'error_description': 'Invalid JWT: 
#Token must be a short-lived token (60 minutes) and in a reasonable timeframe. Check your iat and exp values in the JWT claim.'})