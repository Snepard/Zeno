from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate
from services import auth_service
from auth.security import create_access_token

async def handle_register(db: AsyncSession, user_in: UserCreate):
    return await auth_service.create_user(db, user_in)

async def handle_login(db: AsyncSession, form_data: OAuth2PasswordRequestForm):
    user = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
