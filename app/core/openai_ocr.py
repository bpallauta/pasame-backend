import os
import json
import base64
from openai import OpenAI
from app.core.ocr import OCRService
from app.schemas.bill import BillResultSchema, BillItemSchema

class OpenAIOCRService(OCRService):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def extract_bill(self, image_bytes: bytes) -> BillResultSchema:
        # Encode bytes to base64 string
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        prompt = """
        Eres un asistente especializado en extraer información de boletas y facturas de restaurantes, especialmente de Chile.
        Analiza la imagen adjunta y extrae la siguiente información en estricto formato JSON:
        - "restaurant": El nombre del restaurante o local.
        - "date": La fecha de la boleta (en formato DD/MM/YYYY si es posible).
        - "items": Una lista de objetos, donde cada uno tiene "name" (nombre del producto) y "price" (precio unitario como entero, sin símbolos de moneda ni puntos).
        - "subtotal": El subtotal antes de propina y descuentos.
        - "tax": Impuestos (opcional, 0 si no aplica).
        - "discount": Descuentos aplicados (opcional, 0 si no aplica).
        - "tip": Propina agregada (opcional, 0 si no aplica).
        - "total": El gran total final de la boleta.

        Ignora el texto irrelevante. Asegúrate de separar claramente los productos consumidos de los ítems como "Propina" o "Descuento".
        Devuelve SOLO el JSON, sin markdown ni explicaciones adicionales.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            response_format={ "type": "json_object" },
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000,
        )

        content = response.choices[0].message.content
        data = json.loads(content)

        items = []
        for item in data.get("items", []):
            items.append(BillItemSchema(name=item.get("name", "Item"), price=int(item.get("price", 0))))

        return BillResultSchema(
            restaurant=data.get("restaurant", "Desconocido"),
            date=data.get("date", ""),
            items=items,
            subtotal=int(data.get("subtotal", 0)),
            tax=int(data.get("tax", 0)),
            discount=int(data.get("discount", 0)),
            tip=int(data.get("tip", 0)),
            total=int(data.get("total", 0))
        )
