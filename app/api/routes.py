from fastapi import APIRouter
from app.api import bills

api_router = APIRouter()

api_router.include_router(bills.router, prefix="/bills", tags=["bills"])

@api_router.get("/health")
def health_check():
    return {"status": "ok", "message": "Pásame API is running"}
