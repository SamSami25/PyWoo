from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError
import openpyxl


class ControladorActualizarProductos:
    """
    Controlador del módulo Actualizar Productos.
    Permite exportar plantilla, cargar archivo y actualizar productos.
    """

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._productos_archivo = []

    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # ---------------------------------------------------
    def exportar_plantilla(self, ruta):
        """
        Exporta una plantilla Excel editable.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Actualizar Productos"

        ws.append([
            "ID",
            "SKU",
            "Nombre",
            "Precio",
            "Stock"
        ])

        wb.save(ruta)

    # ---------------------------------------------------
    def cargar_archivo(self, ruta_archivo):
        """
        Lee archivo Excel con datos de productos.
        """
        try:
            wb = openpyxl.load_workbook(ruta_archivo)
            ws = wb.active
        except Exception:
            raise PyWooError("Archivo Excel inválido")

        productos = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row[0]:
                continue

            productos.append({
                "id": int(row[0]),
                "sku": row[1],
                "name": row[2],
                "price": row[3],
                "stock_quantity": row[4]
            })

        if not productos:
            raise PyWooError("El archivo no contiene productos válidos")

        self._productos_archivo = productos
        return productos

    # ---------------------------------------------------
    def actualizar_productos(self):
        """
        Actualiza productos en WooCommerce.
        """
        if not self._productos_archivo:
            raise PyWooError("No hay productos cargados")

        self._inicializar_cliente()

        for p in self._productos_archivo:
            self._cliente.actualizar_producto(
                producto_id=p["id"],
                data={
                    "regular_price": str(p["price"]),
                    "stock_quantity": p["stock_quantity"],
                    "manage_stock": True
                }
            )
