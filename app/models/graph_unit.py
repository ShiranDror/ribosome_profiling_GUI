import numpy as np

class GraphUnit(object):
    """
    This class object holds the data directly required for plotting and nothing more
    """

    def __init__(self,
                 mean_data: np.float_,
                 max_data: np.float_,
                 min_data: np.float_,
                 source_name: str,
                 color: str,
                 line_style: str = "solid",
                 marker: str = "None"
                 ):
        self.mean_data = mean_data
        self.max_data = max_data
        self.min_data = min_data
        self.source_name = source_name
        self.color = color
        self.line_style = line_style
        self.marker = marker
