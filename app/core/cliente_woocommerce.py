# app/core/cliente_woocommerce.py
from __future__ import annotations

import requests
from typing import Any, Dict, List, Optional

from app.core.configuracion import Configuracion
from app.core.excepciones import WooCommerceConexionError


def _safe_int(x: Any, default: int = 0) -> int:
    try:
        if x is None or x == "":
            return default
        return int(float(x))
    except Exception:
        return default


class ClienteWooCommerce:
    def __init__(self, override_cred: Optional[dict] = None):
        config = Configuracion()
        cred = config.obtener_credenciales() or {}

        # ✅ Permite probar conexión sin guardar (override)
        if override_cred:
            cred = {
                "url": override_cred.get("url", cred.get("url", "")),
                "consumer_key": override_cred.get("consumer_key", cred.get("consumer_key", "")),
                "consumer_secret": override_cred.get("consumer_secret", cred.get("consumer_secret", "")),
            }

        url = (cred.get("url") or "").strip().rstrip("/")
        ck = (cred.get("consumer_key") or "").strip()
        cs = (cred.get("consumer_secret") or "").strip()

        if not url or not ck or not cs:
            raise WooCommerceConexionError("Credenciales incompletas: URL/CK/CS")

        self.base_url = f"{url}/wp-json/wc/v3"
        self.auth = (ck, cs)

    # ---------------------------
    # HTTP helper (errores claros)
    # ---------------------------
    def _request(self, method: str, path: str, *, params=None, json=None, timeout: int = 30):
        url = f"{self.base_url}{path}"
        try:
            r = requests.request(
                method=method,
                url=url,
                auth=self.auth,
                params=params,
                json=json,
                timeout=timeout,
            )
            if not r.ok:
                try:
                    payload = r.json()
                    msg = payload.get("message") or str(payload)
                except Exception:
                    msg = r.text[:300]
                raise WooCommerceConexionError(f"{r.status_code} {r.reason}: {msg}")
            return r
        except WooCommerceConexionError:
            raise
        except Exception as e:
            raise WooCommerceConexionError(str(e))

    def probar_conexion(self) -> bool:
        self._request("GET", "/system_status", timeout=10)
        return True

    # ---------------------------
    # Orders
    # ---------------------------
    def obtener_pedidos(self, desde=None, hasta=None, per_page=100) -> List[dict]:
        page = 1
        todos: List[dict] = []
        while True:
            params = {"per_page": per_page, "page": page}
            if desde:
                params["after"] = f"{desde}T00:00:00"
            if hasta:
                params["before"] = f"{hasta}T23:59:59"

            r = self._request("GET", "/orders", params=params, timeout=30)
            data = r.json()
            if not data:
                break
            todos.extend(data)
            page += 1
        return todos

    def obtener_ordenes(self, *args, **kwargs):
        return self.obtener_pedidos(*args, **kwargs)

    # ---------------------------
    # Products
    # ---------------------------
    def obtener_productos(self, per_page=100, filtro_stock=None, incluir_variaciones: bool = False) -> List[dict]:
        page = 1
        productos: List[dict] = []

        while True:
            params = {"per_page": per_page, "page": page}
            r = self._request("GET", "/products", params=params, timeout=30)
            data = r.json()
            if not data:
                break
            productos.extend(data)
            page += 1

        if filtro_stock in ("sin_stock", "con_stock"):
            filtrados = []
            for p in productos:
                stock = _safe_int(p.get("stock_quantity"), 0)
                if filtro_stock == "sin_stock" and stock <= 0:
                    filtrados.append(p)
                if filtro_stock == "con_stock" and stock > 0:
                    filtrados.append(p)
            productos = filtrados

        if not incluir_variaciones:
            return productos

        aplanados: List[dict] = []
        for p in productos:
            aplanados.append(p)

            tipo = (p.get("type") or "").strip().lower()
            if tipo != "variable":
                continue

            parent_id = p.get("id")
            if not parent_id:
                continue

            variaciones = self.obtener_variaciones_producto(int(parent_id), per_page=per_page)
            for v in variaciones:
                v2 = dict(v)
                v2["type"] = "variation"
                v2["parent_id"] = int(parent_id)
                if not v2.get("name"):
                    attrs = v2.get("attributes") or []
                    detalle = ", ".join(f"{a.get('name','')}: {a.get('option','')}".strip() for a in attrs)
                    base_name = (p.get("name") or "").strip()
                    v2["name"] = f"{base_name} ({detalle})" if detalle else base_name
                aplanados.append(v2)

        return aplanados

    def obtener_variaciones_producto(self, producto_id: int, per_page: int = 100) -> List[dict]:
        page = 1
        todos: List[dict] = []
        while True:
            params = {"per_page": per_page, "page": page}
            r = self._request("GET", f"/products/{producto_id}/variations", params=params, timeout=30)
            data = r.json()
            if not data:
                break
            todos.extend(data)
            page += 1
        return todos

    # ---------------------------
    # Updates
    # ---------------------------
    def actualizar_producto(self, producto_id: int, stock=None, precio=None) -> dict:
        data: Dict[str, Any] = {}

        if stock is not None:
            data["manage_stock"] = True
            data["stock_quantity"] = int(stock)

        if precio is not None:
            data["regular_price"] = f"{float(precio):.2f}"

        if not data:
            return {"ok": True, "message": "Sin cambios"}

        r = self._request("PUT", f"/products/{producto_id}", json=data, timeout=30)
        return r.json()

    def actualizar_variacion(self, parent_id: int, variacion_id: int, stock=None, precio=None) -> dict:
        data: Dict[str, Any] = {}

        if stock is not None:
            data["manage_stock"] = True
            data["stock_quantity"] = int(stock)

        if precio is not None:
            data["regular_price"] = f"{float(precio):.2f}"

        if not data:
            return {"ok": True, "message": "Sin cambios"}

        r = self._request(
            "PUT",
            f"/products/{parent_id}/variations/{variacion_id}",
            json=data,
            timeout=30,
        )
        return r.json()
