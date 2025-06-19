from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# SYNC_LOG
# ==========================

@router.get("/", tags=["Sync Log"])
def listar_sync_logs():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM SYNC_LOG WHERE SynEstReg = 'A'")
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuario/{SynUsuCod}", tags=["Sync Log"])
def sync_logs_por_usuario(SynUsuCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM SYNC_LOG WHERE SynUsuCod = %s AND SynEstReg = 'A'", (SynUsuCod,))
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Sync Log"])
def registrar_sync_log(SynUsuCod: int, SynFec: str, SynTipSin: str, SynRes: str, SynEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SYNC_LOG (SynUsuCod, SynFec, SynTipSin, SynRes, SynEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (SynUsuCod, SynFec, SynTipSin, SynRes, SynEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Log de sincronización registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
