import json
import logging
import requests
from django.conf import settings
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class AIDocumentExtractor:
    @staticmethod
    def extract_document_data(file_url: str) -> dict:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        MODEL_NAME = "gemini-2.5-flash-lite"

        try:
            response = requests.get(file_url, timeout=15)
            response.raise_for_status()
            
            # Prompt
            prompt = """
            Analiza esta imagen de un comprobante de domicilio.
            Extrae los datos y responde ÚNICAMENTE con el objeto JSON, sin bloques de código, sin ```json, sin texto adicional.
            Formato:
            {
                "extracted_name": "Nombre",
                "extracted_address": "Dirección",
                "extracted_date": "YYYY-MM-DD"
            }
            """

            result = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    types.Part.from_text(text=prompt),
                    types.Part.from_bytes(
                        data=response.content,
                        mime_type="image/jpeg"
                    )
                ]
            )

            if not result or not result.text:
                raise ValueError("La IA no devolvió texto.")

            # Remove markdown characters
            raw_text = result.text.strip()
            if raw_text.startswith("```"):
                # Delete ```json at the beginning and ``` at the end
                raw_text = raw_text.split("```")
                # Look for the part that contains the JSON
                for part in raw_text:
                    if "{" in part:
                        raw_text = part.replace("json", "").strip()
                        break

            return json.loads(raw_text)

        except Exception as e:
            logger.error(f"Error en extracción: {str(e)}")
            return {
                "error": "No se pudo procesar el documento",
                "details": str(e)
            }