import sys
import iconos_rc

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from app.menu.menu_view import MenuPrincipalView


def aplicar_tema_claro(app: QApplication):

    app.setStyle("Fusion")

    pal = QPalette()

    pal.setColor(QPalette.Window, QColor(245, 247, 250))
    pal.setColor(QPalette.WindowText, Qt.black)

    pal.setColor(QPalette.Base, Qt.white)
    pal.setColor(QPalette.AlternateBase, QColor(240, 244, 248))
    pal.setColor(QPalette.Text, Qt.black)

    pal.setColor(QPalette.Button, QColor(235, 239, 243))
    pal.setColor(QPalette.ButtonText, Qt.black)

    pal.setColor(QPalette.ToolTipBase, Qt.white)
    pal.setColor(QPalette.ToolTipText, Qt.black)

    pal.setColor(QPalette.Highlight, QColor(30, 120, 230))
    pal.setColor(QPalette.HighlightedText, Qt.white)

    pal.setColor(QPalette.Link, QColor(30, 120, 230))
    pal.setColor(QPalette.BrightText, Qt.red)

    app.setPalette(pal)

    app.setStyleSheet("""
        QWidget {
            background: #F5F7FA;
            color: #111;
        }

        QFrame, QGroupBox {
            background: #F5F7FA;
        }

        QLineEdit, QPlainTextEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit {
            background: #FFFFFF;
            color: #111;
            border: 1px solid #D0D7DE;
            border-radius: 6px;
            padding: 4px 6px;
        }

        QPushButton {
            background: #1E78E6;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 6px 14px;
            font-weight: 600;
        }
        QPushButton:disabled {
            background: #A9C7F4;
            color: #F3F6FB;
        }

        QTableView {
            background: #FFFFFF;
            alternate-background-color: #F0F4F8;
            gridline-color: #D0D7DE;
            selection-background-color: #1E78E6;
            selection-color: white;
        }

        QHeaderView::section {
            background: #E9EEF5;
            color: #111;
            padding: 6px;
            border: 1px solid #D0D7DE;
            font-weight: bold;
        }

        QTabWidget::pane {
            background: #FFFFFF;
            border: 1px solid #D0D7DE;
        }
        QTabBar::tab {
            background: #E9EEF5;
            color: #111;
            padding: 8px 12px;
            border: 1px solid #D0D7DE;
            border-bottom: none;
        }
        QTabBar::tab:selected {
            background: #FFFFFF;
        }

        QMenuBar {
            background: #FFFFFF;
            color: #111;
        }
        QMenuBar::item:selected {
            background: #E9EEF5;
        }

        QMenu {
            background: #FFFFFF;
            color: #111;
            border: 1px solid #D0D7DE;
        }
        QMenu::item:selected {
            background: #E9EEF5;
        }

        QScrollBar:vertical {
            background: #F5F7FA;
            width: 12px;
            margin: 0px;
        }
        QScrollBar::handle:vertical {
            background: #C9D4E5;
            min-height: 20px;
            border-radius: 6px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)


def main():
    app = QApplication(sys.argv)

    aplicar_tema_claro(app)

    ventana = MenuPrincipalView()
    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
