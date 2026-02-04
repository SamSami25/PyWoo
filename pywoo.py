import sys
import iconos_rc

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from app.menu.menu_view import MenuPrincipalView


def main():
    app = QApplication(sys.argv)

    ventana = MenuPrincipalView()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
