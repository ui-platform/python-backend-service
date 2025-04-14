from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, VerificationCode
from app.schemas import EmailVerificationRequest
from app.utils import generate_verification_code, send_email_code
from app.deps import get_db

router = APIRouter()

@router.post("/")
async def email_verification(request: EmailVerificationRequest, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).where(User.email == request.email))
    if user:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    if request.send_email:
        code = generate_verification_code()
        db.add(VerificationCode(email=request.email, code=code))
        await db.commit()
        send_email_code(request.email, code)

    return {"message": "Verification code processed"}