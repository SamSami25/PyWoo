# app/core/rutas.py
import os


def obtener_directorio_app():
    base = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
    ruta = os.path.join(base, "PyWoo")
    os.makedirs(ruta, exist_ok=True)
    return ruta
