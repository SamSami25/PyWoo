# app/core/credenciales_controller.py
from app.core.configuracion import guardar_configuracion

class CredencialesController:
    def guardar(self, url, ck, cs):
        if not all([url, ck, cs]):
            raise ValueError("Todos los campos son obligatorios")

        guardar_configuracion(url, ck, cs)
