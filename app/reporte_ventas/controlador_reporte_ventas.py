from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font

from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError


class ControladorReporteVentas:
    """
    Controlador del módulo Reporte de Ventas.
    Gestiona obtención, filtrado y exportación de ventas.
    """

    HEADERS = [
        "FECHA", "CLIENTE", "SUBTOTAL", "ENVÍO", "IVA", "DESCUENTO", "TOTAL",
        "MÉTODO DE PAGO", "UTILIDAD", "ESTADO", "NOTAS", "PEDIDO",
        "IDENTIFICACIÓN", "CORREO", "TELÉFONO", "DIRECCIÓN", "CIUDAD", "CAJERO"
    ]

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._ventas = []

    # ---------------------------------------------------------
    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # ---------------------------------------------------------
    def obtener_ventas(self, fecha_desde, fecha_hasta):
        """
        Obtiene ventas entre dos fechas (YYYY-MM-DD).
        """
        self._inicializar_cliente()

        try:
            ventas = self._cliente.obtener_ordenes(per_page=100)
        except Exception as e:
            raise PyWooError(f"Error al obtener ventas: {e}")

        desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
        hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d")

        filtradas = []

        for v in ventas:
            fecha = datetime.fromisoformat(
                v["date_created"].replace("Z", "")
            )

            if desde <= fecha <= hasta:
                filtradas.append(v)

        self._ventas = filtradas
        return filtradas

    # ---------------------------------------------------------
    def exportar_excel(self, ruta_archivo):
        """
        Exporta las ventas obtenidas a un archivo Excel.
        """
        if not self._ventas:
            raise PyWooError("No hay ventas para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte Ventas"

        # Encabezados
        ws.append(self.HEADERS)
        for col in range(1, len(self.HEADERS) + 1):
            ws.cell(row=1, column=col).font = Font(bold=True)

        # Filas
        for v in self._ventas:
            ws.append([
                v.get("date_created", ""),
                f"{v['billing']['first_name']} {v['billing']['last_name']}",
                v.get("subtotal", ""),
                v.get("shipping_total", ""),
                v.get("total_tax", ""),
                v.get("discount_total", ""),
                v.get("total", ""),
                v.get("payment_method_title", ""),
                "",  # UTILIDAD
                v.get("status", ""),
                v.get("customer_note", ""),
                v.get("id", ""),
                v["billing"].get("company", ""),
                v["billing"].get("email", ""),
                v["billing"].get("phone", ""),
                v["billing"].get("address_1", ""),
                v["billing"].get("city", ""),
                ""   # CAJERO
            ])

        wb.save(ruta_archivo)
