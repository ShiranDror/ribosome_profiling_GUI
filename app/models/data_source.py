import sys
sys.path.append(".")
from funcs.db import save_new_datasource, update_dataset_color
# from funcs.bin_data import bin_data

class DataSource(object):
    """description of class"""

    def __init__(self, DataSourceId: int = 0, Name: str = "", Description: str = "", Color: str = "", IsActive: bool = True):
        self.DataSourceId = DataSourceId #next(DataSource.newid)
        self.Name = Name
        self.Description = Description
        self.Color = Color
        self.IsActive = IsActive
        self.dataPaths = []

    def AddData(self, paths: tuple):
        self.dataPaths.append(paths)
        
    def GetDataPathsList(self):
        return self.dataPaths
    def GetSQLTuple(self):
        return (self.Name, self.Description, self.Color, self.IsActive)
    def SetId(self, DataSourceId):
        self.DataSourceId = DataSourceId
    def GetId(self):
        return self.DataSourceId
    
    def is_active(self):
        return self.IsActive
        
    def SaveToDatabase(self):
        if self.DataSourceId == 0:
            save_new_datasource(self)
            print("Datasource Saved")
        else:
            print("Cannot save Datasource. Already has id")
    
    def update_color(self, color):
        update_dataset_color(self.DataSourceId, color)
        
