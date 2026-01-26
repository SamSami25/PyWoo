from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
import sys


# ==============================
# TEMA CLARO
# ==============================
def aplicar_tema_claro(app):
    app.setStyle("Fusion")

    palette = app.palette()
    palette.setColor(QPalette.Window, QColor("#ffffff"))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor("#ffffff"))
    palette.setColor(QPalette.AlternateBase, QColor("#f2f2f2"))
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor("#f0f0f0"))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.Highlight, QColor("#1e73f1"))
    palette.setColor(QPalette.HighlightedText, Qt.white)

    app.setPalette(palette)

    app.setStyleSheet("""
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }

        QMainWindow {
            background-color: #ffffff;
        }

        QMenuBar, QMenu {
            background-color: #f5f5f5;
            color: #000000;
        }

        QFrame, QGroupBox {
            background-color: #ffffff;
        }
    """)


# ==============================
# TEMA OSCURO
# ==============================
def aplicar_tema_oscuro(app):
    app.setStyle("Fusion")

    palette = app.palette()
    palette.setColor(QPalette.Window, QColor("#121212"))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor("#1e1e1e"))
    palette.setColor(QPalette.AlternateBase, QColor("#2a2a2a"))
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor("#2a2a2a"))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.Highlight, QColor("#1e73f1"))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    app.setPalette(palette)

    app.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: #ffffff;
        }

        QMainWindow {
            background-color: #121212;
        }

        QMenuBar, QMenu {
            background-color: #1e1e1e;
            color: #ffffff;
        }

        QFrame, QGroupBox {
            background-color: #1e1e1e;
        }
    """)


# ==============================
# TEMA SISTEMA
# ==============================
def aplicar_tema_sistema(app):
    """
    Aplica tema claro u oscuro según el sistema operativo.
    """
    if sys.platform.startswith("win"):
        palette = app.palette()
        color = palette.color(QPalette.Window)
        if color.lightness() < 128:
            aplicar_tema_oscuro(app)
        else:
            aplicar_tema_claro(app)
    else:
        aplicar_tema_claro(app)
