# app/core/cliente_woocommerce.py
import requests
from app.core.configuracion import cargar_configuracion

class WooCommerceClient:
    def __init__(self):
        cfg = cargar_configuracion()
        if not all(cfg.values()):
            raise RuntimeError("Credenciales WooCommerce no configuradas")

        self.base_url = f"{cfg['WOO_BASE_URL']}/wp-json/wc/v3"
        self.auth = (cfg["CONSUMER_KEY"], cfg["CONSUMER_SECRET"])

    def get(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            auth=self.auth,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data):
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            auth=self.auth,
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
