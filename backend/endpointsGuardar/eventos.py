from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# EVENTO_USUARIO
# ==========================

@router.get("/", tags=["Eventos"])
def listar_eventos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM EVENTO_USUARIO WHERE EveEstReg = 'A'")
        eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usuario/{EveUsuCod}", tags=["Eventos"])
def eventos_por_usuario(EveUsuCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM EVENTO_USUARIO WHERE EveUsuCod = %s AND EveEstReg = 'A'", (EveUsuCod,))
        eventos = cursor.fetchall()
        cursor.close()
        conn.close()
        return eventos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Eventos"])
def crear_evento(EveUsuCod: int, EveAcc: str, EveFecHor: str, EveDet: str, EveEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO EVENTO_USUARIO (EveUsuCod, EveAcc, EveFecHor, EveDet, EveEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (EveUsuCod, EveAcc, EveFecHor, EveDet, EveEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Evento registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
