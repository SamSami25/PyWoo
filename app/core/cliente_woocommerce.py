# app/core/cliente_woocommerce.py
import requests
from decimal import Decimal, ROUND_HALF_UP
from datetime import date, datetime, time

from app.core.configuracion import Configuracion
from app.core.excepciones import WooCommerceConexionError


class ClienteWooCommerce:
    def __init__(self, override_cred: dict | None = None):
        """
        override_cred opcional para probar conexión sin guardar credenciales.
        Formato esperado:
        {
            "url": "...",
            "consumer_key": "...",
            "consumer_secret": "..."
        }
        """
        if override_cred is not None:
            cred = override_cred
        else:
            config = Configuracion()
            cred = config.obtener_credenciales() or {}

        url = (cred.get("url") or "").strip().rstrip("/")
        ck = (cred.get("consumer_key") or "").strip()
        cs = (cred.get("consumer_secret") or "").strip()

        if not url:
            raise WooCommerceConexionError("URL de WooCommerce no configurada.")
        if not ck:
            raise WooCommerceConexionError("Consumer Key no configurado.")
        if not cs:
            raise WooCommerceConexionError("Consumer Secret no configurado.")

        self.base_url = f"{url}/wp-json/wc/v3"
        self.auth = (ck, cs)

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

    # -----------------------------
    # Helpers de fecha (RFC3339)
    # -----------------------------
    def _to_rfc3339_utc(self, d, end_of_day: bool = False) -> str:
        """
        WooCommerce espera RFC3339 con zona horaria (Z o +00:00).
        Ej: 2026-02-04T00:00:00Z
        """
        if isinstance(d, datetime):
            dt = d
        elif isinstance(d, date):
            dt = datetime.combine(d, time(23, 59, 59) if end_of_day else time(0, 0, 0))
        else:
            return str(d)

        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    def obtener_pedidos(self, desde=None, hasta=None, per_page=100):
        """
        ✅ Filtra correctamente por rango de fechas usando RFC3339 con Z.
        ✅ Incluye status=any para traer todos los estados dentro del rango.
        """
        page = 1
        todos = []
        try:
            while True:
                params = {
                    "per_page": per_page,
                    "page": page,
                    "orderby": "date",
                    "order": "asc",
                    "status": "any",
                }

                if desde:
                    params["after"] = self._to_rfc3339_utc(desde, end_of_day=False)
                if hasta:
                    params["before"] = self._to_rfc3339_utc(hasta, end_of_day=True)

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

    def obtener_ordenes(self, *args, **kwargs):
        return self.obtener_pedidos(*args, **kwargs)

    def obtener_productos(self, per_page=100, filtro_stock=None):
        page = 1
        todos = []
        try:
            while True:
                params = {"per_page": per_page, "page": page}

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
                r = requests.get(
                    f"{self.base_url}/products/{producto_id}/variations",
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

    def actualizar_producto(self, producto_id: int, stock=None, precio=None):
        data = {}

        if stock is not None:
            data["manage_stock"] = True
            data["stock_quantity"] = int(stock)

        if precio is not None:
            p = Decimal(str(precio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            data["regular_price"] = f"{p:.2f}"

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

    def actualizar_variacion(self, producto_id: int, variacion_id: int, stock=None, precio=None):
        data = {}

        if stock is not None:
            data["manage_stock"] = True
            data["stock_quantity"] = int(stock)

        if precio is not None:
            p = Decimal(str(precio)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            data["regular_price"] = f"{p:.2f}"

        try:
            r = requests.put(
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
            r = requests.get(
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
