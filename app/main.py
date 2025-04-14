from fastapi import FastAPI
from app.routes import auth, verification
from app.database import init_models

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_models()

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(verification.router, prefix="/verification", tags=["Verification"])