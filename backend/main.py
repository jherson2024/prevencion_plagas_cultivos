from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as routes_app  # Importa el objeto app con las rutas
from fastapi.staticfiles import StaticFiles
from endpoints.RegistroConfiguracionInicial import router as ruta1_router
from endpoints.ZonaTrabajoMapeo import router as ruta2_router
from endpoints.AccesosColaborativos import router as ruta3_router
from endpoints.CapturaDatosCampo import router as ruta4_router
import os

app = FastAPI(
    title="Sistema de Prevención de Plagas Agrícolas",
    version="1.0.0"
)
os.makedirs("static/imagenes", exist_ok=True)
os.makedirs("static/mapas", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas
app.include_router(ruta1_router)
app.include_router(ruta2_router)
app.include_router(ruta3_router)
app.include_router(ruta4_router)
