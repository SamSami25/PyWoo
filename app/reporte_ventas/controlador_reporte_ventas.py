# app/reporte_ventas/controlador_reporte_ventas.py
from __future__ import annotations

from typing import Callable, Optional, Any
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce


HEADERS = [
    "Fecha", "Cliente", "Subtotal", "Envío", "IVA", "Descuento", "Total",
    "Utilidad", "Estado", "Notas", "Pedido", "Identificación",
    "Correo", "Teléfono", "Dirección", "Ciudad", "Cajero"
]

COLUMN_KEYS = [
    "fecha", "cliente", "subtotal", "envio", "iva", "descuento", "total",
    "utilidad", "estado", "notas", "pedido", "identificacion",
    "correo", "telefono", "direccion", "ciudad", "cajero",
]


def _safe_str(x) -> str:
    return "" if x is None else str(x)


def _to_decimal(x: Any) -> Decimal:
    if x is None or x == "":
        return Decimal("0")
    try:
        return Decimal(str(x))
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _money_dec(x: Decimal) -> str:
    return str(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _safe_float(x) -> float:
    return float(_to_decimal(x))


def _estado_es(status: str) -> str:
    s = (status or "").strip().lower()
    mapa = {
        "pending": "Pendiente",
        "processing": "Procesando",
        "pos-open": "Pendiente",
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

    # ---------------- GENERAR ----------------
    def generar_reporte(
        self,
        desde,
        hasta,
        callback_progreso: Optional[Callable[[int, str], None]] = None,
        should_cancel: Optional[Callable[[], bool]] = None,
        **_kwargs,  # ✅ por si mañana pasas otro param, no revienta
    ):
        pedidos = self.cliente.obtener_pedidos(desde=desde, hasta=hasta)

        self._pedidos.clear()
        total = max(len(pedidos), 1)

        for i, o in enumerate(pedidos, start=1):
            if should_cancel and should_cancel():
                # ✅ cancelación controlada (silenciosa en UI)
                raise RuntimeError("__CANCELADO__")

            pedido_id = o.get("id", "")
            fecha = (o.get("date_created") or "").replace("T", " ")[:16]
            estado = _estado_es(o.get("status", ""))

            billing = o.get("billing") or {}
            shipping = o.get("shipping") or {}

            cliente = (billing.get("first_name", "") + " " + billing.get("last_name", "")).strip()
            if not cliente:
                cliente = billing.get("email", "") or ""

            correo = (billing.get("email") or "").strip()
            telefono = (billing.get("phone") or "").strip()

            # Valores (tu lógica actual)
            subtotal = _to_decimal("0")
            for li in (o.get("line_items") or []):
                subtotal += _to_decimal(li.get("subtotal"))

            envio = _to_decimal(o.get("shipping_total"))
            iva = _to_decimal(o.get("total_tax"))
            descuento = _to_decimal(o.get("discount_total"))
            total_orden = _to_decimal(o.get("total"))

            fila = {
                "fecha": fecha,
                "cliente": cliente,
                "subtotal": _money_dec(subtotal),
                "envio": _money_dec(envio),
                "iva": _money_dec(iva),
                "descuento": _money_dec(descuento),
                "total": _money_dec(total_orden),
                "utilidad": _money_dec(Decimal("0")),
                "estado": estado,
                "notas": (o.get("customer_note") or "").strip(),
                "pedido": pedido_id,
                "identificacion": "",
                "correo": correo,
                "telefono": telefono,
                "direccion": "",
                "ciudad": (shipping.get("city") or billing.get("city") or "").strip(),
                "cajero": "",
            }

            self._pedidos.append(fila)

            if callback_progreso:
                callback_progreso(
                    int((i / total) * 100),
                    f"Procesando pedido {i} de {total}"
                )

        modelo_principal = ModeloTablaReporteVentas(self._pedidos)
        modelo_vacio = ModeloTablaReporteVentas([])
        return modelo_principal, modelo_vacio

    # ---------------- EXPORTAR ----------------
    def exportar_excel(self, ruta: str):
        workbook = xlsxwriter.Workbook(ruta)

        header_fmt = workbook.add_format({
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "bg_color": "#D9EAF7",
        })
        money_fmt = workbook.add_format({"border": 1, "num_format": "#,##0.00"})
        text_fmt = workbook.add_format({"border": 1})

        ws = workbook.add_worksheet("Pedidos")

        for col, h in enumerate(HEADERS):
            ws.write(0, col, h, header_fmt)

        for r, fila in enumerate(self._pedidos, start=1):
            for c, key in enumerate(COLUMN_KEYS):
                val = fila.get(key, "")
                if key in ("subtotal", "envio", "iva", "descuento", "total", "utilidad"):
                    ws.write_number(r, c, _safe_float(val), money_fmt)
                else:
                    ws.write(r, c, val, text_fmt)

        ws.freeze_panes(1, 0)
        ws.autofilter(0, 0, max(1, len(self._pedidos)), len(HEADERS) - 1)

        workbook.close()
