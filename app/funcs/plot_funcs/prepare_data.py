from typing import List
import numpy as np
from funcs.color_utilites import color_variant
from funcs.calculation_utilities.calculate_CI import get_enricment_and_ci
from funcs.calculation_utilities.bin_data import bin_data
from models.graph_unit import GraphUnit
from models.graph_dataset import GraphDataset
from models.data_row import DataRow



def prep_data(graph_dataset_list: List[GraphDataset],
              binning_window: int = 1,
              plot_range: list = [None, None],
              plot_minmax: bool = False,
              plot_control: bool = False,
              plot_enrichment: bool = True,
              plot_individual_data: bool = False,
              show_rpkm: bool = False,
              plot_ci: bool = False,
              normalize_scale: bool = False,
              plot_only_low_ci: bool = False,
              plot_meta: bool = False
            ):

    graph_unit_list = list()
    rpkm_list = []


    if plot_only_low_ci:
        populate_graph_unit_list_plot_only_low_ci(graph_dataset_list, graph_unit_list, binning_window, plot_control)
    elif plot_ci:
        populate_graph_unit_list_plot_ci(graph_dataset_list, graph_unit_list, binning_window, plot_control)
    elif plot_minmax:
        populate_graph_unit_list_minmax(graph_dataset_list, graph_unit_list, binning_window, plot_enrichment, plot_control)
    elif plot_individual_data or plot_meta:
        populate_graph_unit_list_with_individual_plots(graph_dataset_list, graph_unit_list, binning_window, plot_enrichment, plot_control)
    else:
        # not minmax or ci
        populate_graph_unit_list_mean_only(graph_dataset_list, graph_unit_list, binning_window, plot_enrichment)


    if normalize_scale:
        get_normalized_scale_data(graph_unit_list)

    if show_rpkm:
        for graph_dataset in graph_dataset_list:
            rpkm_list.append(graph_dataset.get_RPKM_list())

    return graph_unit_list, rpkm_list


def populate_graph_unit_list_plot_only_low_ci(graph_dataset_list: List[GraphDataset], graph_unit_list: List[GraphUnit], binning_window: int = 1, plot_control: bool = False):
    for graph_dataset in graph_dataset_list:
        dataset_name, _gene_name, color, _gene_length = graph_dataset.get_metadata()
        data_list = graph_dataset.get_data_list()

        append_binned_data_with_only_low_CI_for_plot(graph_unit_list, data_list, binning_window, dataset_name, color)

def populate_graph_unit_list_plot_ci(graph_dataset_list: List[GraphDataset], graph_unit_list: List[GraphUnit], binning_window: int = 1, plot_control: bool = False):
    for graph_dataset in graph_dataset_list:
        dataset_name, gene_name, color, _gene_length = graph_dataset.get_metadata()
        data_list = graph_dataset.get_data_list()

        append_binned_data_with_CI_for_plot(graph_unit_list, data_list, binning_window, dataset_name, gene_name, color)

def append_binned_data_with_only_low_CI_for_plot(graph_unit_list: List[GraphUnit], data_list: List[DataRow], window, dataset_name, color):
    """
    converts a list of GraphDataset to a list of GraphUnit
    specificly prepears data to plot only lower CI data
    """
    #   0       1           2               3               4                       5
    #(data, control, unnormalized_data, total_reads, control_unnormalized_data, control_total_reads)

    for index, data_row in enumerate(data_list):
        np_data = data_row.unnormalized_data
        np_control = data_row.unnormalized_control_data
        (low_ci_array, upp_ci_array) = get_enricment_and_ci(np_data, np_control, data_row.total_reads, data_row.control_total_reads)
        low_ci_array = bin_data(low_ci_array, window)
        graph_unit = GraphUnit(low_ci_array, None, None, dataset_name + " " + str(index), color)
        graph_unit_list.append(graph_unit)

def append_binned_data_with_CI_for_plot(graph_unit_list: List[GraphUnit], data_list: List[DataRow], window: int, dataset_name: str, gene_name: str, color: str):
    """
    converts a list of GraphDataset to a list of GraphUnit
    specificly min and max data are plotting the lower and upper confidance interval
    """
    #   0       1           2               3               4                       5
    #(data, control, unnormalized_data, total_reads, control_unnormalized_data, control_total_reads)

    for index, data_row in enumerate(data_list):
        np_data = data_row.unnormalized_data
        np_control = data_row.unnormalized_control_data
        (low_ci_array, upp_ci_array) = get_enricment_and_ci(np_data, np_control, data_row.total_reads, data_row.control_total_reads)

        enrichment = calculate_enrichment(np_data, np_control, dataset_name, gene_name)
        low_ci_array = enrichment - low_ci_array
        upp_ci_array = enrichment + upp_ci_array
        #low_ci_array = enrichment - (low_ci_array * enrichment)
        #upp_ci_array = enrichment + (upp_ci_array * enrichment)

        enrichment = bin_data(enrichment, window)
        upp_ci_array = bin_data(upp_ci_array, window)
        low_ci_array = bin_data(low_ci_array, window)

        graph_unit = GraphUnit(enrichment, upp_ci_array, low_ci_array, dataset_name + " " + str(index), color)
        graph_unit_list.append(graph_unit)

def get_normalized_scale_data(graph_unit_list: List[GraphUnit]):
    for graph_unit in graph_unit_list:
        normalize_scale_graph_unit(graph_unit)

def normalize_scale_graph_unit(graph_unit: GraphUnit):
    mean_data = graph_unit.mean_data
    min_data = graph_unit.min_data
    max_data = graph_unit.max_data
    # offset from 0
    minimum_value_in_mean_data = np.min(mean_data, axis=0)
    maximum_value_in_mean_data = np.max(mean_data, axis=0)

    mean_data -= minimum_value_in_mean_data
    mean_data /= maximum_value_in_mean_data

    if max_data is not None:
        max_data -= minimum_value_in_mean_data
        max_data /= maximum_value_in_mean_data
    if min_data is not None:
        min_data -= minimum_value_in_mean_data
        min_data /= maximum_value_in_mean_data

    graph_unit.min_data = min_data
    graph_unit.max_data = max_data
    graph_unit.mean_data = mean_data


def populate_graph_unit_list_minmax(graph_dataset_list: List[GraphDataset],
                                    graph_unit_list: List[GraphUnit],
                                    binning_window: int = 1,
                                    plot_enrichment: bool = True,
                                    plot_control: bool = False,
                                    #plot_individual_data: bool = False # cannot plot minmax for individual datasets!
                                    ):
    for graph_dataset in graph_dataset_list:
        dataset_name, gene_name, color, _gene_length = graph_dataset.get_metadata()

        data = graph_dataset.get_data_list()

        data_array_list = []
        data_array_control_list = []
        for data_row in data:
            data_array_list.append(data_row.rpm_normalized_data)
            data_array_control_list.append(data_row.rpm_normalized_control_data)

        if plot_enrichment:
            for i, data_row in enumerate(data_array_list):
                data_array_list[i] = calculate_enrichment(data_array_list[i], data_array_control_list[i], dataset_name, gene_name)

            create_grap_unit_and_append_to_list(graph_unit_list, data_array_list, color, dataset_name, binning_window)
        else:
            create_grap_unit_and_append_to_list(graph_unit_list, data_array_list, color, dataset_name, binning_window)

        if plot_control:
            create_grap_unit_and_append_to_list(graph_unit_list, data_array_control_list, color, dataset_name  + " control", binning_window, line_style="dashed")


def create_grap_unit_and_append_to_list(graph_unit_list: List[GraphUnit], data: List, color: str, dataset_name: str, binning_window: int = 1, line_style: str = "solid"):
    np_data = np.array(data)
    mean_data = np.mean(np_data, axis=0, dtype='float')
    min_data = np_data.min(axis=0)
    max_data = np_data.max(axis=0)

    mean_data = bin_data(mean_data, binning_window)
    min_data = bin_data(min_data, binning_window)
    max_data = bin_data(max_data, binning_window)

    graph_unit = GraphUnit(mean_data, max_data, min_data, dataset_name, color, line_style=line_style)
    graph_unit_list.append(graph_unit)

def populate_graph_unit_list_with_individual_plots(graph_dataset_list: List[GraphDataset], graph_unit_list: List[GraphUnit], binning_window: int = 1, plot_enrichment: bool = True, plot_control: bool = False):
    for graph_dataset in graph_dataset_list:
        dataset_name, gene_name, color, _gene_length = graph_dataset.get_metadata()
        data = graph_dataset.get_data_list()



        if plot_enrichment:
            new_data = []
            for data_row in data:
                new_data.append(calculate_enrichment(data_row.rpm_normalized_data, data_row.rpm_normalized_control_data, dataset_name, gene_name))
            data = new_data
            np_data = np.array(data)
            mean_data = np.mean(np_data, axis=0, dtype='float')
            mean_data = bin_data(mean_data, binning_window)

            graph_unit = GraphUnit(mean_data, None, None, dataset_name, color)
            graph_unit_list.append(graph_unit)
        else:
            for data_row in data:
                graph_unit = GraphUnit(data_row.unnormalized_data, None, None, dataset_name, color)
                graph_unit_list.append(graph_unit)
                if plot_control:
                    graph_unit = GraphUnit(data_row.unnormalized_control_data, None, None, dataset_name + " control", color, line_style="dashed")
                    graph_unit_list.append(graph_unit)





def populate_graph_unit_list_mean_only(graph_dataset_list: List[GraphDataset], graph_unit_list: List[GraphUnit], binning_window: int = 1, plot_enrichment: bool = True):
    for graph_dataset in graph_dataset_list:
        dataset_name, gene_name, color, _gene_length = graph_dataset.get_metadata()
        data = graph_dataset.get_data_list()

        if plot_enrichment:
            new_data = []
            for data_row in data:
                new_data.append(calculate_enrichment(data_row.rpm_normalized_data, data_row.rpm_normalized_control_data, dataset_name, gene_name))
            data = new_data



        np_data = np.array(data)
        mean_data = np.mean(np_data, axis=0, dtype='float')
        mean_data = bin_data(mean_data, binning_window)

        graph_unit = GraphUnit(mean_data, None, None, dataset_name, color)
        graph_unit_list.append(graph_unit)


def calculate_enrichment(main_data, control_data, dataset_name: str, gene_name: str):
    np_data = np.array(main_data, dtype='float')
    np_control = np.array(control_data, dtype='float')
    if 0 in np_control:
        print("WARNING: Control data contains 0", dataset_name, gene_name)
        control_min = 0.02  # 0.004
        if np.any(np_control > 0):
            control_min = np.amin(np_control[np_control > 0.0], axis=0)
        # override
        #control_min = 1
        np_control[np_control == 0] = control_min

    return np_data / np_control
