from datetime import datetime
from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
from openpyxl import Workbook


class ControladorReporteVentas:
    """
    Controlador del módulo Reporte de Ventas.
    Encapsula lógica de obtención y exportación de ventas.
    """

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._ventas = []

    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    def obtener_ventas(self, fecha_desde, fecha_hasta):
        """
        Obtiene ventas entre dos fechas.
        """
        self._inicializar_cliente()

        ventas = self._cliente.obtener_ordenes(per_page=100)

        # Filtrado por fechas (Woo devuelve ISO 8601)
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
            "ID Pedido",
            "Cliente",
            "Email",
            "Total",
            "Fecha"
        ])

        for v in self._ventas:
            ws.append([
                v.get("id"),
                f"{v['billing']['first_name']} {v['billing']['last_name']}",
                v["billing"]["email"],
                v["total"],
                v["date_created"]
            ])

        wb.save(ruta_archivo)
