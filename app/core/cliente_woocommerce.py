import requests
from app.core.excepciones import WooCommerceConexionError


class ClienteWooCommerce:
    def __init__(self, url, consumer_key, consumer_secret):
        self.base_url = f"{url.rstrip('/')}/wp-json/wc/v3"
        self.auth = (consumer_key, consumer_secret)

    def probar_conexion(self):
        try:
            response = requests.get(
                f"{self.base_url}/system_status",
                auth=self.auth,
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def obtener_ordenes(self, per_page=10):
        try:
            response = requests.get(
                f"{self.base_url}/orders",
                auth=self.auth,
                params={"per_page": per_page},
                timeout=15
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise WooCommerceConexionError(str(e))
    
    def obtener_productos(self, per_page=100):
        response = requests.get(
            f"{self.base_url}/products",
            auth=self.auth,
            params={"per_page": per_page},
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    
    def actualizar_producto(self, producto_id, data):
        response = requests.put(
            f"{self.base_url}/products/{producto_id}",
            auth=self.auth,
            json=data,
            timeout=15
        )
        response.raise_for_status()
        return response.json()

    def obtener_clientes(self, per_page=100):
        response = requests.get(
            f"{self.base_url}/customers",
            auth=self.auth,
            params={"per_page": per_page},
            timeout=15
        )
        response.raise_for_status()
        return response.json()

