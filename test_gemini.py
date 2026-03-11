import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options={'api_version': 'v1'}
)

try:
    print("--- Intentando con el modelo encontrado ---")
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", # Usa exactamente el nombre que te salió (ej. gemini-2.0-flash-lite)
        contents="Hola, confirma si recibes este mensaje."
    )
    print(f"Respuesta de Gemini: {response.text}")
except Exception as e:
    print(f"Error: {e}")