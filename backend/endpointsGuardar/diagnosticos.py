from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# Listar diagnósticos activos
@router.get("/", tags=["Diagnósticos"])
def listar_diagnosticos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DIAGNOSTICO WHERE DiaEstReg = 'A'")
        diagnosticos = cursor.fetchall()
        cursor.close()
        conn.close()
        return diagnosticos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener diagnóstico por código
@router.get("/{DiaCod}", tags=["Diagnósticos"])
def obtener_diagnostico(DiaCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM DIAGNOSTICO WHERE DiaCod = %s", (DiaCod,))
        diagnostico = cursor.fetchone()
        cursor.close()
        conn.close()
        if diagnostico:
            return diagnostico
        else:
            raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Crear diagnóstico nuevo
@router.post("/crear", tags=["Diagnósticos"])
def crear_diagnostico(DiaCapCod: int, DiaPlaCod: int, DiaCulCod: int, DiaNivDañ: float, DiaCon: float, DiaMod: str, DiaFec: str, DiaEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DIAGNOSTICO (DiaCapCod, DiaPlaCod, DiaCulCod, DiaNivDañ, DiaCon, DiaMod, DiaFec, DiaEstReg)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (DiaCapCod, DiaPlaCod, DiaCulCod, DiaNivDañ, DiaCon, DiaMod, DiaFec, DiaEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Diagnóstico registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
