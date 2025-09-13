from fastapi import APIRouter, HTTPException, Depends
from firebase_config import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

@router.get("/user")
def get_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_data = verify_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid Token")
    
    return {"account": {"username": user_data["name"], "email": user_data["email"]}}
