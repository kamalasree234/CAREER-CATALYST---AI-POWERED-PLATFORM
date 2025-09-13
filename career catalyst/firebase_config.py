import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase
cred = credentials.Certificate("n")
firebase_admin.initialize_app(cred)

def verify_token(id_token: str):
    """Verifies Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print("Token verification failed:", str(e))
        return None
    
db = firestore.client()
auth = firebase_admin.auth 