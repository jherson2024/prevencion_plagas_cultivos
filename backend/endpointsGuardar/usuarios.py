from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection

router = APIRouter()

# Obtener todos los usuarios activos
@router.get("/", tags=["Usuarios"])
def listar_usuarios():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USUARIO WHERE UsuEstReg = 'A'")
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Obtener un usuario por código
@router.get("/{UsuCod}", tags=["Usuarios"])
def obtener_usuario(UsuCod: int):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USUARIO WHERE UsuCod = %s", (UsuCod,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario:
            return usuario
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Crear nuevo usuario
@router.post("/crear", tags=["Usuarios"])
def crear_usuario(UsuNom: str, UsuCor: str, UsuCon: str, UsuFecReg: str, UsuEst: str, UsuEstReg: str = 'A'):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USUARIO (UsuNom, UsuCor, UsuCon, UsuFecReg, UsuEst, UsuEstReg)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (UsuNom, UsuCor, UsuCon, UsuFecReg, UsuEst, UsuEstReg))
        conn.commit()
        cursor.close()
        conn.close()
        return {"mensaje": "Usuario creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Login básico por correo y contraseña
@router.post("/login", tags=["Usuarios"])
def login(UsuCor: str, UsuCon: str):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM USUARIO
            WHERE UsuCor = %s AND UsuCon = %s AND UsuEstReg = 'A'
        """, (UsuCor, UsuCon))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        if usuario:
            return {"mensaje": "Login exitoso", "usuario": usuario}
        else:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
