from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import ConfiguracionError, WooCommerceConexionError


class CredencialesController:
    """
    Controlador encargado de gestionar credenciales WooCommerce.
    """

    def __init__(self):
        self.config = Configuracion()

    def cargar_credenciales(self):
        return self.config.obtener_credenciales()

    def guardar_credenciales(self, url, consumer_key, consumer_secret):
        if not url or not consumer_key or not consumer_secret:
            raise ConfiguracionError("Todos los campos son obligatorios")

        self.config.guardar_credenciales(
            url=url,
            ck=consumer_key,
            cs=consumer_secret
        )

    def probar_conexion(self, url, consumer_key, consumer_secret):
        cliente = ClienteWooCommerce(
            url=url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )
        return cliente.probar_conexion()
