# app/core/configuracion.py

import os
from dotenv import load_dotenv, set_key
from app.core.excepciones import ConfiguracionError

ENV_PATH = ".env"


class Configuracion:
    def __init__(self):
        load_dotenv(ENV_PATH)

    def obtener_credenciales(self) -> dict:
        url = os.getenv("WC_URL")
        ck = os.getenv("WC_KEY")
        cs = os.getenv("WC_SECRET")

        if not all([url, ck, cs]):
            raise ConfiguracionError("Credenciales de WooCommerce incompletas.")

        return {
            "url": url,
            "consumer_key": ck,
            "consumer_secret": cs,
        }

    def guardar_credenciales(self, url: str, ck: str, cs: str):
        if not all([url, ck, cs]):
            raise ConfiguracionError("No se permiten credenciales vacías.")

        set_key(ENV_PATH, "WC_URL", url)
        set_key(ENV_PATH, "WC_KEY", ck)
        set_key(ENV_PATH, "WC_SECRET", cs)
