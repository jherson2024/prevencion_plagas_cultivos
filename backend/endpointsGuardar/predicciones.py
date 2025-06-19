from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# PREDICCIONES
# ==========================

@router.get("/", tags=["Predicciones"])
def listar_predicciones():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PREDICCION WHERE PreEstReg = 'A'")
        predicciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return predicciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zona/{PreZonGeoCod}", tags=["Predicciones"])
def predicciones_por_zona(PreZonGeoCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM PREDICCION 
            WHERE PreZonGeoCod = %s AND PreEstReg = 'A'
        """, (PreZonGeoCod,))
        zona_preds = cursor.fetchall()
        cursor.close()
        conn.close()
        return zona_preds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Predicciones"])
def crear_prediccion(PrePlaCod: int, PreZonGeoCod: int, PreFecEst: str, PrePro: float, PreModCod: int, PreEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PREDICCION (PrePlaCod, PreZonGeoCod, PreFecEst, PrePro, PreModCod, PreEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (PrePlaCod, PreZonGeoCod, PreFecEst, PrePro, PreModCod, PreEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Predicción registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
