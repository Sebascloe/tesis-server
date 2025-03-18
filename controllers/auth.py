from fastapi import APIRouter, Depends, HTTPException, Response
import httpx
import os
from sqlmodel import Session, select
from database import get_session
from models.users import Users
from schemas.users import UserResponse

from dotenv import load_dotenv

load_dotenv()  # Cargar variables desde .env


router = APIRouter()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise ValueError("Missing Google OAuth credentials")

@router.get("/auth/login")
def login():
    return {
        "auth_url": f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=openid email profile"
    }

@router.get("/auth/callback", response_model=UserResponse)
async def auth_callback(code: str, response: Response, session: Session = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        token_data = {
            "code": code,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_res = await client.post(TOKEN_URL, data=token_data)

        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve access token")

        token_json = token_res.json()
        access_token = token_json.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Invalid token response")

        user_res = await client.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
        user_info = user_res.json()

    # Buscar usuario en la base de datos
    existing_user = session.exec(select(Users).where(Users.email == user_info["email"])).first()

    if not existing_user:
        new_user = Users(
            name=user_info["name"],
            email=user_info["email"],
            phone="",
            dni="",
            distrito_id=None
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        existing_user = new_user

    SECURE_COOKIE = os.getenv("SECURE_COOKIE", "False").lower() == "true"
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite="Lax"
    )

    return existing_user
