# app/core/controlador_credenciales.py

from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce


class ControladorCredenciales:
    def __init__(self):
        self.config = Configuracion()

    def guardar_credenciales(self, url, ck, cs):
        self.config.guardar_credenciales(url, ck, cs)

    def cargar_credenciales(self):
        return self.config.obtener_credenciales()

    def probar_conexion(self):
        cliente = ClienteWooCommerce()
        return cliente.probar_conexion()
