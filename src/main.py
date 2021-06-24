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
        
        #Move to the next tab (select columns)
        self.ui.loadPushButton.clicked.connect(lambda: self.gridStackedWidget.setCurrentIndex(1))
        self.ui.backPushButton.clicked.connect(lambda: self.gridStackedWidget.setCurrentIndex(0))
        
        #When continue is clicked
        self.ui.continuePushButton.clicked.connect(self.define_field_names)
        self.ui.continuePushButton.clicked.connect(lambda: self.gridStackedWidget.setCurrentIndex(2))
    
        # self.ui.file1SelectColumn1.currentTextChanged()
        # self.ui.file1SelectColumn2.currentTextChanged()
        # self.ui.file1SelectColumn3.currentTextChanged()

    def _open_file_dialog(self, line_edit):
        #Open the file
        filename = QFileDialog.getOpenFileName(self, "Open File", "", "Data (*.csv *.tsv *.txt *.xlsx)")[0]
        line_edit.setText(filename)

    def read_file(self,filename):
        return open(filename, encoding="utf-8").read()

    def run_csvlink(self):
        #Read the data
        self.data_1 = csvhelpers.readData(self.read_file(self.file1LineEdit.text()), "",
                                    delimiter=",",
                                    prefix=None)
        self.data_2 = csvhelpers.readData(self.read_file(self.file2LineEdit.text()), "",
                                    delimiter=",",
                                    prefix=None)

        self.select_columns()

    def select_columns(self):
        #Select column names 
        cols1 = list(list(self.data_1.values())[0].keys())
        cols1 = [_ for _ in cols1 if _ != "unique_id" ]
        cols2 = list(list(self.data_2.values())[0].keys())
        cols2 = [_ for _ in cols2 if _ != "unique_id" ]

        #Define boxes
        self.boxes1 = [self.ui.file1SelectColumn1,self.ui.file1SelectColumn2,self.ui.file1SelectColumn3]
        self.boxes2 = [self.ui.file2SelectColumn1,self.ui.file2SelectColumn2,self.ui.file2SelectColumn3]

        #Set up the options (columns)
        for box in self.boxes1:        
            box.addItems(cols1)
        for box in self.boxes2:        
            box.addItems(cols2)        

    def define_field_names(self):
        #Cols in data1
        self.field_names_1 = [_.currentText() for _ in self.boxes1 if _.currentText() != ""]
        self.field_names_2 = [_.currentText() for _ in self.boxes2 if _.currentText() != ""]
        
        #Remap columns if necesarry
        if self.field_names_1 != self.field_names_2:
            for record_id, record in self.data_2.items():
                remapped_record = {}
                for new_field, old_field in zip(self.field_names_1,
                                                self.field_names_2):
                    remapped_record[new_field] = record[old_field]
                self.data_2[record_id] = remapped_record

        
    
    def training(self):
        # Start up dedupe
        deduper = dedupe.RecordLink(self.field_definition)

        # Speed up by finding identical matches
        fields = {variable.field for variable in deduper.data_model.primary_fields}
        (nonexact_1,
            nonexact_2,
            exact_pairs) = self.exact_matches(data_1, data_2, fields)

        # Set up our data sample
        #TODO display logging.info('taking a sample of %d possible pairs', self.sample_size)
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

        #Save the file to the downloads folder (TODO: Ask where to save it)
        self.download_file(clustered_dupes)

    def download_file(self,clustered_dupes):
        #Select folder
        #Select filename

        write_function = csvhelpers.writeLinkedResults
        with open(self.output_file, 'w', encoding='utf-8') as output_file:
                    write_function(clustered_dupes, self.input_1, self.input_2,
                                   "~/Downloads/output_dedupe.csv", False)
      

    def exact_matches(data_1, data_2, match_fields):
        nonexact_1 = {}
        nonexact_2 = {}
        exact_pairs = []
        redundant = {}

        for key, record in data_1.items():
            record_hash = hash(tuple(record[f] for f in match_fields))
            redundant[record_hash] = key        

        for key_2, record in data_2.items():
            record_hash = hash(tuple(record[f] for f in match_fields))
            if record_hash in redundant:
                key_1 = redundant[record_hash]
                exact_pairs.append(((key_1, key_2), 1.0))
                del redundant[record_hash]
            else:
                nonexact_2[key_2] = record

        for key_1 in redundant.values():
            nonexact_1[key_1] = data_1[key_1]
            
        return nonexact_1, nonexact_2, exact_pairs


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()

    # Start the event loop
    sys.exit(app.exec())

