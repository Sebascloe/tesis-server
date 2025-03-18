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

# Credenciales de Discord
CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")

# URLs de autenticación de Discord
TOKEN_URL = "https://discord.com/api/oauth2/token"
USERINFO_URL = "https://discord.com/api/users/@me"

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise ValueError("Missing Discord OAuth credentials")

@router.get("/auth/login1")
def login():
    return {
        "auth_url": f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=identify email"
    }

@router.get("/auth/callback1", response_model=UserResponse)
async def auth_callback(code: str, response: Response, session: Session = Depends(get_session)):
    async with httpx.AsyncClient() as client:
        token_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "scope": "identify email"
        }
        token_res = await client.post(TOKEN_URL, data=token_data, headers={"Content-Type": "application/x-www-form-urlencoded"})

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
            name=user_info["username"],  # Nombre de usuario de Discord
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
