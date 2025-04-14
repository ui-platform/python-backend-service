import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import secrets
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def send_email_code(email: str, code: str):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("email_verification.html")
    html_content = template.render(Title="Email Verification", Code=code)

    msg = EmailMessage()
    msg.add_alternative(html_content, subtype="html")
    msg["Subject"] = "Email Verification"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = email

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as s:
        s.starttls()
        s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        s.send_message(msg)

def generate_verification_code() -> str:
    return secrets.token_hex(3)[:6].upper()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_jwt_token(data: dict, expires_delta: int = 60) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("JWT_SECRET"), algorithm="HS256")