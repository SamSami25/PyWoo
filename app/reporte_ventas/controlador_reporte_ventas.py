from datetime import datetime
from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
from openpyxl import Workbook


class ControladorReporteVentas:
    """
    Controlador del módulo Reporte de Ventas.
    """

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._ventas = []

    # --------------------------------------------------
    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # --------------------------------------------------
    def obtener_ventas(self, fecha_desde, fecha_hasta):
        """
        Obtiene ventas entre dos fechas (inclusive).
        """
        self._inicializar_cliente()

        ventas = self._cliente.obtener_ordenes(per_page=100)

        if not ventas:
            raise PyWooError("No se encontraron ventas en la tienda")

        desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
        hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59
        )

        filtradas = []

        for v in ventas:
            fecha = datetime.fromisoformat(
                v["date_created"].replace("Z", "")
            )

            if desde <= fecha <= hasta:
                filtradas.append(v)

        if not filtradas:
            raise PyWooError(
                "No hay ventas en el rango de fechas seleccionado"
            )

        self._ventas = filtradas
        return filtradas

    # --------------------------------------------------
    def exportar_excel(self, ruta_archivo):
        """
        Exporta las ventas obtenidas a Excel.
        """
        if not self._ventas:
            raise PyWooError("No hay ventas para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte Ventas"

        ws.append([
            "FECHA",
            "CLIENTE",
            "SUBTOTAL",
            "ENVÍO",
            "IVA",
            "DESCUENTO",
            "TOTAL",
            "MÉTODO DE PAGO",
            "ESTADO",
            "PEDIDO",
            "CORREO",
            "TELÉFONO",
        ])

        for v in self._ventas:
            ws.append([
                v.get("date_created"),
                f"{v['billing']['first_name']} {v['billing']['last_name']}",
                v.get("subtotal"),
                v.get("shipping_total"),
                v.get("total_tax"),
                v.get("discount_total"),
                v.get("total"),
                v.get("payment_method_title"),
                v.get("status"),
                v.get("id"),
                v["billing"].get("email"),
                v["billing"].get("phone"),
            ])

        wb.save(ruta_archivo)
