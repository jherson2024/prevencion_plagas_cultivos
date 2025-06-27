import google.generativeai as genai
from PIL import Image
import json
import re

# Configura tu API KEY de Gemini
genai.configure(api_key="API_KEY")

# Define el modelo
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

def detectar_gemini(ruta_imagen: str) -> dict:
    """
    Analiza una imagen de cultivo y retorna un dict con los datos:
    {
        "plaga_detectada": bool,
        "nombre_plaga": str | None,
        "severidad": str | None,
        "acciones_recomendadas": str | None
    }
    """
    try:
        image = Image.open(ruta_imagen)

        prompt = """
        Analiza esta imagen de una planta o cultivo y responde lo siguiente en formato JSON:
        Solo responde con el JSON. No agregues texto adicional.
        {
          "plaga_detectada": bool,
          "nombre_plaga": string | null,
          "severidad": string | null,
          "acciones_recomendadas": string | null
        }
        """

        response = model.generate_content([prompt, image])
        texto = response.text.strip()
        print("respuesta gemini")
        print(texto)
        # Extraer JSON con regex
        match = re.search(r'\{[\s\S]*\}', texto)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)
        else:
            return {
                "plaga_detectada": False,
                "nombre_plaga": None,
                "severidad": None,
                "acciones_recomendadas": None
            }

    except Exception as e:
        print("error")
        print(e)
        # En caso de error, devuelve una detección vacía
        return {
            "plaga_detectada": False,
            "nombre_plaga": None,
            "severidad": None,
            "acciones_recomendadas": None,
            "error": str(e)
        }
