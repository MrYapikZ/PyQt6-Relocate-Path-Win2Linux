from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox, QAbstractItemView

from app.ui.relocate_widget_ui import Ui_Form


class RelocateHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)