from app.core.cliente_woocommerce import WooCommerceClient


class InventarioController:
    def __init__(self):
        self.client = WooCommerceClient()

    def obtener_todos(self):
        return self.client.get("products")

    def obtener_con_stock(self):
        productos = self.client.get("products")
        return [p for p in productos if p.get("stock_quantity", 0) > 0]

    def obtener_sin_stock(self):
        productos = self.client.get("products")
        return [p for p in productos if p.get("stock_quantity", 0) == 0]

    def exportar_inventario(self):
        productos = self.obtener_todos()
        # Aquí luego va Excel / CSV
        print(f"Exportando {len(productos)} productos")
