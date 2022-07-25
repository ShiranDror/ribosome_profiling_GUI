from functools import partial
from PySide2 import QtGui
from PySide2.QtWidgets import QGridLayout, QLabel, QCheckBox, QPushButton, QColorDialog, QWidgetItem
import sys
sys.path.append(".")
from models.data_source import DataSource
from funcs.db import delete_datasource, toggle_dataset_active

class DataSourceForm(QGridLayout):
    def __init__(self, parent):
        QGridLayout.__init__(self)
        self.parent = parent
        
    def clear_layout(self):
        for i in reversed(range(self.count())):
            item = self.itemAt(i)

            if isinstance(item, QWidgetItem):
                item.widget().close()

            # remove the item from layout
            self.removeItem(item)
            
    def populate(self, data_source_list: list):
        self.clear_layout()
        
        
        for index, data_source in enumerate(data_source_list):
            name, _description, color, is_active = data_source.GetSQLTuple()
            
            color_button = QPushButton("")
            color_button.setStyleSheet("QPushButton {background-color: " + color + ";}")
            color_button.clicked.connect(partial(self.change_color, data_source))
            
            checkbox = QCheckBox(name)
            checkbox.setChecked(is_active)
            checkbox.clicked.connect(partial(self.checkbox_clicked, data_source.GetId()))
            
            delete_button = QPushButton("DELETE")
            delete_button.setStyleSheet("QPushButton {background-color: #dc3545; border-color:#dc3545; color: #fff;}")
            delete_button.clicked.connect(partial(self.delete_datasource, data_source.GetId()))
            
            self.addWidget(color_button, index, 1)
            self.addWidget(checkbox, index, 2)
            self.addWidget(delete_button, index, 3)
        
    def checkbox_clicked(self, datasource_id):
        toggle_dataset_active(datasource_id)
        self.parent.populate_datasource_form()
    
    def change_color(self, data_source: DataSource):
        qcolor = QColorDialog().getColor()
        new_color = qcolor.name()
        data_source.update_color(new_color)
        self.parent.populate_datasource_form()
        
    def delete_datasource(self, datasource_id: int):
        delete_datasource(datasource_id)
        self.parent.populate_datasource_form()
            
            