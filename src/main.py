from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtUiTools import QUiLoader
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("ui/mainwindow.ui", None)
        self.ui.show()

        file1PushButton = ui.file1PushButton
        file2PushButton = ui.file2PushButton

        file1LineEdit = ui.file1LineEdit
        file2LineEdit = ui.file2LineEdit

    def _open_file_dialog(self, line_edit):
        filename = QFileDialog.getOpenFileName()



if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())

