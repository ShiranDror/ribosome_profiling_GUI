from funcs.db import load_datasources
from models.data_source import DataSource
from gui_models.FileDialog import FileDialog
from gui_models.data_source_form import DataSourceForm
# import os
# import copy
# from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QVBoxLayout, QPushButton

import sys
sys.path.append(".")

# colors = ['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6', '#1f78b4', '#33a02c', '#e31a1c',
#           '#ff7f00', '#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
#
colors = "#5899DA,#E8743B,#19A979,#ED4A7B,#945ECF,#13A4B4,#525DF4,#BF399E,#6C8893,#EE6868,#2F6497".split(",")

class DataSourceModule(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)
        self.SourcesList = []
        
        self.data_source_form = DataSourceForm(self)
        
        self.addDatasourceButton = QPushButton("Add")
        
        # size = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        # self.data_source_form.setSizePolicy(size)

        self.addLayout(self.data_source_form)
        self.addStretch(1)
        self.addWidget(self.addDatasourceButton)

        self.addDatasourceButton.clicked.connect(self.OpenFileDialog)

        self.populate_datasource_form()

    def populate_datasource_form(self):
        self.LoadDatasources()
       
        self.data_source_form.populate(self.SourcesList)
      
    def GetSourceList(self):
        return self.SourcesList
   
    def get_active_source_list(self):
        return [item for item in self.SourcesList if item.is_active()]

    def get_active_source_ids(self):
        sources = self.get_active_source_list()
        ids = []
        for source in sources:
            ids.append(source.GetId())
        return ids

    def OpenFileDialog(self):
        """ opens files selection dialog """
        file_dialog = FileDialog(self)
        file_dialog.setBaseSize(400, 700)
        file_dialog.show()

    def AddNewFiles(self, NewDataFiles: list, name: str = "", desc: str = ""):
        # NewDataFiles is a list of tuples, [(DataPath, ControlPath), ... ]
        color = colors[len(self.SourcesList) % len(colors)]
        ds = DataSource(DataSourceId=0, Name=name,
                        Description=desc, Color=color, IsActive=True)
        for i in range(len(NewDataFiles)):
            ds.AddData(NewDataFiles[i])
        ds.SaveToDatabase()
        self.populate_datasource_form()

    def LoadDatasources(self):
        self.SourcesList = load_datasources()