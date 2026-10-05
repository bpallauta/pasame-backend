from fastapi import APIRouter
from pydantic import BaseModel
import base64
from app.schemas.bill import BillResultSchema
from app.schemas.debt import SendChargeRequest, SendChargeResponse
from app.core.ocr import get_ocr_service

router = APIRouter()

class ScanBillRequest(BaseModel):
    image_base64: str

@router.post("/scan", response_model=BillResultSchema)
async def scan_bill(request: ScanBillRequest):
    ocr_service = get_ocr_service()
    image_bytes = base64.b64decode(request.image_base64)
    result = ocr_service.extract_bill(image_bytes)
    
    return result

@router.post("/{bill_id}/send", response_model=SendChargeResponse)
async def send_charges(bill_id: str, request: SendChargeRequest):
    # Mock logic for MVP. We just pretend we saved these debts to the database 
    # and sent emails to everyone.
    return SendChargeResponse(
        message="Emails enviados exitosamente.",
        debts_created=len(request.debts)
    )
