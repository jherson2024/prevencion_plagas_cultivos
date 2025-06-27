from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from datetime import date
from database import get_connection
import os
from uuid import uuid4
from fastapi import Query
from .chatgpt import detectar_chatgpt
from .gemini import detectar_gemini
from .deepseck import detectar_deepseck

router = APIRouter()
IMAGENES_DIR = "static/imagenes"
os.makedirs(IMAGENES_DIR, exist_ok=True)

# -----------------------------
# Imagen
# -----------------------------
@router.post("/imagen/subir")
async def subir_y_registrar_imagen(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "gif"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido")

    nombre_archivo = f"{uuid4()}.{extension}"
    ruta_fisica = os.path.join(IMAGENES_DIR, nombre_archivo)
    url_publica = f"/static/imagenes/{nombre_archivo}"

    with open(ruta_fisica, "wb") as f:
        contenido = await file.read()
        f.write(contenido)

    tam_kb = os.path.getsize(ruta_fisica) // 1024

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO imagen (
            ImaUrl, ImaTam, ImaRes, ImaFecCap, ImaPro, ImaTipIma, ImaEstReg
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (url_publica, tam_kb, "N/A", date.today(), "No", "cultivo", "A"))
    conn.commit()
    ima_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"ImaCod": ima_id, "url": url_publica, "message": "Imagen subida y registrada"}

@router.delete("/imagen/eliminar/{ImaCod}")
async def eliminar_imagen(ImaCod: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ImaUrl FROM imagen WHERE ImaCod = %s AND ImaEstReg = 'A'", (ImaCod,))
    imagen = cursor.fetchone()

    if not imagen:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    ruta_fisica = "." + imagen["ImaUrl"]
    if os.path.exists(ruta_fisica):
        os.remove(ruta_fisica)

    cursor.execute("UPDATE imagen SET ImaEstReg = 'I' WHERE ImaCod = %s", (ImaCod,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Imagen eliminada"}

# -----------------------------
# Ubicacion
# -----------------------------
@router.post("/ubicacion/crear")
async def crear_ubicacion(request: Request):
    body = await request.json()
    UbiMapParCod = body.get("UbiMapParCod")
    UbiCoo = body.get("UbiCoo")
    UbiCooB = body.get("UbiCooB")
    UbiCom = body.get("UbiCom", "")

    if not all([UbiMapParCod, UbiCoo, UbiCooB]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ubicacion (
            UbiMapParCod, UbiCoo, UbiCooB, UbiCom, UbiEstReg
        ) VALUES (%s, %s, %s, %s, %s)
    """, (UbiMapParCod, UbiCoo, UbiCooB, UbiCom, "A"))
    conn.commit()
    ubi_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"UbiCod": ubi_id, "message": "Ubicación registrada"}

# -----------------------------
# Captura
# -----------------------------
@router.post("/captura/crear")
async def crear_captura(request: Request):
    body = await request.json()
    CapUsuCod = body.get("CapUsuCod")
    CapImaCod = body.get("CapImaCod")
    CapUbiCod = body.get("CapUbiCod")
    CapFec = body.get("CapFec", str(date.today()))
    CapNot = body.get("CapNot", "")

    if not all([CapUsuCod, CapImaCod, CapUbiCod]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO captura (
            CapUsuCod, CapImaCod, CapUbiCod, CapFec, CapNot, CapEstReg
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (CapUsuCod, CapImaCod, CapUbiCod, CapFec, CapNot, "A"))
    conn.commit()
    cap_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"CapCod": cap_id, "message": "Captura registrada"}

# -----------------------------
# Offline Buffer
# -----------------------------
@router.post("/offline_buffer/guardar")
async def guardar_offline(request: Request):
    body = await request.json()
    DatUsuCod = body.get("DatUsuCod")
    DatTipDat = body.get("DatTipDat")
    DatCon = body.get("DatCon")
    DatFecCre = body.get("DatFecCre", str(date.today()))
    DatSin = body.get("DatSin", "pendiente")

    if not all([DatUsuCod, DatTipDat, DatCon]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO datos_offline_buffer (
            DatUsuCod, DatTipDat, DatCon, DatFecCre, DatSin, DatEstReg
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (DatUsuCod, DatTipDat, DatCon, DatFecCre, DatSin, "A"))
    conn.commit()
    dat_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"DatCod": dat_id, "message": "Dato offline guardado"}

# -----------------------------
# Sync Log
# -----------------------------
@router.post("/sync_log/registrar")
async def registrar_sync_log(request: Request):
    body = await request.json()
    SynUsuCod = body.get("SynUsuCod")
    SynFec = body.get("SynFec", str(date.today()))
    SynTipSin = body.get("SynTipSin")
    SynRes = body.get("SynRes")

    if not all([SynUsuCod, SynTipSin, SynRes]):
        raise HTTPException(status_code=400, detail="Datos incompletos")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sync_log (
            SynUsuCod, SynFec, SynTipSin, SynRes, SynEstReg
        ) VALUES (%s, %s, %s, %s, %s)
    """, (SynUsuCod, SynFec, SynTipSin, SynRes, "A"))
    conn.commit()
    sync_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"SynCod": sync_id, "message": "Sincronización registrada"}
@router.get("/imagen/listar/usuario/{UsuCod}")
async def listar_imagenes_por_usuario(UsuCod: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ImaCod, ImaUrl, ImaTam, ImaRes, ImaFecCap, ImaTipIma
        FROM imagen
        WHERE ImaEstReg = 'A' AND ImaCod IN (
            SELECT CapImaCod FROM captura WHERE CapUsuCod = %s AND CapEstReg = 'A'
        )
    """, (UsuCod,))
    imagenes = cursor.fetchall()
    cursor.close()
    conn.close()
    return imagenes


@router.get("/captura/listar")
async def listar_capturas(usu: int = None, parcela: int = None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT c.CapCod, c.CapFec, c.CapNot,
               i.ImaUrl, i.ImaRes, i.ImaTam,
               u.UbiCoo, u.UbiCooB, u.UbiCom
        FROM captura c
        JOIN imagen i ON c.CapImaCod = i.ImaCod
        JOIN ubicacion u ON c.CapUbiCod = u.UbiCod
        WHERE c.CapEstReg = 'A'
    """
    params = []

    if usu:
        query += " AND c.CapUsuCod = %s"
        params.append(usu)
    if parcela:
        query += " AND u.UbiMapParCod = %s"
        params.append(parcela)

    cursor.execute(query, tuple(params))
    capturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return capturas


@router.post("/detecciones/listar")
async def listar_deteccion_por_imagen(request: Request):
    datos = await request.json()
    ima_cod = datos.get("cap_cod")
    ia_nombre = datos.get("ia_nombre")

    if not ima_cod or not ia_nombre:
        raise HTTPException(status_code=400, detail="Faltan datos requeridos")

    if ia_nombre not in ["chatgpt", "gemini", "deepseck"]:
        raise HTTPException(status_code=400, detail="IA no válida")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 1. Obtener URL de imagen
    cursor.execute("SELECT ImaUrl FROM imagen WHERE ImaCod = %s AND ImaEstReg = 'A'", (ima_cod,))
    imagen = cursor.fetchone()
    if not imagen:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    ima_url = imagen["ImaUrl"]

    # 2. Verificar si ya existe detección con esa IA
    cursor.execute("""
        SELECT * FROM deteccion
        WHERE ImaCod = %s AND IauUse = %s
    """, (ima_cod, ia_nombre))
    deteccion = cursor.fetchone()

    if deteccion:
        print("ya hay una deteccion anterior")
        resultado = {
            "ImaUrl": ima_url,
            "PlaDet": deteccion["PlaDet"],
            "NomPla": deteccion["NomPla"],
            "SevPla": deteccion["SevPla"],
            "AccRec": deteccion["AccRec"]
        }
        print(resultado)
    else:
        print("no habia deteccion anterior")
        ruta_local = "." + ima_url
        if ia_nombre == "chatgpt":
            resultado_ia = detectar_chatgpt(ruta_local)
        elif ia_nombre == "gemini":
            resultado_ia = detectar_gemini(ruta_local)
        else:
            resultado_ia = detectar_deepseck(ruta_local)

        # Guardar en base de datos
        cursor.execute("""
            REPLACE INTO deteccion (
                ImaCod, PlaDet, NomPla, SevPla, AccRec, IauUse
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            ima_cod,
            resultado_ia["plaga_detectada"],
            resultado_ia.get("nombre_plaga"),
            resultado_ia.get("severidad"),
            resultado_ia.get("acciones_recomendadas"),
            ia_nombre
        ))
        conn.commit()

        resultado = {
            "ImaUrl": ima_url,
            "PlaDet": resultado_ia["plaga_detectada"],
            "NomPla": resultado_ia.get("nombre_plaga"),
            "SevPla": resultado_ia.get("severidad"),
            "AccRec": resultado_ia.get("acciones_recomendadas")
        }

    cursor.close()
    conn.close()
    return resultado
