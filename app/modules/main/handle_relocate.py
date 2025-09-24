from PyQt6.QtCore import QVariant, Qt
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox, QAbstractItemView, QListWidgetItem

from app.ui.relocate_widget_ui import Ui_Form
from app.services.file_manager import FileManager


class RelocateHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.root_path = None
        self._available_widget_order = []

        self.ui.toolButton_rootPath.clicked.connect(self.on_select_folder)
        self.ui.pushButton_folderListImport.clicked.connect(self.on_import_select)

        self.ui.listWidget_folderList.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.ui.listWidget_folderList.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.ui.listWidget_available.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.ui.listWidget_available.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.ui.listWidget_selected.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.ui.listWidget_selected.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.ui.pushButton_listControl_add.clicked.connect(self.on_move_available_item)
        self.ui.pushButton_listControl_remove.clicked.connect(self.on_move_selected_item)

        self.ui.pushButton_buttonScan.clicked.connect(self.on_scan_files)
        self.ui.pushButton_buttonClear.clicked.connect(self.on_clear)

        self._enable_drag_drop_lineedits()
        self._wire_search_available()
        self._wire_search_selected()

    def on_select_folder(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.ui.lineEdit_rootPath.setText(directory)

    def on_clear(self):
        self.ui.listWidget_selected.clear()
        self.ui.listWidget_available.clear()
        self.ui.listWidget_folderList.clear()
        self.ui.lineEdit_availableSearch.clear()
        self.ui.lineEdit_selectedSearch.clear()

    def on_scan_files(self):
        self.ui.listWidget_folderList.clear()
        self.root_path = self.ui.lineEdit_rootPath.text()

        if not self.root_path:
            QMessageBox.critical(self, "Error", "Root path not set")
            return

        list_folder = FileManager().get_folder_list(root_path=self.root_path)
        if list_folder:
            for folder in list_folder:
                self.ui.listWidget_folderList.addItem(folder)

    def on_import_select(self):
        self.ui.listWidget_available.clear()
        self.ui.lineEdit_availableSearch.clear()
        self._available_widget_order = []
        directory = self.ui.listWidget_folderList.selectedItems()
        if not directory:
            QMessageBox.warning(self, "Error", "Folder not selected")
            return

        for folder in directory:
            path = FileManager().combine_paths(self.root_path, folder.text())
            files = FileManager().get_file_by_ext(directory=path, ext=".blend",
                                                  latest=self.ui.checkBox_optionLatest.isChecked(),
                                                  recursive=self.ui.checkBox_optionRecursive.isChecked())
            if not files:
                QMessageBox.warning(self, "Error", "No files found")

            for file in files:
                item = QListWidgetItem(file.name)
                item.setData(Qt.ItemDataRole.UserRole, file)
                self.ui.listWidget_available.addItem(item)
                self._available_widget_order.append(file.name)

    def on_move_available_item(self):
        sel = self.ui.listWidget_available.selectedItems()
        for item in sel:
            self.ui.listWidget_selected.addItem(item.text())
            row = self.ui.listWidget_available.row(item)
            self.ui.listWidget_available.takeItem(row)

    def on_move_selected_item(self):
        sel = self.ui.listWidget_selected.selectedItems()
        for item in sel:
            text = item.text()
            insert_row = self._find_insert_row_for_label(text)
            self.ui.listWidget_available.insertItem(insert_row, text)
            row = self.ui.listWidget_selected.row(item)
            self.ui.listWidget_selected.takeItem(row)

    def _enable_drag_drop_lineedits(self):
        def enable_dragdrop(le, exts=None):
            if not le:
                return
            le.setAcceptDrops(True)

            def dragEnterEvent(event):
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                else:
                    event.ignore()

            def dropEvent(event):
                if event.mimeData().hasUrls():
                    file_path = event.mimeData().urls()[0].toLocalFile()
                    if exts:
                        for ext in exts:
                            if file_path.lower().endswith(ext):
                                le.setText(file_path)
                                event.acceptProposedAction()
                                return
                        event.ignore()
                    else:
                        le.setText(file_path)
                        event.acceptProposedAction()
                else:
                    event.ignore()

            le.dragEnterEvent = dragEnterEvent
            le.dropEvent = dropEvent

        enable_dragdrop(getattr(self.ui, "lineEdit_rootPath", None), [])

    def _available_order_index(self, label: str) -> int:
        try:
            return self._available_widget_order.index(label)
        except ValueError:
            return len(self._available_widget_order)

    def _find_insert_row_for_label(self, label: str) -> int:
        """Cari posisi penyisipan berdasarkan urutan awal"""
        target_idx = self._available_order_index(label)
        lw = self.ui.listWidget_available
        for row in range(lw.count()):
            other_label = lw.item(row).text()
            if self._available_order_index(other_label) > target_idx:
                return row
        return lw.count()

    def _wire_search_available(self):
        le = getattr(self.ui, "lineEdit_availableSearch", None)
        if le:
            le.textChanged.connect(self._filter_available_list)

    def _filter_available_list(self, text: str):
        lw = self.ui.listWidget_available
        text_low = (text or "").lower().strip()
        for i in range(lw.count()):
            item = lw.item(i)
            item.setHidden(text_low not in item.text().lower())

    def _wire_search_selected(self):
        le = getattr(self.ui, "lineEdit_selectedSearch", None)
        if le:
            le.textChanged.connect(self._filter_selected_list)

    def _filter_selected_list(self, text: str):
        lw = self.ui.listWidget_selected
        text_low = (text or "").lower().strip()
        for i in range(lw.count()):
            item = lw.item(i)
            item.setHidden(text_low not in item.text().lower())