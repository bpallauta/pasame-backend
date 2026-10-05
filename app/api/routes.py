from fastapi import APIRouter
from app.api import bills
from app.api.endpoints import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(bills.router, prefix="/bills", tags=["bills"])

@api_router.get("/health")
def health_check():
    return {"status": "ok", "message": "Pásame API is running"}
