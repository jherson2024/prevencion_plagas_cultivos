import json
import re
from PIL import Image

# Simulación de análisis con ChatGPT
def detectar_chatgpt(ruta_imagen: str) -> dict:
    """
    Simula el análisis de una imagen usando ChatGPT.
    """
    try:
        # En un caso real deberías llamar a una API o modelo tuyo.
        # Aquí vamos a simularlo con valores fijos:
        imagen = Image.open(ruta_imagen)  # Validación de existencia

        # Simulación de análisis (puedes integrar OpenAI Vision si es necesario)
        respuesta = """
        {
            "plaga_detectada": true,
            "nombre_plaga": "Pulgón verde",
            "severidad": "media",
            "acciones_recomendadas": "Aplicar jabón potásico y monitorear cada 3 días"
        }
        """
        return json.loads(respuesta)

    except Exception as e:
        return {
            "plaga_detectada": False,
            "nombre_plaga": None,
            "severidad": None,
            "acciones_recomendadas": None,
            "error": str(e)
        }
