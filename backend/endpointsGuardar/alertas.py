from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# ALERTA
# ==========================

@router.get("/", tags=["Alertas"])
def listar_alertas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ALERTA WHERE AleEstReg = 'A'")
        alertas = cursor.fetchall()
        cursor.close()
        conn.close()
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Alertas"])
def crear_alerta(AleTip: str, AleMen: str, AleGra: str, AleFecGen: str, AleEst: str, AleEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ALERTA (AleTip, AleMen, AleGra, AleFecGen, AleEst, AleEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (AleTip, AleMen, AleGra, AleFecGen, AleEst, AleEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Alerta registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
# USUARIO_ALERTA
# ==========================

@router.get("/usuario/{UsuUsuCod}", tags=["Alertas"])
def listar_alertas_usuario(UsuUsuCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM USUARIO_ALERTA WHERE UsuUsuCod = %s AND UsuEstReg = 'A'
        """, (UsuUsuCod,))
        usuario_alertas = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuario_alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/usuario/registrar", tags=["Alertas"])
def registrar_alerta_usuario(UsuUsuCod: int, UsuAleCod: int, UsuLei: str, UsuFecLec: str, UsuEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USUARIO_ALERTA (UsuUsuCod, UsuAleCod, UsuLei, UsuFecLec, UsuEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (UsuUsuCod, UsuAleCod, UsuLei, UsuFecLec, UsuEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Alerta registrada para el usuario"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
