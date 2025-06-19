from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# API_KEY
# ==========================

@router.get("/", tags=["API Key"])
def listar_claves():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM API_KEY WHERE ApiEstReg = 'A'")
        claves = cursor.fetchall()
        cursor.close()
        conn.close()
        return claves
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["API Key"])
def crear_clave(ApiUsuCod: int, ApiCla: str, ApiFecEmi: str, ApiAct: str, ApiNivAcc: str, ApiEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO API_KEY (ApiUsuCod, ApiCla, ApiFecEmi, ApiAct, ApiNivAcc, ApiEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ApiUsuCod, ApiCla, ApiFecEmi, ApiAct, ApiNivAcc, ApiEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Clave API registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
