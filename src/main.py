from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtUiTools import QUiLoader
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        ui = loader.load("ui/mainwindow.ui", None)
        
        file1PushButton = ui.file1PushButton


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()  

    # Start the event loop
    sys.exit(app.exec_())