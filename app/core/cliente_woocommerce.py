# app/core/cliente_woocommerce.py
import requests
from decimal import Decimal, ROUND_HALF_UP

from app.core.configuracion import Configuracion
from app.core.excepciones import WooCommerceConexionError


class ClienteWooCommerce:
    def __init__(self):
        config = Configuracion()
        cred = config.obtener_credenciales()

        self.base_url = f"{cred['url'].rstrip('/')}/wp-json/wc/v3"
        self.auth = (cred["consumer_key"], cred["consumer_secret"])
        self.session = requests.Session()

    def probar_conexion(self):
        try:
            r = self.session.get(
                f"{self.base_url}/system_status",
                auth=self.auth,
                timeout=10
            )
            r.raise_for_status()
            return True
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def obtener_pedidos(self, desde=None, hasta=None, per_page=100):
        page = 1
        todos = []
        try:
            while True:
                params = {"per_page": per_page, "page": page, "status": "any"}
                if desde:
                    params["after"] = f"{desde}T00:00:00"
                if hasta:
                    params["before"] = f"{hasta}T23:59:59"

                r = self.session.get(
                    f"{self.base_url}/orders",
                    auth=self.auth,
                    params=params,
                    timeout=30
                )
                r.raise_for_status()

                data = r.json() or []
                if not data:
                    break

                todos.extend(data)

                if len(data) < per_page:
                    break

                page += 1

            return todos
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def obtener_ordenes(self, *args, **kwargs):
        return self.obtener_pedidos(*args, **kwargs)

    def obtener_productos(self, per_page=100, filtro_stock=None):
        page = 1
        todos = []
        try:
            while True:
                params = {"per_page": per_page, "page": page}

                r = self.session.get(
                    f"{self.base_url}/products",
                    auth=self.auth,
                    params=params,
                    timeout=30
                )
                r.raise_for_status()

                productos = r.json() or []
                if not productos:
                    break

                todos.extend(productos)

                if len(productos) < per_page:
                    break

                page += 1

            if filtro_stock == "sin_stock":
                todos = [p for p in todos if int(p.get("stock_quantity") or 0) <= 0]
            elif filtro_stock == "con_stock":
                todos = [p for p in todos if int(p.get("stock_quantity") or 0) > 0]

            return todos
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def obtener_variaciones_producto(self, producto_id: int, per_page: int = 100):
        page = 1
        todos = []
        try:
            while True:
                params = {"per_page": per_page, "page": page}
                r = self.session.get(
                    f"{self.base_url}/products/{producto_id}/variations",
                    auth=self.auth,
                    params=params,
                    timeout=30
                )
                r.raise_for_status()

                data = r.json() or []
                if not data:
                    break

                todos.extend(data)

                if len(data) < per_page:
                    break

                page += 1

            return todos
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def actualizar_producto(self, producto_id: int, stock=None, precio=None):
        data = {}

        if stock is not None:
            data["manage_stock"] = True
            data["stock_quantity"] = int(stock)

        if precio is not None:
            p = Decimal(str(precio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            data["regular_price"] = f"{p:.2f}"

        try:
            r = self.session.put(
                f"{self.base_url}/products/{producto_id}",
                auth=self.auth,
                json=data,
                timeout=30
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def actualizar_variacion(self, producto_id: int, variacion_id: int, stock=None, precio=None):
        data = {}

        if stock is not None:
            data["manage_stock"] = True
            data["stock_quantity"] = int(stock)

        if precio is not None:
            p = Decimal(str(precio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            data["regular_price"] = f"{p:.2f}"

        try:
            r = self.session.put(
                f"{self.base_url}/products/{producto_id}/variations/{variacion_id}",
                auth=self.auth,
                json=data,
                timeout=30
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def obtener_sku_producto(self, producto_id: int) -> str:
        try:
            r = self.session.get(
                f"{self.base_url}/products/{producto_id}",
                auth=self.auth,
                timeout=30,
            )
            r.raise_for_status()
            return (r.json().get("sku") or "").strip()
        except Exception:
            return ""

    def obtener_sku_variacion(self, variacion_id: int) -> str:
        return ""
