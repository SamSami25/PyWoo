from app.core.cliente_woocommerce import WooCommerceClient


class ActualizarProductosController:
    def __init__(self):
        self.client = WooCommerceClient()

    def obtener_productos(self):
        return self.client.get("products")

    def exportar_productos(self):
        productos = self.obtener_productos()
        # Aquí luego se implementa CSV / Excel
        print(f"Exportando {len(productos)} productos")
