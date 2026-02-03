# app/reporte_ventas/controlador_reporte_ventas.py
from __future__ import annotations

from typing import Callable, Optional, Any

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce


# ---------------------------
# Columnas del reporte
# ---------------------------
HEADERS = [
    "Fecha", "Cliente", "Subtotal", "Envío", "IVA", "Descuento", "Total",
    "Utilidad", "Estado", "Notas", "Pedido", "Identificación",
    "Correo", "Teléfono", "Dirección", "Ciudad", "Cajero"
]

COLUMN_KEYS = [
    "fecha",
    "cliente",
    "subtotal",
    "envio",
    "iva",
    "descuento",
    "total",
    "utilidad",
    "estado",
    "notas",
    "pedido",
    "identificacion",
    "correo",
    "telefono",
    "direccion",
    "ciudad",
    "cajero",
]


# ---------------------------
# Helpers
# ---------------------------
def _safe_str(x) -> str:
    return "" if x is None else str(x)


def _to_decimal(x: Any) -> Decimal:
    """Convierte a Decimal de forma segura.

    WooCommerce normalmente devuelve montos como strings. Usar Decimal evita
    errores típicos de float (por ejemplo, totales que difieren en 0.01).
    """
    if x is None or x == "":
        return Decimal("0")
    try:
        return Decimal(str(x))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _money_dec(x: Decimal) -> str:
    return str(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _safe_float(x) -> float:
    # Solo para xlsxwriter.write_number (requiere float)
    return float(_to_decimal(x))


def _money(x) -> str:
    return _money_dec(_to_decimal(x))


def _estado_es(status: str) -> str:
    s = (status or "").strip().lower()
    mapa = {
        "pending": "Pendiente",
        "processing": "Procesando",
        "on-hold": "En espera",
        "completed": "Completado",
        "cancelled": "Cancelado",
        "refunded": "Reembolsado",
        "failed": "Fallido",
        "checkout-draft": "Borrador",
        "trash": "Eliminado",
    }
    return mapa.get(s, status or "")


class ModeloTablaReporteVentas(QAbstractTableModel):
    def __init__(self, datos: list[dict]):
        super().__init__()
        self._datos = datos

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(COLUMN_KEYS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        fila = self._datos[index.row()]
        clave = COLUMN_KEYS[index.column()]

        if role == Qt.DisplayRole:
            return _safe_str(fila.get(clave, ""))

        if role == Qt.TextAlignmentRole:
            # números a la derecha, texto centrado
            if clave in ("subtotal", "envio", "iva", "descuento", "total", "utilidad"):
                return int(Qt.AlignVCenter | Qt.AlignRight)
            return int(Qt.AlignCenter)

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if 0 <= section < len(HEADERS):
                    return HEADERS[section]
            if role == Qt.FontRole:
                f = QFont()
                f.setBold(True)
                return f
            if role == Qt.TextAlignmentRole:
                return int(Qt.AlignCenter)
        return None


class ControladorReporteVentas:
    def __init__(self):
        self.cliente = ClienteWooCommerce()
        self._pedidos: list[dict] = []

    @property
    def pedidos(self):
        return self._pedidos

    # ---------------- Helpers Woo ----------------
    def _armar_direccion(self, billing: dict) -> str:
        parts = [billing.get("address_1") or "", billing.get("address_2") or ""]
        return " ".join([p.strip() for p in parts if p.strip()]).strip()

    def _obtener_ciudad(self, billing: dict, shipping: dict) -> str:
        return (shipping.get("city") or billing.get("city") or "").strip()

    def _obtener_notas(self, order: dict) -> str:
        return (order.get("customer_note") or "").strip()

    def _obtener_descuento(self, order: dict) -> Decimal:
        return _to_decimal(order.get("discount_total"))

    def _obtener_envio(self, order: dict) -> Decimal:
        return _to_decimal(order.get("shipping_total"))

    def _obtener_total(self, order: dict) -> Decimal:
        return _to_decimal(order.get("total"))

    def _obtener_iva(self, order: dict) -> Decimal:
        return _to_decimal(order.get("total_tax"))

    def _obtener_subtotal(self, order: dict) -> Decimal:
        """Subtotal sin impuestos.

        Preferimos line_items.subtotal (antes de descuentos por cupón).
        Si por alguna razón no viene, usamos un fallback consistente.
        """
        line_items = order.get("line_items") or []
        subtotal = Decimal("0")
        for li in line_items:
            subtotal += _to_decimal(li.get("subtotal"))
        if subtotal > 0:
            return subtotal

        # fallback: total - shipping - tax + discount
        total = self._obtener_total(order)
        shipping = self._obtener_envio(order)
        tax = self._obtener_iva(order)
        discount = self._obtener_descuento(order)
        calc = total - shipping - tax + discount
        return max(calc, Decimal("0"))

    def _meta_value(self, order: dict, *keys: str) -> str:
        """Busca un valor en meta_data por varias posibles claves."""
        metas = order.get("meta_data") or []
        keys_norm = {k.strip().lower() for k in keys if k and k.strip()}
        for m in metas:
            k = str(m.get("key") or "").strip().lower()
            if k in keys_norm:
                v = m.get("value")
                return "" if v is None else str(v).strip()
        return ""

    def _obtener_identificacion(self, billing: dict, order: dict) -> str:
        """Intenta obtener Cédula/RUC/Identificación.

        Depende del plugin/campos de checkout. Probamos varias rutas comunes:
        - billing.*
        - meta_data (Checkout Field Editor, plugins locales, etc.)
        """
        # 1) Algunos plugins guardan directamente en billing
        for k in (
            "cedula",
            "ruc",
            "dni",
            "documento",
            "identificacion",
            "vat",
        ):
            v = (billing.get(k) or "").strip()
            if v:
                return v

        # 2) Meta_data: múltiples nombres típicos
        v = self._meta_value(
            order,
            "_billing_cedula",
            "billing_cedula",
            "cedula",
            "_billing_ruc",
            "billing_ruc",
            "ruc",
            "cedula_ruc",
            "_billing_documento",
            "billing_documento",
            "documento",
            "_billing_vat",
            "billing_vat",
            "vat",
        )
        if v:
            return v

        # 3) Último fallback: company (si lo usaban así antes)
        return (billing.get("company") or "").strip()

    def _obtener_cajero(self, order: dict) -> str:
        # No estándar: POS/administración podría guardar usuario en meta_data
        return self._meta_value(order, "cajero", "cashier", "pos_user", "_pos_user")

    # ---------------- GENERAR ----------------
    def generar_reporte(self, desde, hasta, callback_progreso: Optional[Callable[[int, str], None]] = None):
        # Enviamos date directamente; el cliente construye ISO8601 con zona
        pedidos = self.cliente.obtener_pedidos(desde=desde, hasta=hasta)

        self._pedidos.clear()
        total = max(len(pedidos), 1)

        for i, o in enumerate(pedidos, start=1):
            pedido_id = o.get("id", "")
            fecha = (o.get("date_created") or "").replace("T", " ")[:16]  # yyyy-mm-dd hh:mm
            estado = _estado_es(o.get("status", ""))

            billing = o.get("billing") or {}
            shipping = o.get("shipping") or {}

            cliente = (billing.get("first_name", "") + " " + billing.get("last_name", "")).strip()
            if not cliente:
                cliente = billing.get("email", "") or ""

            correo = (billing.get("email") or "").strip()
            telefono = (billing.get("phone") or "").strip()
            direccion = self._armar_direccion(billing)
            ciudad = self._obtener_ciudad(billing, shipping)

            subtotal = self._obtener_subtotal(o)
            envio = self._obtener_envio(o)
            iva = self._obtener_iva(o)
            descuento = self._obtener_descuento(o)
            total_orden = self._obtener_total(o)

            notas = self._obtener_notas(o)
            identificacion = self._obtener_identificacion(billing, o)
            cajero = self._obtener_cajero(o)

            # Utilidad: si todavía no tienes costos, mejor 0.00 (no inventa)
            utilidad_val = Decimal("0")

            fila = {
                "fecha": fecha,
                "cliente": cliente,
                "subtotal": _money_dec(subtotal),
                "envio": _money_dec(envio),
                "iva": _money_dec(iva),
                "descuento": _money_dec(descuento),
                "total": _money_dec(total_orden),
                "utilidad": _money_dec(utilidad_val),
                "estado": estado,
                "notas": notas,
                "pedido": pedido_id,
                "identificacion": identificacion,
                "correo": correo,
                "telefono": telefono,
                "direccion": direccion,
                "ciudad": ciudad,
                "cajero": cajero,
            }

            self._pedidos.append(fila)

            if callback_progreso:
                callback_progreso(
                    int((i / total) * 100),
                    f"Procesando pedido {i} de {total}"
                )

        # ✅ La UI tiene 2 tablas: devolvemos la misma en la primera y una vacía en la segunda.
        modelo_principal = ModeloTablaReporteVentas(self._pedidos)
        modelo_vacio = ModeloTablaReporteVentas([])
        return modelo_principal, modelo_vacio

    # ---------------- EXPORTAR ----------------
    def exportar_excel(self, ruta: str):
        workbook = xlsxwriter.Workbook(ruta)

        # Estilos
        header_fmt = workbook.add_format({
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "bg_color": "#D9EAF7",
        })
        money_fmt = workbook.add_format({"border": 1, "num_format": "#,##0.00"})
        text_fmt = workbook.add_format({"border": 1})
        totals_label_fmt = workbook.add_format({"bold": True, "border": 1})
        totals_money_fmt = workbook.add_format({"bold": True, "border": 1, "num_format": "#,##0.00"})

        ws = workbook.add_worksheet("Pedidos")

        # Header
        for col, h in enumerate(HEADERS):
            ws.write(0, col, h, header_fmt)

        # Column widths (ajuste básico)
        widths = {
            "fecha": 18,
            "cliente": 22,
            "subtotal": 12,
            "envio": 10,
            "iva": 10,
            "descuento": 12,
            "total": 12,
            "utilidad": 12,
            "estado": 14,
            "notas": 22,
            "pedido": 10,
            "identificacion": 16,
            "correo": 22,
            "telefono": 14,
            "direccion": 26,
            "ciudad": 14,
            "cajero": 14,
        }
        for col, key in enumerate(COLUMN_KEYS):
            ws.set_column(col, col, widths.get(key, 18))

        # Datos (sumamos con Decimal para evitar desfases por float)
        sum_sub_d = sum((_to_decimal(x.get("subtotal")) for x in self._pedidos), Decimal("0"))
        sum_env_d = sum((_to_decimal(x.get("envio")) for x in self._pedidos), Decimal("0"))
        sum_iva_d = sum((_to_decimal(x.get("iva")) for x in self._pedidos), Decimal("0"))
        sum_desc_d = sum((_to_decimal(x.get("descuento")) for x in self._pedidos), Decimal("0"))
        sum_total_d = sum((_to_decimal(x.get("total")) for x in self._pedidos), Decimal("0"))
        sum_util_d = sum((_to_decimal(x.get("utilidad")) for x in self._pedidos), Decimal("0"))

        for r, fila in enumerate(self._pedidos, start=1):
            for c, key in enumerate(COLUMN_KEYS):
                val = fila.get(key, "")
                if key in ("subtotal", "envio", "iva", "descuento", "total", "utilidad"):
                    ws.write_number(r, c, _safe_float(val), money_fmt)
                else:
                    ws.write(r, c, val, text_fmt)

        last_data_row = len(self._pedidos)

        # Autofiltro y freeze header
        ws.autofilter(0, 0, max(last_data_row, 1), len(HEADERS) - 1)
        ws.freeze_panes(1, 0)

        # Totales (fila debajo)
        totals_row = last_data_row + 1
        ws.write(totals_row, 0, "Totales", totals_label_fmt)

        # escribe totales en columnas específicas
        idx = {k: i for i, k in enumerate(COLUMN_KEYS)}
        ws.write_number(totals_row, idx["subtotal"], float(sum_sub_d), totals_money_fmt)
        ws.write_number(totals_row, idx["envio"], float(sum_env_d), totals_money_fmt)
        ws.write_number(totals_row, idx["iva"], float(sum_iva_d), totals_money_fmt)
        ws.write_number(totals_row, idx["descuento"], float(sum_desc_d), totals_money_fmt)
        ws.write_number(totals_row, idx["total"], float(sum_total_d), totals_money_fmt)
        ws.write_number(totals_row, idx["utilidad"], float(sum_util_d), totals_money_fmt)

        workbook.close()
