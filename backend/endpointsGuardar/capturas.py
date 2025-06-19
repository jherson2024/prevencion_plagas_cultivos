from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection

router = APIRouter()

# Listar todas las capturas activas
@router.get("/", tags=["Capturas"])
def listar_capturas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CAPTURA WHERE CapEstReg = 'A'")
        capturas = cursor.fetchall()
        cursor.close()
        conn.close()
        return capturas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener captura por código
@router.get("/{CapCod}", tags=["Capturas"])
def obtener_captura(CapCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CAPTURA WHERE CapCod = %s", (CapCod,))
        captura = cursor.fetchone()
        cursor.close()
        conn.close()
        if captura:
            return captura
        else:
            raise HTTPException(status_code=404, detail="Captura no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Registrar nueva captura
@router.post("/crear", tags=["Capturas"])
def crear_captura(CapUsuCod: int, CapImaCod: int, CapUbiCod: int, CapFec: str, CapNot: str, CapEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CAPTURA (CapUsuCod, CapImaCod, CapUbiCod, CapFec, CapNot, CapEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (CapUsuCod, CapImaCod, CapUbiCod, CapFec, CapNot, CapEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Captura registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
