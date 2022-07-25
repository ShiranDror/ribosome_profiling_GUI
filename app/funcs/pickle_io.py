import pickle
import numpy as np
import csv


def get_dict():
    with open('database/genes_ids_and_names.csv') as csv_file:
        reader = csv.reader(csv_file)
        mydict = dict(reader)
    return mydict

def sum_two_np_arrays(a, b):
    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b
    return c

def get_meta_gene_array(path: str):
    with open(path, "rb") as file:
        dic = pickle.load(file)
        summary_array = np.empty(1, dtype='int')
        total_reads = 0
        for gene_name in dic:
            total_reads += int(np.sum(np.array(dic[gene_name][60:-60])))

        normalization_factor = 1000000 / total_reads

        for gene_name in dic:

            gene_array = np.array(dic[gene_name], dtype='int')
            gene_array = gene_array * normalization_factor
            gene_array /= np.average(gene_array, axis=0)

            summary_array = sum_two_np_arrays(summary_array, gene_array)

        # normalized_array = np.array(summary_array, dtype='float')
        # normalized_array /= total_reads
        return (summary_array, summary_array, total_reads)


def get_gene_array(path: str, gene_name: str):
    """ unpickles file into a dictionary of genes and arrays, and returns normalized(RPM) numpy array by gene_name
        e.g.: dic[gene_name] = [0, 10, 4, 0 ...]
        a
    """

    with open(path, "rb") as file:
        dic = pickle.load(file)
        total_reads = 0
        upper_case_dic = {}
        for key in dic:
            upper_case_dic[key.upper()] = dic[key]
        dic = upper_case_dic
        # skipping for e coli
        # if not gene_name in dic:
        #     gene_dict = get_dict()
        #     found = False
        #     for key, value in gene_dict.items():
        #         if key == gene_name and value in dic:
        #             found = True
        #             gene_name = value
        #         elif value == gene_name and key in dic:
        #             found = True
        #             gene_name = key

        #     if not found:
        #         return 0


        gene_array = np.array(dic[gene_name], dtype='int')

        for key in dic:
            total_reads += int(np.sum(np.array(dic[key][60:-60])))

        normalization_factor = 1000000 / total_reads
        normalized_array = np.array(gene_array, dtype='float')
        normalized_array *= normalization_factor
        return (normalized_array, gene_array, total_reads)

