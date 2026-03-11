import json
import requests
import logging
import time
from google import genai
from google.genai import errors
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class AIDocumentExtractor:
    
    @staticmethod
    def extract_document_data(file_url: str) -> dict:
        client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
            http_options={'api_version': 'v1'}
        )
        
        # El modelo que confirmamos que funciona en tu cuenta
        MODEL_NAME = "gemini-2.0-flash-lite"

        try:
            # 1. Descargar el documento
            response = requests.get(file_url, timeout=15)
            response.raise_for_status()
            
            prompt = """
            Analiza este comprobante de domicilio. 
            Extrae y devuelve ÚNICAMENTE un JSON con:
            {
                "extracted_name": "Nombre completo",
                "extracted_address": "Dirección completa",
                "extracted_date": "YYYY-MM-DD"
            }
            """

            # 2. Llamada a la IA
            result = client.models.generate_content(
                model=MODEL_NAME,
                contents=[
                    prompt,
                    {
                        "mime_type": response.headers.get('Content-Type', 'application/pdf'),
                        "data": response.content
                    }
                ],
                config={"response_mime_type": "application/json"}
            )

            return json.loads(result.text)

        except errors.ClientError as e:
            if "429" in str(e):
                logger.error("Error 429: Cuota excedida temporalmente.")
                return {"error": "Servicio de IA saturado, intente en 30 segundos."}
            raise e
        except Exception as e:
            logger.error(f"Error inesperado en extracción: {str(e)}")
            return {"error": str(e)}