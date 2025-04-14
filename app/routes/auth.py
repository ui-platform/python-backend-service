from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, VerificationCode
from app.schemas import RegisterRequest, LoginRequest
from app.utils import hash_password, verify_password, create_jwt_token
from app.deps import get_db

router = APIRouter()

@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user_check = await db.execute(select(User).where(User.email == request.email))
    if user_check.scalar():
        raise HTTPException(status_code=400, detail="Email already registered")

    code_entry = await db.scalar(select(VerificationCode).where(
        and_(VerificationCode.email == request.email, VerificationCode.code == request.code, VerificationCode.used == False)))
    if not code_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    hashed_password = hash_password(request.password)
    new_user = User(email=request.email, password=hashed_password)
    db.add(new_user)
    code_entry.used = True
    await db.commit()

    token = create_jwt_token({"sub": str(new_user.id)})
    return {"message": "User registered successfully", "access_token": token}

@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == request.email))
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token({"sub": str(user.id)})
    return {"message": "Login successful", "access_token": token}