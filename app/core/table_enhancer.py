from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Iterable, Sequence
import re
from datetime import datetime

from PySide6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression, QModelIndex
from PySide6.QtWidgets import QTableView, QHeaderView


def _as_decimal(x) -> Decimal:
    """Convierte a Decimal.
    """
    if x is None:
        return Decimal("0")
    s = str(x).strip()
    if not s:
        return Decimal("0")
    s = s.replace(",", ".")
    # Quita símbolos comunes (moneda / espacios)
    s = re.sub(r"[^0-9.\-]", "", s)
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return Decimal("0")


class MultiColumnSortFilterProxy(QSortFilterProxyModel):
    """Proxy con:
    - Filtro por múltiples columnas (ej. SKU + NOMBRE)
    - Ordenamiento que intenta comparar números como números
    """

    def __init__(self, search_columns: Sequence[int] = (0, 1), parent=None):
        super().__init__(parent)
        self._search_columns = tuple(search_columns)
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)
        self.setSortRole(Qt.DisplayRole)

    def set_search_columns(self, cols: Sequence[int]) -> None:
        self._search_columns = tuple(cols)
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        rx = self.filterRegularExpression()
        if not rx or not rx.pattern():
            return True

        model = self.sourceModel()
        if model is None:
            return True

        for col in self._search_columns:
            idx = model.index(source_row, col, source_parent)
            text = str(idx.data(Qt.DisplayRole) or "")
            if rx.match(text).hasMatch():
                return True
        return False

    def _try_parse_datetime(self, s: str):
        """Intenta parsear fechas comunes (Woo: YYYY-MM-DD HH:MM)."""
        s = (s or "").strip()
        if not s:
            return None

        m = re.match(r"^(\d{4}-\d{2}-\d{2})(?:\s+(\d{2}:\d{2})(?::(\d{2}))?)?", s)
        if not m:
            return None

        date_part = m.group(1)
        time_part = m.group(2) or "00:00"
        sec_part = m.group(3)
        fmt = "%Y-%m-%d %H:%M" if sec_part is None else "%Y-%m-%d %H:%M:%S"
        try:
            if sec_part is None:
                return datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
            return datetime.strptime(f"{date_part} {time_part}:{sec_part}", "%Y-%m-%d %H:%M:%S")
        except Exception:
            return None

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        l = left.data(Qt.DisplayRole)
        r = right.data(Qt.DisplayRole)

        ls = str(l or "").strip()
        rs = str(r or "").strip()

        # 1) Fechas primero
        ldtt = self._try_parse_datetime(ls)
        rdtt = self._try_parse_datetime(rs)
        if ldtt is not None and rdtt is not None:
            return ldtt < rdtt

        # 2) Numérico
        try:
            if ls and rs:
                if any(ch.isdigit() for ch in ls) and any(ch.isdigit() for ch in rs):
                    ld = _as_decimal(ls)
                    rd = _as_decimal(rs)
                    return ld < rd
        except Exception:
            pass

        # 3) Texto
        return ls.casefold() < rs.casefold()


@dataclass
class EnhancedTable:
    table: QTableView
    proxy: MultiColumnSortFilterProxy


class TableEnhancer:
    """Aplica sorting por encabezados + búsqueda con resaltado (selección azul)."""

    def __init__(
        self,
        tables: Iterable[QTableView],
        search_columns: Sequence[int] = (0, 1),
    ) -> None:
        self._items: list[EnhancedTable] = []
        for t in tables:
            proxy = MultiColumnSortFilterProxy(search_columns=search_columns, parent=t)
            self._items.append(EnhancedTable(table=t, proxy=proxy))

            t.setSortingEnabled(True)
            t.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
            t.setSelectionMode(QTableView.SelectionMode.SingleSelection)
            hdr = t.horizontalHeader()
            hdr.setSectionsClickable(True)
            hdr.setSortIndicatorShown(True)
            hdr.setSectionResizeMode(QHeaderView.Interactive)

            t.setStyleSheet(
                "QTableView::item:selected:!active {"
                " background: palette(highlight);"
                " color: palette(highlighted-text);"
                " }"
            )

    def set_models(self, models: Sequence) -> None:
        """Asigna modelos en el mismo orden en que se pasaron las tablas."""
        for it, m in zip(self._items, models):
            it.proxy.setSourceModel(m)
            it.table.setModel(it.proxy)

            it.table.setSortingEnabled(True)
            hdr = it.table.horizontalHeader()
            hdr.setSortIndicatorShown(True)
            hdr.setSectionsClickable(True)

            col = hdr.sortIndicatorSection() if hdr.sortIndicatorSection() >= 0 else 0
            order = hdr.sortIndicatorOrder()
            it.table.sortByColumn(col, order)

    def clear(self) -> None:
        for it in self._items:
            it.table.setModel(None)
            it.proxy.setSourceModel(None)

    def apply_search(self, table: QTableView, text: str) -> None:
        text = (text or "").strip()
        for it in self._items:
            if it.table is table:

                if not text:
                    it.proxy.setFilterRegularExpression(QRegularExpression(""))
                    it.table.clearSelection()
                    return

                pattern = re.escape(text)
                rx = QRegularExpression(pattern, QRegularExpression.CaseInsensitiveOption)
                it.proxy.setFilterRegularExpression(rx)

                if it.proxy.rowCount() > 0:
                    it.table.selectRow(0)
                    it.table.scrollTo(it.proxy.index(0, 0))
                else:
                    it.table.clearSelection()
                return
