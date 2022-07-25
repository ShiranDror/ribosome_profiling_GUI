from PySide2.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QSizePolicy, QLabel,
                              QLineEdit, QCheckBox, QRadioButton)
from PySide2.QtGui import QIntValidator

class PlotSettings(QHBoxLayout):
    """description of class"""
    def __init__(self, parent = None):
        QHBoxLayout.__init__(self)
        self.parent = parent

        self.BinWindow = QLineEdit("")
        self.BinWindow.setPlaceholderText("Average window")
        self.onlyInt = QIntValidator()
        self.BinWindow.setValidator(self.onlyInt)
        self.BinWindow.setText("15")

        self.PlotRange = QLineEdit("")
        self.PlotRange.setPlaceholderText("Range (start:end)")
        #self.onlyInt = QIntValidator()
        self.PlotRange.setValidator(self.onlyInt)
        self.PlotRange.setText(":")

        self.use_codons = QCheckBox("Plot by codons")
        self.PlotControlsCheckbox = QCheckBox("Plot controls")
        self.PlotIndividualSets = QCheckBox("Plot individual sets")
        self.PlotEntrichment = QCheckBox("Plot enrichment")
        self.PlotMeta = QCheckBox("Plot meta")

        self.NoCI = QRadioButton("None")
        self.PlotMinMaxCheckbox = QRadioButton("Plot min and max values")
        self.PlotConfidanceInterval = QRadioButton("Plot CI")
        self.OnlyLowCI = QRadioButton("Only low CI")

        self.ShowTotalRPKMForGene = QCheckBox("Show total RPKM for gene")
        self.NormalizeScale = QCheckBox("Normalize scale")

        self.use_codons.setChecked(True)
        self.PlotConfidanceInterval.setChecked(True)
        self.PlotEntrichment.setChecked(True)

        self.addWidget(self.use_codons)
        self.addWidget(self.BinWindow)
        self.addWidget(self.PlotRange)

        self.addWidget(self.PlotControlsCheckbox)
        self.addWidget(self.PlotIndividualSets)
        self.addWidget(self.PlotEntrichment)
        self.addWidget(self.PlotMeta)

        self.addWidget(self.NoCI)
        self.addWidget(self.PlotMinMaxCheckbox)
        self.addWidget(self.PlotConfidanceInterval)
        self.addWidget(self.OnlyLowCI)

        self.addWidget(self.ShowTotalRPKMForGene)
        self.addWidget(self.NormalizeScale)



