import requests
from app.core.configuracion import Configuracion
from app.core.excepciones import WooCommerceConexionError


class ClienteWooCommerce:
    def __init__(self):
        config = Configuracion()
        cred = config.obtener_credenciales()

        self.base_url = f"{cred['url'].rstrip('/')}/wp-json/wc/v3"
        self.auth = (cred["consumer_key"], cred["consumer_secret"])

    # -------------------------------------------------
    # CONEXIÓN
    # -------------------------------------------------
    def probar_conexion(self):
        try:
            r = requests.get(
                f"{self.base_url}/system_status",
                auth=self.auth,
                timeout=10
            )
            r.raise_for_status()
            return True
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    # -------------------------------------------------
    # PEDIDOS / ÓRDENES (TODOS)
    # -------------------------------------------------
    def obtener_pedidos(self, desde=None, hasta=None, per_page=100):
        page = 1
        todos = []

        try:
            while True:
                params = {
                    "per_page": per_page,
                    "page": page
                }

                if desde:
                    params["after"] = f"{desde}T00:00:00"
                if hasta:
                    params["before"] = f"{hasta}T23:59:59"

                r = requests.get(
                    f"{self.base_url}/orders",
                    auth=self.auth,
                    params=params,
                    timeout=30
                )
                r.raise_for_status()

                data = r.json()
                if not data:
                    break

                todos.extend(data)
                page += 1

            return todos

        except Exception as e:
            raise WooCommerceConexionError(str(e))

    # alias
    def obtener_ordenes(self, *args, **kwargs):
        return self.obtener_pedidos(*args, **kwargs)

    # -------------------------------------------------
    # PRODUCTOS (TODOS)
    # -------------------------------------------------
    def obtener_productos(self, per_page=100, filtro_stock=None):
        page = 1
        todos = []

        try:
            while True:
                params = {
                    "per_page": per_page,
                    "page": page
                }

                r = requests.get(
                    f"{self.base_url}/products",
                    auth=self.auth,
                    params=params,
                    timeout=30
                )
                r.raise_for_status()

                productos = r.json()
                if not productos:
                    break

                todos.extend(productos)
                page += 1

            # Filtros de inventario
            if filtro_stock == "sin_stock":
                todos = [
                    p for p in todos
                    if int(p.get("stock_quantity") or 0) <= 0
                ]
            elif filtro_stock == "con_stock":
                todos = [
                    p for p in todos
                    if int(p.get("stock_quantity") or 0) > 0
                ]

            return todos

        except Exception as e:
            raise WooCommerceConexionError(str(e))

    # -------------------------------------------------
    # ACTUALIZAR PRODUCTO
    # -------------------------------------------------
    def actualizar_producto(self, producto_id: int, stock=None, precio=None):
        data = {}

        if stock is not None:
            data["stock_quantity"] = int(stock)

        if precio is not None:
            data["regular_price"] = str(precio)

        try:
            r = requests.put(
                f"{self.base_url}/products/{producto_id}",
                auth=self.auth,
                json=data,
                timeout=30
            )
            r.raise_for_status()
            return r.json()
        except Exception as e:
            raise WooCommerceConexionError(str(e))
