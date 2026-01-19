from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
from openpyxl import Workbook


class ControladorListaDistribuidores:
    """
    Controlador del módulo Lista de Distribuidores.
    Genera información de productos para distribuidores y exporta a Excel.
    """

    # ==============================
    # ENCABEZADOS
    # ==============================
    HEADERS_TABLA = [
        "SKU",
        "NOMBRE DEL PRODUCTO",
        "VARIACIÓN",
        "STOCK",
        "PVP",
        "PRECIO DE COMPRA",
        "GANANCIA",
        "DESCUENTO (%)",
        "PRECIO DE DESCUENTO ($)",
        "PVD",
        "OBSERVACIÓN",
        "URL",
    ]

    HEADERS_EXCEL = [
        "SKU",
        "NOMBRE DEL PRODUCTO",
        "VARIACIÓN",
        "STOCK",
        "PVP",
        "DESCUENTO (%)",
        "PRECIO DE DESCUENTO ($)",
        "PVD",
        "OBSERVACIÓN",
        "URL",
    ]

    # ==============================
    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._simples = []
        self._variados = []

    # ==============================
    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # ==============================
    def generar_lista(self, callback_progreso=None):
        """
        Obtiene productos desde WooCommerce y los separa en simples y variados.
        """
        self._inicializar_cliente()

        productos = self._cliente.obtener_productos(per_page=100)

        if not productos:
            raise PyWooError("No se encontraron productos")

        self._simples = []
        self._variados = []

        total = len(productos)

        for i, p in enumerate(productos, start=1):

            # Progreso
            if callback_progreso:
                callback_progreso(i, total)

            sku = p.get("sku") or ""
            stock = p.get("stock_quantity") or 0
            precio = float(p.get("price") or 0)
            url = p.get("permalink") or ""

            fila = {
                "SKU": sku,
                "NOMBRE DEL PRODUCTO": p.get("name", ""),
                "VARIACIÓN": p.get("type", "simple"),
                "STOCK": stock,
                "PVP": precio,
                "PRECIO DE COMPRA": "",
                "GANANCIA": "",
                "DESCUENTO (%)": "",
                "PRECIO DE DESCUENTO ($)": "",
                "PVD": "",
                "OBSERVACIÓN": "",
                "URL": url,
            }

            if p.get("type") == "variable":
                self._variados.append(fila)
            else:
                self._simples.append(fila)

        return self._simples, self._variados

    # ==============================
    def exportar_excel(self, ruta_archivo):
        """
        Exporta la lista de distribuidores a Excel con encabezado reducido.
        """
        if not self._simples and not self._variados:
            raise PyWooError("No hay datos para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Distribuidores"

        # Encabezado
        ws.append(self.HEADERS_EXCEL)

        for grupo in (self._simples, self._variados):
            for fila in grupo:
                ws.append([
                    fila.get("SKU", ""),
                    fila.get("NOMBRE DEL PRODUCTO", ""),
                    fila.get("VARIACIÓN", ""),
                    fila.get("STOCK", ""),
                    fila.get("PVP", ""),
                    fila.get("DESCUENTO (%)", ""),
                    fila.get("PRECIO DE DESCUENTO ($)", ""),
                    fila.get("PVD", ""),
                    fila.get("OBSERVACIÓN", ""),
                    fila.get("URL", ""),
                ])

        wb.save(ruta_archivo)
