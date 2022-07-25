from functools import partial
from PySide2.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QLabel, QPushButton



class FileDialog(QWidget):
    """description of class"""

    def __init__(self, parent=None):

        self.parent = parent
        QWidget.__init__(self)

        self.vbox = QVBoxLayout()

        number_of_datasets = 2
        self.gui_elements = []

        for i in range(number_of_datasets):
            dic = {
                "DataButton": QPushButton("Add data file #" + str(i+1)),
                "DataLabel":  QLabel("Select Data " + str(i+1)),
                "DataPath": "",
                "ControlButton": QPushButton("Add control data file #" + str(i+1)),
                "ControlLabel":  QLabel("Select Control " + str(i+1)),
                "ControlPath": ""
            }

            dic["DataButton"].clicked.connect(
                partial(self.SelectFile, i, "Data"))
            dic["ControlButton"].clicked.connect(
                partial(self.SelectFile, i, "Control"))

            hbox = QHBoxLayout()

            hbox.addWidget(dic["DataButton"])
            hbox.addWidget(dic["DataLabel"])
            hbox.addWidget(dic["ControlButton"])
            hbox.addWidget(dic["ControlLabel"])

            self.vbox.addLayout(hbox)
            self.gui_elements.append(dic)

        InputsHbox = QHBoxLayout()

        self.NameInput = QLineEdit("Dataset name")
        self.DescriptionInput = QLineEdit("Dataset description")

        InputsHbox.addWidget(self.NameInput)
        InputsHbox.addWidget(self.DescriptionInput)
        self.vbox.addLayout(InputsHbox)

        ButtonsHbox = QHBoxLayout()

        ClearButton = QPushButton("Clear")
        SaveButton = QPushButton("Save")
        CancelButton = QPushButton("Cancel")

        ClearButton.clicked.connect(self.ClearSelection)
        CancelButton.clicked.connect(self.CancelDialog)
        SaveButton.clicked.connect(self.Save)

        ButtonsHbox.addWidget(ClearButton)
        ButtonsHbox.addWidget(SaveButton)
        ButtonsHbox.addWidget(CancelButton)
        self.vbox.addLayout(ButtonsHbox)

        self.setLayout(self.vbox)

    def SelectFile(self, index, field_name):
        path, _type = QFileDialog.getOpenFileName(self, 'Select File')
        if field_name == "Data":

            self.gui_elements[index]["DataPath"] = path
            self.gui_elements[index]["DataLabel"].setText(path)
        else:
            self.gui_elements[index]["ControlPath"] = path
            self.gui_elements[index]["ControlLabel"].setText(path)

    def Save(self):
        answer = []
        for i in range(len(self.gui_elements)):
            dic = self.gui_elements[i]
            if dic["DataPath"] != "":
                answer.append((dic["DataPath"], dic["ControlPath"]))

        if len(answer) > 0:
            self.parent.AddNewFiles(
                answer, self.NameInput.text(), self.DescriptionInput.text())
            self.close()

    def CancelDialog(self):
        self.close()

    def ClearSelection(self):
        self.NameInput = ""
        self.DescriptionInput = ""
        for i in range(len(self.gui_elements)):
            dic = self.gui_elements[i]
            dic["DataLabel"].setText("")
            dic["DataPath"] = ""
            dic["ControlLabel"].setText("")
            dic["ControlPath"] = ""
