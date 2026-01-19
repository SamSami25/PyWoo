import sys
from PySide6.QtWidgets import QApplication
from app.core.credenciales_view import VentanaCredenciales
from app.menu.menu_view import MenuPrincipal
from scripts.compilar_ui import compilar_ui

def main():
    compilar_ui()
    app = QApplication(sys.argv)

    credenciales = VentanaCredenciales()

    if credenciales.exec() == VentanaCredenciales.Accepted:
        menu = MenuPrincipal()
        menu.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
