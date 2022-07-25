from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import (QWidget, QHeaderView, QHBoxLayout, QVBoxLayout, QTableView, QListWidget, QPushButton,
                               QSizePolicy, QLineEdit, QFileDialog, QTextBrowser)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import math

import sys
sys.path.append(".")
from funcs.extract_data import extract_data, extract_metagene
#from funcs.plot_from_pickle import plot_to_file

from gui_models.DataSourceModule import DataSourceModule
from gui_models.PlotSettings import PlotSettings
from gui_models.PlotWidget import PlotWidget
from gui_models.ExportToolbar import ExportToolbar


class Widget(QWidget):
    """ """
    def __init__(self):
        QWidget.__init__(self)



        # QWidget Layout
        self.main_layout = QHBoxLayout()

        # Left layout
        self.left_layout = DataSourceModule()

        self.main_layout.addLayout(self.left_layout)

        # Right Layout
        #size.setHorizontalStretch(4)
        #self.chart_view.setSizePolicy(size)
        self.SearchBox = QHBoxLayout()
        self.SearchInput = QLineEdit("")
        self.SearchInput.setPlaceholderText("Gene. e.g. PRS5")
        self.SearchButton = QPushButton("Plot!")
        self.SearchButton.clicked.connect(self.Plot)


        self.SearchBox.addWidget(self.SearchInput)
        self.SearchBox.addWidget(self.SearchButton)

        self.PlotSettings = PlotSettings()
        self.canvas_widget = PlotWidget(self, width=10, height=8, dpi=70)
        self.toolbar = NavigationToolbar(self.canvas_widget, self)

        self.export_toolbar = ExportToolbar(self)
        #self.output_text = QtWidgets.QTextBrowser(self)

        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(self.SearchBox, 1)
        self.right_layout.addLayout(self.PlotSettings, 1)
        self.right_layout.addLayout(self.export_toolbar, 1)
        self.right_layout.addWidget(self.toolbar)

        self.right_layout.addWidget(self.canvas_widget)
        #self.right_layout.addWidget(self.output_text)
        #self.right_layout.addWidget(self.chart_view)
        self.main_layout.addLayout(self.right_layout)


        # Set the layout to the QWidget
        self.setLayout(self.main_layout)

        #self.graph_data = []

    def format_gene_text(self, gene_input):
        gene_name_list = gene_input.split(",")
        for index, gene_name in enumerate(gene_name_list):
            gene_name_list[index] = gene_name.strip().upper()
        return gene_name_list


    def Plot(self):
        self.canvas_widget.ClearPlot()
        #self.output_text.clear()
        gene_input = self.SearchInput.text()
        plot_controls = self.PlotSettings.PlotControlsCheckbox.isChecked()
        plot_individual_data = self.PlotSettings.PlotIndividualSets.isChecked()
        plot_enrichment = self.PlotSettings.PlotEntrichment.isChecked()


        plot_meta = self.PlotSettings.PlotMeta.isChecked()
        plot_ci = self.PlotSettings.PlotConfidanceInterval.isChecked()
        plot_minmax = self.PlotSettings.PlotMinMaxCheckbox.isChecked()
        bin_window = int(self.PlotSettings.BinWindow.text() or "1")
        plot_range = self.PlotSettings.PlotRange.text()
        if len(plot_range) < 2 or plot_range.find(":") == -1:
            plot_range = [None, None]
        else:
            plot_range_array = plot_range.split(":")
            plot_range = []
            if (len(plot_range_array[0]) < 1):
                plot_range.append(None)
            else:
                out_number = None
                try:
                    out_number = int(plot_range_array[0])
                except ValueError as ex:
                    print('"%s" cannot be converted to an int: %s' % (plot_range_array[0], ex))
                    pass
                plot_range.append(out_number)

            if (len(plot_range_array[1]) < 1):
                plot_range.append(None)
            else:
                out_number = None
                try:
                    out_number = int(plot_range_array[0])
                except ValueError as ex:
                    print('"%s" cannot be converted to an int: %s' % (plot_range_array[0], ex))
                    pass
                plot_range.append(out_number)

        show_rpkm = self.PlotSettings.ShowTotalRPKMForGene.isChecked()
        use_codons = self.PlotSettings.use_codons.isChecked()
        normalize_scale = self.PlotSettings.NormalizeScale.isChecked()
        plot_only_low_ci = self.PlotSettings.OnlyLowCI.isChecked()
        data_sources = self.left_layout.get_active_source_list()


        self.canvas_widget.ClearPlot()

        gene_name_list = self.format_gene_text(gene_input)
        rpkm_list = []
        if plot_meta:
            gene_name_list = ["Meta gene profile"]

        number_of_rows = math.ceil(len(gene_name_list) / 3)
        if number_of_rows < 1:
            number_of_rows = 1
        number_of_cols = 3
        if len(gene_name_list) < number_of_cols:
            number_of_cols = len(gene_name_list)



        for index, gene_name in enumerate(gene_name_list):
            graph_data = []
            for ds in data_sources:
                try:
                    if plot_meta:
                        graph_data.append(extract_metagene(data_source=ds, use_codons=use_codons))
                    else:
                        graph_data.append(extract_data(gene_name, ds, use_codons))
                except Exception as error:
                    print("Could not open gene: " + gene_name + " from data source: " + ds.Name)
                    print("Unexpected error:", error)
            subplot_index = index + 1
            temp_rpkm_list = self.canvas_widget.PlotData( graph_dataset_list=graph_data,
                                                          binning_window=bin_window,
                                                          plot_range=plot_range,
                                                          plot_minmax=plot_minmax,
                                                          plot_control=plot_controls,
                                                          show_rpkm=show_rpkm,
                                                          plot_ci=plot_ci,
                                                          use_codons=use_codons,
                                                          normalize_scale=normalize_scale,
                                                          plot_only_low_ci=plot_only_low_ci,
                                                          plot_meta=plot_meta,
                                                          plot_enrichment=plot_enrichment,
                                                          plot_individual_data=plot_individual_data,
                                                          subplot_row=number_of_rows,
                                                          subplot_column=number_of_cols,
                                                          subplot_index=subplot_index)
            rpkm_list.append(temp_rpkm_list)

        if (show_rpkm):
            for data in rpkm_list:
                for val in data:
                    print(val)
                    #self.output_text.append(str(val))

    # def export_plot(self, save_filename: str):
    #     gene_name = self.SearchInput.text()
    #     plot_controls = self.PlotSettings.PlotControlsCheckbox.isChecked()
    #     plot_minmax = self.PlotSettings.PlotMinMaxCheckbox.isChecked()
    #     bin_window = int(self.PlotSettings.BinWindow.text() or "1")
    #     data_sources_ids = self.left_layout.get_active_source_ids()
    #     plot_to_file(data_sources_ids, gene_name, save_filename,
    #                     bin_window=bin_window,
    #                     plot_controls=plot_controls,
    #                     plot_minmax=plot_minmax,
    #                     # plot_enrichment=True,
    #                     # get_rpm=True
    #       )


