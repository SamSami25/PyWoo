from openpyxl import Workbook
from openpyxl.styles import Font

from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError


class ControladorInventario:
    """
    Controlador del módulo Inventario.
    Gestiona obtención, filtrado y exportación de productos.
    """

    HEADERS = [
        "SKU",
        "NOMBRE DEL PRODUCTO",
        "CATEGORIA",
        "STOCK",
        "PRECIO",
        "ESTADO"
    ]

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._productos = []

    # --------------------------------------------------
    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # --------------------------------------------------
    def obtener_productos(self, filtro="todos"):
        """
        Obtiene productos desde WooCommerce.
        filtro: 'todos' | 'con_stock' | 'sin_stock'
        """
        self._inicializar_cliente()

        try:
            productos = self._cliente.obtener_productos(per_page=100)
        except Exception as e:
            raise PyWooError(f"Error al obtener productos: {e}")

        if filtro == "con_stock":
            productos = [
                p for p in productos
                if (p.get("stock_quantity") or 0) > 0
            ]

        elif filtro == "sin_stock":
            productos = [
                p for p in productos
                if not p.get("stock_quantity")
            ]

        self._productos = productos
        return productos

    # --------------------------------------------------
    def exportar_excel(self, ruta_archivo):
        """
        Exporta los productos cargados a Excel.
        """
        if not self._productos:
            raise PyWooError("No hay productos para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Inventario"

        # Encabezados
        ws.append(self.HEADERS)
        for col in range(1, len(self.HEADERS) + 1):
            ws.cell(row=1, column=col).font = Font(bold=True)

        # Datos
        for p in self._productos:
            categorias = ", ".join(
                c.get("name", "") for c in p.get("categories", [])
            )

            ws.append([
                p.get("sku", ""),
                p.get("name", ""),
                categorias,
                p.get("stock_quantity", 0),
                p.get("price", ""),
                p.get("stock_status", "")
            ])

        wb.save(ruta_archivo)
