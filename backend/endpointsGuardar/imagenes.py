from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# Listar todas las imágenes activas
@router.get("/", tags=["Imágenes"])
def listar_imagenes():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM IMAGEN WHERE ImaEstReg = 'A'")
        imagenes = cursor.fetchall()
        cursor.close()
        conn.close()
        return imagenes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener una imagen por código
@router.get("/{ImaCod}", tags=["Imágenes"])
def obtener_imagen(ImaCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM IMAGEN WHERE ImaCod = %s", (ImaCod,))
        imagen = cursor.fetchone()
        cursor.close()
        conn.close()
        if imagen:
            return imagen
        else:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Registrar una nueva imagen
@router.post("/crear", tags=["Imágenes"])
def crear_imagen(ImaUrl: str, ImaTam: int, ImaRes: str, ImaFecCap: str, ImaPro: str, ImaEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO IMAGEN (ImaUrl, ImaTam, ImaRes, ImaFecCap, ImaPro, ImaEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ImaUrl, ImaTam, ImaRes, ImaFecCap, ImaPro, ImaEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Imagen registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
