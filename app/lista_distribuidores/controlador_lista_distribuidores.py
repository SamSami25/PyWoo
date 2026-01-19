from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
from openpyxl import Workbook


class ControladorListaDistribuidores:
    """
    Controlador del módulo Lista de Distribuidores.
    Obtiene clientes WooCommerce y exporta a Excel.
    """

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._distribuidores = []

    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # --------------------------------------------------
    def generar_lista(self):
        """
        Obtiene distribuidores (clientes) desde WooCommerce.
        """
        self._inicializar_cliente()

        clientes = self._cliente.obtener_clientes(per_page=100)

        if not clientes:
            raise PyWooError("No se encontraron distribuidores")

        self._distribuidores = clientes
        return clientes

    # --------------------------------------------------
    def exportar_excel(self, ruta_archivo):
        """
        Exporta la lista de distribuidores a Excel.
        """
        if not self._distribuidores:
            raise PyWooError("No hay distribuidores para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Distribuidores"

        ws.append([
            "ID",
            "Nombre",
            "Email",
            "Empresa",
            "Teléfono",
            "País"
        ])

        for c in self._distribuidores:
            ws.append([
                c.get("id"),
                f"{c['first_name']} {c['last_name']}",
                c.get("email"),
                c.get("billing", {}).get("company"),
                c.get("billing", {}).get("phone"),
                c.get("billing", {}).get("country")
            ])

        wb.save(ruta_archivo)
