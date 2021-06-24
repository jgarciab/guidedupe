from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtUiTools import QUiLoader
import sys

import csvhelpers
import dedupe
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Load UI created in QTDesign
        loader = QUiLoader()
        self.ui = loader.load("ui/mainwindow.ui", None)
        self.ui.show()

        self.gridStackedWidget = self.ui.gridStackedWidget

        #Define the two buttons to load the files
        self.file1PushButton = self.ui.file1PushButton
        self.file2PushButton = self.ui.file2PushButton

        #Boxes where the file path is displayed
        self.file1LineEdit = self.ui.file1LineEdit
        self.file2LineEdit = self.ui.file2LineEdit

        #Connect to the boxes to select the file
        self.file1PushButton.clicked.connect(lambda: self._open_file_dialog(self.file1LineEdit))
        self.file2PushButton.clicked.connect(lambda: self._open_file_dialog(self.file2LineEdit))

        #When the load data button is clicked, run run_csvlink
        self.ui.loadPushButton.clicked.connect(self.run_csvlink)
        self.ui.loadPushButton.clicked.connect(lambda: self.gridStackedWidget.setCurrentIndex(1))
        
        #Move to the next tab (select columns)

    def _open_file_dialog(self, line_edit):
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "Data (*.csv *.tsv *.txt *.xlsx)")[0]
        line_edit.setText(filename)

    def run_csvlink(self):
        #I believe the second field is not needed (fields_names)
        self.data_1 = csvhelpers.readData(self.file1LineEdit.text(), "",
                                    delimiter=",",
                                    prefix='input_1')
        self.data_2 = csvhelpers.readData(self.file2LineEdit.text(), "",
                                    delimiter=",",
                                    prefix='input_2')



    def select_columns(self):
        cols1 = list(self.data_1.values())[0]
        cols2 = list(self.data_2.values())[0]


        #Cols in data1
        #self.field_names_1
        
        #Cols in data2
        #self.field_names_2
        # if self.field_names_1 != self.field_names_2:
        #     for record_id, record in data_2.items():
        #         remapped_record = {}
        #         for new_field, old_field in zip(self.field_names_1,
        #                                         self.field_names_2):
        #             remapped_record[new_field] = record[old_field]
        #         data_2[record_id] = remapped_record

    #Move to the next tab (select columns)
    
    def training(self):
        deduper = dedupe.RecordLink(self.field_definition)

        fields = {variable.field for variable in deduper.data_model.primary_fields}
        (nonexact_1,
            nonexact_2,
            exact_pairs) = exact_matches(data_1, data_2, fields)

        # Set up our data sample
        logging.info('taking a sample of %d possible pairs', self.sample_size)
        deduper.sample(nonexact_1, nonexact_2, self.sample_size)

        # Perform standard training procedures
        self.dedupe_training(deduper)

        #TODO: Diplay "blocking"

        #TODO display logging.info('finding a good threshold with a recall_weight of %s' %
                    #  self.recall_weight)
        threshold = deduper.threshold(data_1, data_2,
                                      recall_weight=self.recall_weight)

        #TODO display logging.info('clustering...')
        clustered_dupes = deduper.match(data_1, data_2, threshold)

        clustered_dupes.extend(exact_pairs)

        #TODO display logging.info('# duplicate sets %s' % len(clustered_dupes))


    def download_file(self):
        #write_function = csvhelpers.writeLinkedResults
        # write out our results

        # if self.output_file:
        #     if sys.version < '3' :
        #         with open(self.output_file, 'wb', encoding='utf-8') as output_file:
        #             write_function(clustered_dupes, self.input_1, self.input_2,
        #                            output_file, self.inner_join)
        #     else :
        #         with open(self.output_file, 'w', encoding='utf-8') as output_file:
        #             write_function(clustered_dupes, self.input_1, self.input_2,
        #                            output_file, self.inner_join)
        # else:
        #     write_function(clustered_dupes, self.input_1, self.input_2,
        #                    sys.stdout, self.inner_join)
        pass     

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())

