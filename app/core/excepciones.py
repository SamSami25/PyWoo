# app/core/excepciones.py
class PyWooError(Exception):
    """Excepción base del proyecto PyWoo"""
    pass


class ConfiguracionError(PyWooError):
    """Errores relacionados con configuración y credenciales"""
    pass


class WooCommerceConexionError(PyWooError):
    """Errores de conexión con WooCommerce"""
    pass
