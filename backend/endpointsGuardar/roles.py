from fastapi import APIRouter

router = APIRouter()

@router.get("/usuarios/{UsuCod}/roles")
def obtener_roles_usuario(UsuCod: int):
    pass

@router.post("/usuarios/{UsuCod}/roles/asignar")
def asignar_rol_usuario(UsuCod: int, rol_id: int):
    pass
