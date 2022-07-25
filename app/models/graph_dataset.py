# from funcs.calculation_utilities.bin_data import bin_data, bin_array_sum
# from funcs.calculation_utilities.calculate_CI import calc_agrest_coull_CI
import numpy as np

from models.data_row import DataRow

# import sys
# sys.path.append(".")


class GraphDataset(object):
    """description of class"""

    def __init__(self, dataset_name: str, gene_name: str, color: str, description: str):
        self.dataset_name = dataset_name
        self.gene_name = gene_name
        self.color = color
        self.description = description
        self.data_list = list()
   
    def get_data_list(self):
        return self.data_list

    def get_metadata(self):
        """ returns metadata dataset_name, gene_name, color, gene_length """
        return self.dataset_name, self.gene_name, self.color, self.get_gene_length()

    def get_gene_length(self):
        if len(self.data_list) > 0 and self.data_list[0]:
            return self.data_list[0].gene_length
        return 0

    def get_RPKM_list(self):
        """ data, control, unnormalized_data, total_reads, control_unnormalized_data, control_total_reads """
        rpkm_list = []
        for data in self.data_list:
            control_data = data[4]
            if len(control_data) > 120:
                control_data = control_data[60:-60]
            total_reads_for_gene = np.sum(control_data, axis=0, dtype='float')
            rpkm_list.append(total_reads_for_gene / data[5])
        return rpkm_list

    # graph_dataset.add_data((data, control, unnormalized_data, total_reads, control_unnormalized_data, control_total_reads))
    def add_data(self, data_row: DataRow):
        """ Add data tuple (data, control). Data is considered already RPM normalized, but not post enrichment calculation
            tuple contains 2 normal arrays, which will be convereted to numpy arrays
        """
        self.data_list.append(data_row)

    def rescale_all_data(self):
        scaled_data_list = []
        for data in self.data_list:
            scaled_data_list.append((self.normalize_scale_graph_unit(data[0]), self.normalize_scale_graph_unit(data[1]), self.normalize_scale_graph_unit(data[2]), data[3], self.normalize_scale_graph_unit(data[4]), data[5]))
        return scaled_data_list

    def normalize_scale_graph_unit(self, data_array):
        # offset from 0
        minimum_value_in_mean_data = np.min(data_array, axis=0)
        maximum_value_in_mean_data = np.max(data_array, axis=0)
        return (data_array - minimum_value_in_mean_data) / maximum_value_in_mean_data