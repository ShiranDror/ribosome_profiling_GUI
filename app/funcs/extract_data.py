import sys
sys.path.append(".")
from models.graph_dataset import GraphDataset
from models.data_source import DataSource
from models.data_row import DataRow
#from funcs.HDF5io import GetNormalizedGeneData
from funcs.pickle_io import get_gene_array, get_meta_gene_array
from funcs.calculation_utilities.bin_data import bin_and_shrink

def extract_metagene(data_source: DataSource, use_codons: bool = True):
    graph_dataset = GraphDataset(data_source.Name, "Metagene", data_source.Color, data_source.Description)
    for paths_tuple in data_source.GetDataPathsList():
            (data, unnormalized_data, total_reads) = get_meta_gene_array(paths_tuple[0])
            if use_codons:
                data = bin_and_shrink(data, 3)
                unnormalized_data = bin_and_shrink(unnormalized_data, 3)
            control = []

            control_path = paths_tuple[1]
            if control_path and len(control_path) > 0:
                (control, control_unnormalized_data, control_total_reads) = get_meta_gene_array(control_path)
                if use_codons:
                    control = bin_and_shrink(control, 3)
                    control_unnormalized_data = bin_and_shrink(control_unnormalized_data, 3)

            
            data_row = DataRow(data, control, unnormalized_data, control_unnormalized_data, total_reads, control_total_reads)
            graph_dataset.add_data(data_row)

    return graph_dataset

def extract_data(gene_name: str, data_source: DataSource, use_codons: bool = True):
    """ """
    graph_dataset = GraphDataset(data_source.Name, gene_name, data_source.Color, data_source.Description)
    for paths_tuple in data_source.GetDataPathsList():

        (data, unnormalized_data, total_reads) = get_gene_array(paths_tuple[0], gene_name)
        if use_codons:
            data = bin_and_shrink(data, 3)
            unnormalized_data = bin_and_shrink(unnormalized_data, 3)
        control = []

        control_path = paths_tuple[1]
        if control_path and len(control_path) > 0:
            (control, control_unnormalized_data, control_total_reads) = get_gene_array(control_path, gene_name)
            if use_codons:
                control = bin_and_shrink(control, 3)
                control_unnormalized_data = bin_and_shrink(control_unnormalized_data, 3)

        
        data_row = DataRow(data, control, unnormalized_data, control_unnormalized_data, total_reads, control_total_reads)
        graph_dataset.add_data(data_row)

    return graph_dataset
