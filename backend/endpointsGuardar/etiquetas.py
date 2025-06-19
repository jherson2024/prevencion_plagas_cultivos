from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# Listar todas las etiquetas activas
@router.get("/", tags=["Etiquetas"])
def listar_etiquetas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ETIQUETA_MANUAL WHERE EtiEstReg = 'A'")
        etiquetas = cursor.fetchall()
        cursor.close()
        conn.close()
        return etiquetas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener una etiqueta por código
@router.get("/{EtiCod}", tags=["Etiquetas"])
def obtener_etiqueta(EtiCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ETIQUETA_MANUAL WHERE EtiCod = %s", (EtiCod,))
        etiqueta = cursor.fetchone()
        cursor.close()
        conn.close()
        if etiqueta:
            return etiqueta
        else:
            raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Crear una nueva etiqueta manual
@router.post("/crear", tags=["Etiquetas"])
def crear_etiqueta(EtiDiaCod: int, EtiUsuCod: int, EtiPlaCor: str, EtiObs: str, EtiFec: str, EtiEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ETIQUETA_MANUAL (EtiDiaCod, EtiUsuCod, EtiPlaCor, EtiObs, EtiFec, EtiEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (EtiDiaCod, EtiUsuCod, EtiPlaCor, EtiObs, EtiFec, EtiEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Etiqueta registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
