from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# CLIMA
# ==========================

@router.get("/", tags=["Clima"])
def listar_clima():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CLIMA WHERE CliEstReg = 'A'")
        clima = cursor.fetchall()
        cursor.close()
        conn.close()
        return clima
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/zona/{CliZonGeoCod}", tags=["Clima"])
def clima_por_zona(CliZonGeoCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CLIMA WHERE CliZonGeoCod = %s AND CliEstReg = 'A'", (CliZonGeoCod,))
        datos = cursor.fetchall()
        cursor.close()
        conn.close()
        return datos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Clima"])
def registrar_clima(CliFec: str, CliZonGeoCod: int, CliTem: float, CliHum: float, CliLlu: float, CliFue: str, CliEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CLIMA (CliFec, CliZonGeoCod, CliTem, CliHum, CliLlu, CliFue, CliEstReg)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (CliFec, CliZonGeoCod, CliTem, CliHum, CliLlu, CliFue, CliEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Registro de clima guardado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
