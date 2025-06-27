import json
from PIL import Image

def detectar_deepseck(ruta_imagen: str) -> dict:
    """
    Simula una detección con el modelo DeepSeck.
    """
    try:
        imagen = Image.open(ruta_imagen)  # Valida que la imagen existe

        # Simulación de resultado de IA
        resultado = {
            "plaga_detectada": True,
            "nombre_plaga": "Mosca blanca",
            "severidad": "alta",
            "acciones_recomendadas": "Aplicar insecticida biológico y evitar exceso de riego"
        }
        return resultado

    except Exception as e:
        return {
            "plaga_detectada": False,
            "nombre_plaga": None,
            "severidad": None,
            "acciones_recomendadas": None,
            "error": str(e)
        }
