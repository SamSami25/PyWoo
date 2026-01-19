import os
import csv
import openpyxl
from openpyxl import Workbook

from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.excepciones import PyWooError


class ControladorActualizarProductos:
    """
    Controlador del módulo Actualizar Productos.
    """

    HEADERS_VALIDOS = ["SKU", "PRECIO_VENTA"]

    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._productos_archivo = []

    # --------------------------------------------------
    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # --------------------------------------------------
    def cargar_archivo(self, ruta):
        extension = os.path.splitext(ruta)[1].lower()

        if extension == ".xlsx":
            productos = self._leer_excel(ruta)
        elif extension == ".csv":
            productos = self._leer_csv(ruta)
        else:
            raise PyWooError("Vuelva a Cargar el Archivo")

        if not productos:
            raise PyWooError("El archivo no contiene datos válidos")

        self._productos_archivo = productos
        return productos

    # --------------------------------------------------
    def _leer_excel(self, ruta):
        try:
            wb = openpyxl.load_workbook(ruta)
            ws = wb.active
        except Exception:
            raise PyWooError("Archivo Excel inválido")

        encabezado = [str(c.value).strip().upper() for c in ws[1][:2]]

        if encabezado != self.HEADERS_VALIDOS:
            raise PyWooError("Encabezado Incorrecto")

        productos = []
        for fila in ws.iter_rows(min_row=2, values_only=True):
            sku, precio = fila[:2]

            if not sku or precio is None:
                continue

            productos.append({
                "sku": str(sku),
                "price": float(precio),
                "estado": "Sin Actualizar"
            })

        return productos

    # --------------------------------------------------
    def _leer_csv(self, ruta):
        try:
            with open(ruta, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                encabezado = next(reader)
        except Exception:
            raise PyWooError("Archivo CSV inválido")

        encabezado = [h.strip().upper() for h in encabezado[:2]]
        if encabezado != self.HEADERS_VALIDOS:
            raise PyWooError("Encabezado Incorrecto")

        productos = []
        with open(ruta, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)

            for row in reader:
                if len(row) < 2:
                    continue

                sku, precio = row[:2]
                productos.append({
                    "sku": sku,
                    "price": float(precio),
                    "estado": "Sin Actualizar"
                })

        return productos

    # --------------------------------------------------
    def actualizar_productos(self):
        if not self._productos_archivo:
            raise PyWooError("No hay productos cargados")

        self._inicializar_cliente()

        productos_tienda = self._cliente.obtener_productos(per_page=100)

        mapa_productos = {
            p.get("sku"): p.get("id")
            for p in productos_tienda
            if p.get("sku")
        }

        for p in self._productos_archivo:
            sku = p["sku"]
            if sku not in mapa_productos:
                p["estado"] = "Sin Actualizar"
                continue

            producto_id = mapa_productos[sku]

            self._cliente.actualizar_producto(
                producto_id=producto_id,
                data={
                    "regular_price": str(p["price"]),
                    "manage_stock": True
                }
            )

            p["estado"] = "Actualizado"

    # --------------------------------------------------
    def exportar_resultado(self, ruta):
        if not self._productos_archivo:
            raise PyWooError("No hay datos para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Resultado Actualización"

        headers = [
            "SKU", "PRECIO VENTA", "ESTADO"
        ]
        ws.append(headers)

        for p in self._productos_archivo:
            ws.append([
                p["sku"],
                p["price"],
                p["estado"]
            ])

        wb.save(ruta)
