from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# Listar todas las ubicaciones activas
@router.get("/", tags=["Ubicaciones"])
def listar_ubicaciones():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM UBICACION WHERE UbiEstReg = 'A'")
        ubicaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return ubicaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener una ubicación por código
@router.get("/{UbiCod}", tags=["Ubicaciones"])
def obtener_ubicacion(UbiCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM UBICACION WHERE UbiCod = %s", (UbiCod,))
        ubicacion = cursor.fetchone()
        cursor.close()
        conn.close()
        if ubicacion:
            return ubicacion
        else:
            raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Registrar nueva ubicación
@router.post("/crear", tags=["Ubicaciones"])
def crear_ubicacion(UbiMapParCod: int, UbiCoo: float, UbiCooB: float, UbiCom: str, UbiEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO UBICACION (UbiMapParCod, UbiCoo, UbiCooB, UbiCom, UbiEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (UbiMapParCod, UbiCoo, UbiCooB, UbiCom, UbiEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Ubicación registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
