from app.core.cliente_woocommerce import WooCommerceClient


class DistribuidoresController:
    def __init__(self):
        self.client = WooCommerceClient()

    def obtener_distribuidores(self):
        # En WooCommerce, distribuidores suelen mapearse a customers
        return self.client.get("customers")

    def exportar_distribuidores(self):
        distribuidores = self.obtener_distribuidores()
        # Aquí luego se implementa CSV / Excel
        print(f"Exportando {len(distribuidores)} distribuidores")
