from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtUiTools import QUiLoader
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("ui/mainwindow.ui", None)
        self.ui.show()
        
        self.file1PushButton = self.ui.file1PushButton
        self.file2PushButton = self.ui.file2PushButton

    def _open_file_dialog(self, line_edit):
        filename = QFileDialog.getOpenFileName(self, tr("Open File"), "~", tr(""))

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())