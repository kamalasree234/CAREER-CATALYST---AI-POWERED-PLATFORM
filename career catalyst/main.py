import os
from fastapi import FastAPI, HTTPException, Depends
from firebase_config import db, auth
import requests
from firebase_admin import auth as firebase_auth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, Header
from firebase_config import verify_token






app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

app.include_router(auth.router)

GEMINI_API_KEY = os.geten
GNEWS_API_KEY = os.getenv

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Firebase Authentication API"}

@app.get("/user")
def get_user_data(authorization: str = Header(None)):
    """Fetch user details using Firebase Token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token missing")

    token = authorization.split("Bearer ")[-1]  # Extract token
    user_data = verify_token(token)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Token")

    return {"message": "Authenticated", "account": user_data}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Firebase authentication token."""
    try:
        decoded_token = firebase_auth.verify_id_token(credentials.credentials)
        return decoded_token["uid"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ------------------ USER ROUTES ------------------

@app.post("/register-user")
def register_user(user_data: dict):
    """
    Register a new user in Firestore after Google Sign-In.
    """
    user_id = user_data.get("uid")
    email = user_data.get("email")

    if not user_id or not email:
        raise HTTPException(status_code=400, detail="Missing user details")

    user_ref = db.collection("users").document(user_id)
    user_ref.set({
        "email": email,
        "history": [],
        "interests": []
    })

    return {"message": "User registered successfully"}

@app.get("/user/{user_id}", dependencies=[Depends(verify_token)])
def get_user(user_id: str):
    """
    Get user details from Firestore.
    """
    user_ref = db.collection("users").document(user_id).get()
    if user_ref.exists:
        return user_ref.to_dict()
    else:
        raise HTTPException(status_code=404, detail="User not found")

# ------------------ HISTORY ROUTES ------------------

@app.post("/add-history/{user_id}", dependencies=[Depends(verify_token)])
def add_to_history(user_id: str, career: dict):
    """
    Add searched career to user's history.
    """
    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()

    if not user.exists:
        raise HTTPException(status_code=404, detail="User not found")

    history = user.to_dict().get("history", [])
    history.append(career)
    user_ref.update({"history": history})

    return {"message": "Career added to history"}

@app.get("/history/{user_id}", dependencies=[Depends(verify_token)])
def get_history(user_id: str):
    """
    Retrieve user's career search history.
    """
    user_ref = db.collection("users").document(user_id).get()
    if user_ref.exists:
        return {"history": user_ref.to_dict().get("history", [])}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# ------------------ INTERESTS ROUTES ------------------

@app.get("/interests/{user_id}", dependencies=[Depends(verify_token)])
def get_interests(user_id: str):
    """
    Get user interests (based on past searches).
    """
    user_ref = db.collection("users").document(user_id).get()
    if user_ref.exists:
        history = user_ref.to_dict().get("history", [])
        return {"interests": history} if history else {"message": "Nothing to show here"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# ------------------ ROADMAP GENERATOR (GEMINI API) ------------------

@app.get("/roadmap/{career}")
def generate_roadmap(career: str):
    """
    Fetch career roadmap using Gemini API.
    """
    url = f"https://api.gemini.com/roadmap?career={career}&key={GEMINI_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch roadmap")

# ------------------ JOB SEARCH ------------------

@app.get("/jobs/{career}")
def get_jobs(career: str):
    """
    Fetch job opportunities related to the career.
    """
    job_api_url = f"https://jobs-api.com/search?query={career}"
    response = requests.get(job_api_url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch jobs")

# ------------------ NEWS (GNEWS API) ------------------

@app.get("/news/{career}")
def get_news(career: str):
    """
    Fetch career-related news from GNews.
    """
    url = f"https://gnews.io/api/v4/search?q={career}&token={GNEWS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch news")

# ------------------ ACCOUNT MANAGEMENT ------------------

@app.get("/account/{user_id}", dependencies=[Depends(verify_token)])
def get_account_details(user_id: str):
    """
    Get user account details.
    """
    user_ref = db.collection("users").document(user_id).get()
    if user_ref.exists:
        return {"email": user_ref.to_dict().get("email")}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/update-password")
def update_password(email: str, new_password: str):
    """
    Update user password in Firebase.
    """
    try:
        user = auth.get_user_by_email(email)
        auth.update_user(user.uid, password=new_password)
        return {"message": "Password updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
