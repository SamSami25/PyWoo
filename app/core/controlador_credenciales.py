# app/core/controlador_credenciales.py
from __future__ import annotations

from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import WooCommerceConexionError


class ControladorCredenciales:
    def __init__(self):
        self.config = Configuracion()

    def guardar_credenciales(self, url: str, ck: str, cs: str) -> None:
        url = (url or "").strip().rstrip("/")
        ck = (ck or "").strip()
        cs = (cs or "").strip()

        if not url:
            raise ValueError("Debe ingresar la URL de la tienda.")
        if not ck:
            raise ValueError("Debe ingresar el Consumer Key.")
        if not cs:
            raise ValueError("Debe ingresar el Consumer Secret.")

        self.config.guardar_credenciales(url, ck, cs)

    def cargar_credenciales(self) -> dict:
        return self.config.obtener_credenciales() or {}

    def probar_conexion(self, url: str, ck: str, cs: str) -> bool:
        url = (url or "").strip().rstrip("/")
        ck = (ck or "").strip()
        cs = (cs or "").strip()

        if not url:
            raise ValueError("Debe ingresar la URL de la tienda.")
        if not ck:
            raise ValueError("Debe ingresar el Consumer Key.")
        if not cs:
            raise ValueError("Debe ingresar el Consumer Secret.")

        try:
            cliente = ClienteWooCommerce(
                override_cred={
                    "url": url,
                    "consumer_key": ck,
                    "consumer_secret": cs,
                }
            )
            return cliente.probar_conexion()
        except WooCommerceConexionError as e:
            # mensaje listo para mostrar en UI
            raise WooCommerceConexionError(f"No se pudo conectar con WooCommerce: {e}")
