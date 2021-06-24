from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtUiTools import QUiLoader
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.ui = loader.load("ui/mainwindow.ui", None)
        self.ui.show()

        file1PushButton = self.ui.file1PushButton
        file2PushButton = self.ui.file2PushButton

        file1LineEdit = self.ui.file1LineEdit
        file2LineEdit = self.ui.file2LineEdit

        file1PushButton.clicked.connect(lambda: self._open_file_dialog(file1LineEdit))
        file2PushButton.clicked.connect(lambda: self._open_file_dialog(file2LineEdit))

    def _open_file_dialog(self, line_edit):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "Data (*.csv *.tsv *.txt *.xlsx)")[0]
        line_edit.setText(filename)

    def run_csvlink(self):
        from . import csvhelpers
        import dedupe

        data_1 = csvhelpers.readData(self.filename1, self.field_names_1,
                                    delimiter=",",
                                    prefix='input_1')
        data_2 = csvhelpers.readData(self.filename2, self.field_names_2,
                                    delimiter=",",
                                    prefix='input_2')



if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())

