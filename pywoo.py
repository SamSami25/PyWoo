import sys
import os
import iconos_rc
from PySide6.QtWidgets import QApplication
from app.menu.menu_view import MenuPrincipalView
from app.core.temas import (aplicar_tema_claro, aplicar_tema_oscuro, aplicar_tema_sistema)

def main():
    app = QApplication(sys.argv)

    aplicar_tema_sistema(app)

    ventana = MenuPrincipalView()
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
