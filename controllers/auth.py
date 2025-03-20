# from fastapi import APIRouter, Depends, HTTPException, Response
# import httpx
# import os
# from sqlmodel import Session, select
# from database import get_session
# from models.users import Users
# from schemas.users import UserResponse

# from dotenv import load_dotenv

# load_dotenv()  # Cargar variables desde .env


# router = APIRouter()

# CLIENT_ID = os.getenv("CLIENT_ID")
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# REDIRECT_URI = os.getenv("REDIRECT_URI")
# TOKEN_URL = "https://oauth2.googleapis.com/token"
# USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
#     raise ValueError("Missing Google OAuth credentials")

# @router.get("/auth/login")
# def login():
#     return {
#         "auth_url": f"https://accounts.google.com/o/oauth2/auth"
#         f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
#         f"&response_type=code&scope=openid email profile"
#     }

# @router.get("/auth/callback", response_model=UserResponse)
# async def auth_callback(code: str, response: Response, session: Session = Depends(get_session)):
#     async with httpx.AsyncClient() as client:
#         token_data = {
#             "code": code,
#             "client_id": CLIENT_ID,
#             "client_secret": CLIENT_SECRET,
#             "redirect_uri": REDIRECT_URI,
#             "grant_type": "authorization_code",
#         }
#         token_res = await client.post(TOKEN_URL, data=token_data)

#         if token_res.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to retrieve access token")

#         token_json = token_res.json()
#         access_token = token_json.get("access_token")

#         if not access_token:
#             raise HTTPException(status_code=400, detail="Invalid token response")

#         user_res = await client.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
#         user_info = user_res.json()

#     # Buscar usuario en la base de datos
#     existing_user = session.exec(select(Users).where(Users.email == user_info["email"])).first()

#     if not existing_user:
#         new_user = Users(
#             name=user_info["name"],
#             email=user_info["email"],
#             phone="",
#             dni="",
#             distrito_id=None
#         )
#         session.add(new_user)
#         session.commit()
#         session.refresh(new_user)
#         existing_user = new_user

#     SECURE_COOKIE = os.getenv("SECURE_COOKIE", "False").lower() == "true"
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         secure=SECURE_COOKIE,
#         samesite="Lax"
#     )

#     return existing_user


from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Response
import httpx
import os
from sqlmodel import Session, select
from database import get_session
from models.users import Users
from schemas.users import UserResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Cargar variables desde .env

# Configuración de OAuth2
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise ValueError("Missing Google OAuth credentials")

# Inicializar FastAPI
app = FastAPI()

# Configurar CORS para permitir cookies
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia esto por el dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

# 🔐 Obtener usuario actual desde la cookie
async def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    print("TOKEN ENCONTRADO EN COOKIE:", access_token)  # 👀 Verifica si se obtiene la cookie

    if not access_token:
        raise HTTPException(status_code=401, detail="No token found in cookies")

    async with httpx.AsyncClient() as client:
        user_res = await client.get(
            USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
        )

    print("GOOGLE RESPONSE:", user_res.json())  # 🔍 Verifica respuesta de Google

    if user_res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    return user_res.json()

# 🔑 Ruta para iniciar sesión (redirige a Google)
@router.get("/auth/login")
def login():
    return {
        "auth_url": f"https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&scope=openid email profile"
    }

# ✅ Callback donde Google devuelve el código y obtenemos el token
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

    # 📌 Buscar usuario en la base de datos
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

    # 🔒 Guardar el token en una cookie segura
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # ✅ Evita acceso desde JavaScript
        secure=False,   # ⚠️ Usa True solo en producción con HTTPS
        samesite="Lax"
    )

    return existing_user

# 🚪 Logout (elimina la cookie y cierra sesión)
@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

# 🔐 Endpoint protegido: Solo usuarios autenticados pueden acceder
@router.get("/")
async def root(user: dict = Depends(get_current_user)):
    return {"message": f"Hola {user['name']}, bienvenido a Waza!"}

# Agregar el router a la aplicación
app.include_router(router)
