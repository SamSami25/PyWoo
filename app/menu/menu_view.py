# app/menu/menu_view.py
from PySide6.QtWidgets import QWidget
from app.menu.ui.ui_view_menu import Ui_MainW_menu

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainW_menu()
        self.ui.setupUi(self)
