from __future__ import annotations

from typing import Callable, Optional, Any
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.column_utils import prune_empty_columns


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
    # Evita celdas vacías
    if x is None:
        return "N/A"
    s = str(x)
    return s if s.strip() else "N/A"


def _clamp_nonneg_dec(x: Decimal) -> Decimal:
    return x if x >= 0 else Decimal("0")


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


def _normalizar_doc(v: Any) -> str | None:
    """Devuelve cédula/RUC válida (solo dígitos 10 o 13). Evita hashes/alfanuméricos."""
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None

    s = re.sub(r"[\s\-]", "", s)  # quita espacios y guiones

    # Ecuador: cédula 10 / RUC 13
    if re.fullmatch(r"\d{10}|\d{13}", s):
        return s

    return None


class ModeloTablaReporteVentas(QAbstractTableModel):
    def __init__(self, datos: list[dict], headers: list[str], keys: list[str]):
        super().__init__()
        self._datos = datos
        self._headers = headers
        self._keys = keys

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(self._keys)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        fila = self._datos[index.row()]
        clave = self._keys[index.column()]

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
                if 0 <= section < len(self._headers):
                    return self._headers[section]
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
        self._headers = list(HEADERS)
        self._keys = list(COLUMN_KEYS)

    def _extraer_identificacion(self, o: dict) -> str | None:
        """
        Identificación real (cédula/RUC/DNI/VAT) desde billing/meta_data.
        *NO* usa 'tax' por contiene-texto (porque trae basura/hash).
        Solo acepta números 10 o 13 (EC).
        """
        billing = o.get("billing") or {}

        # Lista blanca billing
        allow_billing = {
            "identificacion", "identificación", "cedula", "cédula", "dni", "ruc",
            "tax_id", "vat", "nif", "billing_ruc", "billing_cedula",
        }

        for k in billing.keys():
            kk = str(k).strip().lower()
            if kk in allow_billing:
                doc = _normalizar_doc(billing.get(k))
                if doc:
                    return doc

        # Lista blanca meta_data
        allow_meta = {
            "identificacion", "identificación", "cedula", "cédula", "dni", "ruc",
            "tax_id", "vat_number", "billing_vat", "billing_ruc", "billing_cedula",
            "_billing_ruc", "_billing_cedula",
        }

        for md in (o.get("meta_data") or []):
            key = str(md.get("key") or "").strip().lower()
            if not key or key not in allow_meta:
                continue
            doc = _normalizar_doc(md.get("value"))
            if doc:
                return doc

        return None

    def _extraer_cajero(self, o: dict) -> str | None:
        for md in (o.get("meta_data") or []):
            key = str(md.get("key") or "").strip().lower()
            if any(t in key for t in ("cashier", "cajero", "pos", "seller", "vendedor")):
                v = md.get("value")
                if v is None:
                    continue
                s = str(v).strip()
                if s:
                    return s
        return None

    def generar_reporte(
        self,
        desde,
        hasta,
        callback_progreso: Optional[Callable[[int, str], None]] = None,
        should_cancel: Optional[Callable[[], bool]] = None,
        **_kwargs,
    ):
        pedidos = self.cliente.obtener_pedidos(desde=desde, hasta=hasta)

        self._pedidos.clear()
        total = max(len(pedidos), 1)

        for i, o in enumerate(pedidos, start=1):
            if should_cancel and should_cancel():
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

            direccion = " ".join(
                [
                    (shipping.get("address_1") or billing.get("address_1") or "").strip(),
                    (shipping.get("address_2") or billing.get("address_2") or "").strip(),
                ]
            ).strip()
            direccion = direccion or None

            identificacion = self._extraer_identificacion(o)
            cajero = self._extraer_cajero(o)

            subtotal = Decimal("0")
            for li in (o.get("line_items") or []):
                subtotal += _to_decimal(li.get("subtotal"))

            subtotal = _clamp_nonneg_dec(subtotal)
            envio = _clamp_nonneg_dec(_to_decimal(o.get("shipping_total")))
            iva = _clamp_nonneg_dec(_to_decimal(o.get("total_tax")))
            descuento = _clamp_nonneg_dec(_to_decimal(o.get("discount_total")))
            total_orden = _clamp_nonneg_dec(_to_decimal(o.get("total")))

            fila = {
                "fecha": fecha or "N/A",
                "cliente": cliente or "N/A",
                "subtotal": _money_dec(subtotal),
                "envio": _money_dec(envio),
                "iva": _money_dec(iva),
                "descuento": _money_dec(descuento),
                "total": _money_dec(total_orden),
                "utilidad": _money_dec(Decimal("0")),
                "estado": estado or "N/A",
                "notas": (o.get("customer_note") or "").strip() or None,
                "pedido": pedido_id or "N/A",
                "identificacion": identificacion,
                "correo": correo or None,
                "telefono": telefono or None,
                "direccion": direccion,
                "ciudad": (shipping.get("city") or billing.get("city") or "").strip() or None,
                "cajero": cajero,
            }

            self._pedidos.append(fila)

            if callback_progreso:
                callback_progreso(
                    int((i / total) * 100),
                    f"Procesando pedido {i} de {total}"
                )

        optional = {
            "identificacion",
            "correo",
            "telefono",
            "direccion",
            "ciudad",
            "cajero",
            "notas",
        }
        self._headers, self._keys = prune_empty_columns(self._pedidos, HEADERS, COLUMN_KEYS, optional)

        modelo_principal = ModeloTablaReporteVentas(self._pedidos, self._headers, self._keys)
        modelo_vacio = ModeloTablaReporteVentas([], self._headers, self._keys)
        return modelo_principal, modelo_vacio

    def exportar_excel(self, ruta: str, filas=None):
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

        for col, h in enumerate(self._headers):
            ws.write(0, col, h, header_fmt)

        datos = filas if filas is not None else self._pedidos

        for r, fila in enumerate(datos, start=1):
            for c, key in enumerate(self._keys):
                val = fila.get(key, "")
                if key in ("subtotal", "envio", "iva", "descuento", "total", "utilidad"):
                    ws.write_number(r, c, _safe_float(val), money_fmt)
                else:
                    ws.write(r, c, val, text_fmt)

        ws.freeze_panes(1, 0)
        ws.autofilter(0, 0, max(1, len(datos)), max(0, len(self._headers) - 1))

        workbook.close()
