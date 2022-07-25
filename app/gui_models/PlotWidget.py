# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#               2015 Jens H Nielsen
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitatio

from __future__ import unicode_literals
import sys
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide2 import QtWidgets


# Make sure that we are using QT5
matplotlib.use('Qt5Agg')


#from matplotlib.pyplot import Figure


sys.path.append(".")
from funcs.plot_funcs.plot_funcs_main import plot_data
from funcs.plot_funcs.settings import plot_settings


# progname = os.path.basename(sys.argv[0])
# progversion = "0.1"


class PlotWidget(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width: int = 5, height: int = 4, dpi: int = 300):
        #x = plt.Figure()
        self.figure = plt.Figure(figsize=(width, height), dpi=dpi)

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        #self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent

        #self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        plot_settings()

    def ClearPlot(self):
        self.figure.clear()

    def PlotData(self, graph_dataset_list,
                binning_window: int = 1,
                plot_range: list = [],
                plot_minmax: bool = False,
                plot_control: bool = False,
                show_rpkm: bool = False,
                plot_ci: bool = False,
                use_codons: bool = True,
                normalize_scale: bool = False,
                plot_only_low_ci: bool = False,
                plot_meta: bool = False,
                plot_enrichment: bool = True,
                plot_individual_data: bool = False,
                subplot_row: int = 1,
                subplot_column: int = 1,
                subplot_index: int = 1
                ):

        axis = self.figure.add_subplot(subplot_row, subplot_column, subplot_index)

        rpkm_list = plot_data(graph_dataset_list=graph_dataset_list,
                                axis=axis,
                                plot_range = plot_range,
                                binning_window=binning_window,
                                plot_minmax=plot_minmax,
                                plot_control=plot_control,
                                plot_enrichment=plot_enrichment,
                                plot_individual_data=plot_individual_data,
                                show_rpkm=show_rpkm,
                                plot_ci=plot_ci,
                                use_codons=use_codons,
                                normalize_scale=normalize_scale,
                                plot_only_low_ci=plot_only_low_ci,
                                plot_meta=plot_meta)
        if subplot_index == 1:
            if subplot_column == 1 and subplot_row == 1:
                axis.legend()
            else:
                handles, labels = axis.get_legend_handles_labels()
                self.figure.legend(handles, labels, loc=1, mode='expand', numpoints=1, ncol=8, fancybox=True, fontsize='small')

        self.draw()
        self.figure.tight_layout()
        return rpkm_list




