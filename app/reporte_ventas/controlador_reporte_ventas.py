from app.core.cliente_woocommerce import WooCommerceClient


class VentasController:
    def __init__(self):
        self.client = WooCommerceClient()

    def obtener_ventas(self, fecha_desde, fecha_hasta):
        params = {
            "after": f"{fecha_desde}T00:00:00",
            "before": f"{fecha_hasta}T23:59:59",
            "per_page": 100
        }
        return self.client.get("orders", params=params)
