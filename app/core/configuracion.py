# app/core/configuracion.py
import os
from dotenv import set_key, load_dotenv

ENV_PATH = ".env"

load_dotenv()

def guardar_configuracion(url, consumer_key, consumer_secret):
    set_key(ENV_PATH, "WOO_BASE_URL", url)
    set_key(ENV_PATH, "CONSUMER_KEY", consumer_key)
    set_key(ENV_PATH, "CONSUMER_SECRET", consumer_secret)

def cargar_configuracion():
    return {
        "WOO_BASE_URL": os.getenv("WOO_BASE_URL"),
        "CONSUMER_KEY": os.getenv("CONSUMER_KEY"),
        "CONSUMER_SECRET": os.getenv("CONSUMER_SECRET"),
    }

def configuracion_completa():
    cfg = cargar_configuracion()
    return all(cfg.values())
