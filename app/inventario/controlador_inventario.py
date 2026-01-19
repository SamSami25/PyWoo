from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
from openpyxl import Workbook


class ControladorInventario:
    """
    Controlador del módulo Inventario.
    Gestiona obtención y exportación de productos.
    """

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._productos = []

    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    def obtener_productos(self, filtro="todos"):
        """
        filtro: todos | con_stock | sin_stock
        """
        self._inicializar_cliente()

        productos = self._cliente.obtener_productos(per_page=100)

        if filtro == "con_stock":
            productos = [p for p in productos if p.get("stock_quantity", 0) > 0]

        elif filtro == "sin_stock":
            productos = [p for p in productos if not p.get("stock_quantity")]

        self._productos = productos
        return productos

    def exportar_excel(self, ruta_archivo):
        if not self._productos:
            raise PyWooError("No hay productos para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Inventario"

        ws.append([
            "ID",
            "Producto",
            "SKU",
            "Stock",
            "Precio",
            "Estado"
        ])

        for p in self._productos:
            ws.append([
                p.get("id"),
                p.get("name"),
                p.get("sku"),
                p.get("stock_quantity"),
                p.get("price"),
                p.get("stock_status")
            ])

        wb.save(ruta_archivo)
