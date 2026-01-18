# pywoo.py
import sys
from PySide6.QtWidgets import QApplication
from app.core.credenciales_view import VentanaCredenciales
from app.menu.ui.ui_view_menu import Ui_MainW_menu
from scripts.compilar_ui import compilar_ui


def main():
    compilar_ui()
    app = QApplication(sys.argv)

    cred = VentanaCredenciales()
    if cred.exec() == cred.Accepted:
        menu = Ui_MainW_menu()
        menu.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
