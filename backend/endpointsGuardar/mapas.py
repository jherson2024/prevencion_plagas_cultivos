from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()

# ==========================
# MAPA_PARCELA
# ==========================

@router.get("/parcelas", tags=["Mapas"])
def listar_mapas_parcela():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM MAPA_PARCELA WHERE MapEstReg = 'A'")
        mapas = cursor.fetchall()
        cursor.close()
        conn.close()
        return mapas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/parcela/crear", tags=["Mapas"])
def crear_mapa_parcela(MapUsuCod: int, MapZonGeoCod: int, MapImaMap: str, MapAnc: int, MapAlt: int,
                       MapFecSub: str, MapNom: str, MapCom: str, MapEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MAPA_PARCELA (MapUsuCod, MapZonGeoCod, MapImaMap, MapAnc, MapAlt, MapFecSub, MapNom, MapCom, MapEstReg)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (MapUsuCod, MapZonGeoCod, MapImaMap, MapAnc, MapAlt, MapFecSub, MapNom, MapCom, MapEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Mapa de parcela registrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================
# CAPA_MAPA
# ==========================

@router.get("/capas", tags=["Mapas"])
def listar_capas_mapa():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CAPA_MAPA WHERE CapEstReg = 'A'")
        capas = cursor.fetchall()
        cursor.close()
        conn.close()
        return capas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/capa/crear", tags=["Mapas"])
def crear_capa_mapa(CapUsuCod: int, CapNom: str, CapTipVis: str, CapFilApl: str, CapEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CAPA_MAPA (CapUsuCod, CapNom, CapTipVis, CapFilApl, CapEstReg)
            VALUES (%s, %s, %s, %s, %s)
        """, (CapUsuCod, CapNom, CapTipVis, CapFilApl, CapEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Capa de mapa registrada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
