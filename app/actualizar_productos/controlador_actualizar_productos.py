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
    Carga archivo (Excel/CSV), valida encabezado,
    actualiza productos en WooCommerce y exporta resultados.
    """

    HEADERS_VALIDOS = ["SKU", "PRECIO_VENTA"]

    # ==================================================
    def __init__(self):
        self.config = Configuracion()
        self._cliente = None
        self._productos_archivo = []
        self._simples = []
        self._variados = []

    # ==================================================
    def _inicializar_cliente(self):
        if self._cliente is None:
            url, ck, cs = self.config.obtener_credenciales()
            self._cliente = ClienteWooCommerce(url, ck, cs)

    # ==================================================
    def cargar_archivo(self, ruta):
        """
        Carga archivo Excel o CSV con validaciones.
        """
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

    # ==================================================
    def _leer_excel(self, ruta):
        try:
            wb = openpyxl.load_workbook(ruta)
            ws = wb.active
        except Exception:
            raise PyWooError("Archivo Inválido")

        encabezado = [str(c.value).strip().upper() for c in ws[1][:2]]

        if encabezado != self.HEADERS_VALIDOS:
            raise PyWooError("Encabezado Incorrecto")

        productos = []

        for fila in ws.iter_rows(min_row=2, values_only=True):
            sku, precio = fila[:2]

            if not sku or precio is None:
                continue

            productos.append({
                "sku": str(sku).strip(),
                "price": float(precio),
                "estado": "Sin Actualizar"
            })

        return productos

    # ==================================================
    def _leer_csv(self, ruta):
        try:
            with open(ruta, newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                encabezado = next(reader)
        except Exception:
            raise PyWooError("Archivo Inválido")

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

                if not sku or not precio:
                    continue

                productos.append({
                    "sku": str(sku).strip(),
                    "price": float(precio),
                    "estado": "Sin Actualizar"
                })

        return productos

    # ==================================================
    def actualizar_productos(self, callback_progreso=None):
        """
        Actualiza productos en WooCommerce.
        Devuelve (simples, variados) para la UI.
        """
        if not self._productos_archivo:
            raise PyWooError("No hay productos cargados")

        self._inicializar_cliente()

        productos_tienda = self._cliente.obtener_productos(per_page=100)

        mapa_productos = {
            p.get("sku"): p
            for p in productos_tienda
            if p.get("sku")
        }

        self._simples = []
        self._variados = []

        total = len(self._productos_archivo)

        for i, p in enumerate(self._productos_archivo, start=1):

            if callback_progreso:
                callback_progreso(i, total)

            sku = p["sku"]

            if sku not in mapa_productos:
                p["estado"] = "Sin Actualizar"
                continue

            producto_tienda = mapa_productos[sku]
            producto_id = producto_tienda.get("id")
            tipo = producto_tienda.get("type", "simple")

            # Actualizar en WooCommerce
            self._cliente.actualizar_producto(
                producto_id=producto_id,
                data={
                    "regular_price": str(p["price"]),
                    "manage_stock": True
                }
            )

            p["estado"] = "Actualizado"

            fila = {
                "SKU": sku,
                "NOMBRE DEL PRODUCTO": producto_tienda.get("name", ""),
                "STOCK": producto_tienda.get("stock_quantity", ""),
                "PRECIO COMPRA": "",
                "PRECIO VENTA": p["price"],
                "ESTADO": p["estado"]
            }

            if tipo == "variable":
                self._variados.append(fila)
            else:
                self._simples.append(fila)

        return self._simples, self._variados

    # ==================================================
    def exportar_resultado(self, ruta):
        """
        Exporta el resultado final a Excel.
        """
        if not self._simples and not self._variados:
            raise PyWooError("No hay datos para exportar")

        wb = Workbook()
        ws = wb.active
        ws.title = "Resultado Actualización"

        headers = [
            "SKU",
            "NOMBRE DEL PRODUCTO",
            "STOCK",
            "PRECIO COMPRA",
            "PRECIO VENTA",
            "ESTADO"
        ]

        ws.append(headers)

        for grupo in (self._simples, self._variados):
            for p in grupo:
                ws.append([
                    p.get("SKU", ""),
                    p.get("NOMBRE DEL PRODUCTO", ""),
                    p.get("STOCK", ""),
                    p.get("PRECIO COMPRA", ""),
                    p.get("PRECIO VENTA", ""),
                    p.get("ESTADO", "")
                ])

        wb.save(ruta)
