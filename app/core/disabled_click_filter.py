from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import QObject, QEvent
from PySide6.QtWidgets import QMessageBox, QWidget


class DisabledClickFilter(QObject):
    """Muestra un mensaje cuando el usuario intenta hacer click en un botón deshabilitado."""

    def __init__(
        self,
        parent_widget: QWidget,
        reason_getter: Callable[[], Optional[str]],
        title: str = "Acción deshabilitada",
    ) -> None:
        super().__init__(parent_widget)
        self._parent_widget = parent_widget
        self._reason_getter = reason_getter
        self._title = title

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QEvent.MouseButtonPress:
            try:
                enabled = bool(obj.isEnabled())
            except Exception:
                enabled = True

            if not enabled:
                reason = (self._reason_getter() or "").strip()
                if not reason:
                    reason = "Esta acción está deshabilitada en este momento."

                QMessageBox.information(self._parent_widget, self._title, reason)
                return True

        return super().eventFilter(obj, event)
