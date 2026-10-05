from abc import ABC, abstractmethod
from app.schemas.bill import BillResultSchema, BillItemSchema

class OCRService(ABC):
    @abstractmethod
    def extract_bill(self, image_bytes: bytes) -> BillResultSchema:
        pass

class MockOCRService(OCRService):
    def extract_bill(self, image_bytes: bytes) -> BillResultSchema:
        # Mock logic as requested by user in test data
        return BillResultSchema(
            restaurant="Restaurante XYZ",
            date="04/10/2026",
            items=[
                BillItemSchema(name="Hamburguesa", price=12990),
                BillItemSchema(name="Pizza", price=15990),
                BillItemSchema(name="Papas fritas", price=5990),
                BillItemSchema(name="Coca Cola", price=2000),
            ],
            subtotal=36970,
            tax=0,
            discount=0,
            tip=0,
            total=36970
        )

import os
from dotenv import load_dotenv

load_dotenv()

# Factory function to get the current OCR service
def get_ocr_service() -> OCRService:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        from app.core.openai_ocr import OpenAIOCRService
        return OpenAIOCRService(api_key=api_key)
    return MockOCRService()
