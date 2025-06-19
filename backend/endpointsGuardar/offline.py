from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# DATOS_OFFLINE_BUFFER
# ==========================

@router.get("/", tags=["Offline Buffer"])
def listar_datos_offline():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DATOS_OFFLINE_BUFFER WHERE DatEstReg = 'A'")
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuario/{DatUsuCod}", tags=["Offline Buffer"])
def datos_offline_por_usuario(DatUsuCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DATOS_OFFLINE_BUFFER WHERE DatUsuCod = %s AND DatEstReg = 'A'", (DatUsuCod,))
        buffer = cursor.fetchall()
        cursor.close()
        conn.close()
        return buffer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Offline Buffer"])
def registrar_dato_offline(DatUsuCod: int, DatTipDat: str, DatCon: str, DatFecCre: str, DatSin: str, DatEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DATOS_OFFLINE_BUFFER (DatUsuCod, DatTipDat, DatCon, DatFecCre, DatSin, DatEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (DatUsuCod, DatTipDat, DatCon, DatFecCre, DatSin, DatEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Dato offline registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
