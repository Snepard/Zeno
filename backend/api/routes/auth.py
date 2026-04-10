from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

from db.user_store import create_user, get_user_by_email, verify_password
from config.settings import settings

router = APIRouter()


def _make_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    try:
        user = create_user(user_in.email, user_in.password, user_in.full_name)
        token = _make_token(user["id"])
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "access_token": token,
            "token_type": "bearer",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest):
    user = get_user_by_email(login_data.email)
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return {"access_token": _make_token(user["id"]), "token_type": "bearer"}
