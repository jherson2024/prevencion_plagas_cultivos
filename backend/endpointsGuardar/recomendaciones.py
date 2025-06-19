from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# RECOMENDACION
# ==========================

@router.get("/", tags=["Recomendaciones"])
def listar_recomendaciones():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM RECOMENDACION WHERE RecEstReg = 'A'")
        recomendaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return recomendaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crear", tags=["Recomendaciones"])
def crear_recomendacion(RecPlaCod: int, RecCulCod: int, RecNivDañ: float, RecAccSug: str, RecEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RECOMENDACION (RecPlaCod, RecCulCod, RecNivDañ, RecAccSug, RecEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (RecPlaCod, RecCulCod, RecNivDañ, RecAccSug, RecEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Recomendación registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==========================
# RECOMENDACION_APLICADA
# ==========================

@router.get("/aplicadas", tags=["Recomendaciones Aplicadas"])
def listar_recomendaciones_aplicadas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM RECOMENDACION_APLICADA WHERE RecEstReg = 'A'")
        aplicadas = cursor.fetchall()
        cursor.close()
        conn.close()
        return aplicadas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/aplicada", tags=["Recomendaciones Aplicadas"])
def aplicar_recomendacion(RecUsuCod: int, RecRecCod: int, RecFec: str, RecCom: str, RecEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO RECOMENDACION_APLICADA (RecUsuCod, RecRecCod, RecFec, RecCom, RecEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (RecUsuCod, RecRecCod, RecFec, RecCom, RecEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Recomendación aplicada registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
