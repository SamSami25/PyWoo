from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
from openpyxl import Workbook


# ==========================================================
# FUNCIONES DE NEGOCIO
# ==========================================================
def validar_precio(precio) -> float:
    try:
        return round(float(precio), 4)
    except Exception:
        return 0.0


def por_descuento(ganancia: float) -> float:
    """
    Regla de negocio para descuento en función de la ganancia (0..1)
    """
    if ganancia <= 0.1:
        return 0.0
    elif ganancia <= 0.6:
        return round(0.4 * ganancia - 0.04, 4)
    return 0.20


def calc_ganancia(precio_compra: float, pvp: float) -> float:
    if pvp <= 0:
        return 0.0
    try:
        return round(1.0 - (precio_compra / pvp), 4)
    except Exception:
        return 0.0


def observacion(descuento_monto: float, stock: int) -> str:
    if descuento_monto >= 10 and stock > 1:
        return "COMPRA MÍNIMA 2 UNIDADES"
    return ""


# ==========================================================
# CONTROLADOR
# ==========================================================
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
        Obtiene productos desde WooCommerce y los separa en simples y variables,
        aplicando reglas de negocio.
        """
        self._inicializar_cliente()

        productos = self._cliente.obtener_productos(per_page=100)
        if not productos:
            raise PyWooError("No se encontraron productos")

        self._simples = []
        self._variados = []

        total = len(productos)

        for i, p in enumerate(productos, start=1):

            if callback_progreso:
                callback_progreso(i, total)

            sku = p.get("sku") or ""
            stock = int(p.get("stock_quantity") or 0)

            pvp = validar_precio(p.get("price"))
            precio_compra = validar_precio(p.get("regular_price"))

            ganancia = calc_ganancia(precio_compra, pvp)
            descuento_pct = por_descuento(ganancia)
            descuento_monto = round(pvp * descuento_pct, 4)
            pvd = round(pvp - descuento_monto, 4)

            fila = {
                "SKU": sku,
                "NOMBRE DEL PRODUCTO": p.get("name", ""),
                "VARIACIÓN": p.get("type", "simple"),
                "STOCK": stock,
                "PVP": pvp,
                "PRECIO DE COMPRA": precio_compra,
                "GANANCIA": ganancia,
                "DESCUENTO (%)": descuento_pct,
                "PRECIO DE DESCUENTO ($)": descuento_monto,
                "PVD": pvd,
                "OBSERVACIÓN": observacion(descuento_monto, stock),
                "URL": p.get("permalink", ""),
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
