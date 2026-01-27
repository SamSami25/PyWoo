import os
import json
from app.core.rutas import obtener_directorio_app
from app.core.excepciones import ConfiguracionError


class Configuracion:
    ARCHIVO = "credenciales.json"

    def __init__(self):
        self.ruta = os.path.join(obtener_directorio_app(), self.ARCHIVO)

    def obtener_credenciales(self):
        if not os.path.exists(self.ruta):
            raise ConfiguracionError("Credenciales no configuradas")

        with open(self.ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("url") or not data.get("consumer_key") or not data.get("consumer_secret"):
            raise ConfiguracionError("Credenciales incompletas")

        return data

    def guardar_credenciales(self, url, consumer_key, consumer_secret):
        data = {
            "url": url.strip(),
            "consumer_key": consumer_key.strip(),
            "consumer_secret": consumer_secret.strip()
        }

        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
