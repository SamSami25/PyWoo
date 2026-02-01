# app/core/configuracion.py
import os
import json

from app.core.rutas import obtener_directorio_app
from app.core.excepciones import ConfiguracionError


class Configuracion:
    ARCHIVO = "credenciales.json"

    def __init__(self):
        self.ruta = os.path.join(obtener_directorio_app(), self.ARCHIVO)

    def obtener_credenciales(self) -> dict:
        if not os.path.exists(self.ruta):
            raise ConfiguracionError("Credenciales no configuradas")

        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            raise ConfiguracionError("El archivo de credenciales está corrupto o inválido")

        url = (data.get("url") or "").strip()
        ck = (data.get("consumer_key") or "").strip()
        cs = (data.get("consumer_secret") or "").strip()

        if not url or not ck or not cs:
            raise ConfiguracionError("Credenciales incompletas")

        return {"url": url, "consumer_key": ck, "consumer_secret": cs}

    def guardar_credenciales(self, url: str, consumer_key: str, consumer_secret: str):
        data = {
            "url": url.strip(),
            "consumer_key": consumer_key.strip(),
            "consumer_secret": consumer_secret.strip()
        }

        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)

        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
