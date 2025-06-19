from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# USO_API_LOG
# ==========================

@router.get("/", tags=["Uso API"])
def listar_uso_api():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USO_API_LOG WHERE UsoEstReg = 'A'")
        registros = cursor.fetchall()
        cursor.close()
        conn.close()
        return registros
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/registrar", tags=["Uso API"])
def registrar_uso_api(UsoApiKeyCod: int, UsoFecHor: str, UsoEnd: str, UsoExi: str, UsoMenRes: str, UsoEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USO_API_LOG (UsoApiKeyCod, UsoFecHor, UsoEnd, UsoExi, UsoMenRes, UsoEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (UsoApiKeyCod, UsoFecHor, UsoEnd, UsoExi, UsoMenRes, UsoEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Uso de API registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
