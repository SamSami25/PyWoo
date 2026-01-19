import sys
from PySide6.QtWidgets import QApplication, QDialog

from app.core.credenciales_view import VentanaCredenciales
from app.menu.menu_view import MenuPrincipal
from scripts.compilar_ui import compilar_ui


def main():
    compilar_ui()
    app = QApplication(sys.argv)

    dialogo = VentanaCredenciales()

    if dialogo.exec() == QDialog.Accepted:
        menu = MenuPrincipal()
        menu.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
