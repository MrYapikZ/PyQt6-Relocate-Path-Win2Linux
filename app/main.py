import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

from app.ui.main_widget_ui import Ui_MainWindow
from app.modules.main.handle_relocate import RelocateHandler


class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Relocate Path Win2Linux")
        self.ui.label_version.setText("v0.1.0")

        self.ui.tabWidget_main.addTab(RelocateHandler(), "Relocate")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainUI()
    main.show()
    sys.exit(app.exec())

# pyinstaller --clean --noconsole --onefile -n RelocatePathW2L -p . --collect-submodules app app/main.py
