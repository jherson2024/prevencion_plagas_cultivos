from fastapi import APIRouter, HTTPException
import mysql.connector
from config import DB_CONFIG

router = APIRouter()

@router.get("/usuarios/{UsuCod}/suscripcion")
def obtener_suscripcion_usuario(UsuCod: int):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            p.PlaNom AS plan,
            s.SusFecIni AS fecha_inicio,
            s.SusFecFin AS fecha_fin,
            s.SusEst AS estado
        FROM SUSCRIPCION s
        JOIN PLAN p ON s.SusPlaCod = p.PlaCod
        WHERE s.SusUsuCod = %s
        ORDER BY s.SusFecIni DESC
        LIMIT 1;
    """
    cursor.execute(query, (UsuCod,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Suscripción no encontrada")

    return result
