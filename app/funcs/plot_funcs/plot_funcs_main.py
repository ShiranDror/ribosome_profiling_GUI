import matplotlib.pyplot as plt
import numpy as np
from models.graph_unit import GraphUnit
from typing import List

from funcs.plot_funcs.plot_domains import plot_domains
from funcs.plot_funcs.prepare_data import prep_data

# graph_data, bin_window, plot_minmax, plot_controls, show_rpkm, plot_ci, use_codons, normalize_scale)
# axis = self.figure.add_subplot(111)
            # plot_enrichment: bool = True,
            #   plot_individual_data: bool = False,
      #  rpkm_list = plot_data(graph_dataset_list, axis, binning_window, plot_minmax, plot_control, True, False, show_rpkm, plot_ci, use_codons, normalize_scale)

def plot_data(graph_dataset_list,
              axis,
              plot_range: list = [None, None],
              binning_window: int = 1,
              plot_minmax: bool = False,
              plot_control: bool = False,
              plot_enrichment: bool = True,
              plot_individual_data: bool = False,
              show_rpkm: bool = False,
              plot_ci: bool = False,
              use_codons: bool = True,
              normalize_scale: bool = False,
              plot_only_low_ci: bool = False,
              plot_meta: bool = False
              ):
    if len(graph_dataset_list) == 0:
        print("graph_dataset_list len is 0")
        return [[0, 0]]
    _dataset_name, gene_name, _color, gene_length = graph_dataset_list[0].get_metadata()

    # list(range(len(normalized_sample_mean_data)))
    aa_positions = np.arange(-20, gene_length-20, dtype="float")

    #nt_positions = list(range(-60, gene_length-60))
    #aa_positions = [i / 3 for i in nt_positions]
    #aa_positions = np.true_divide(nt_positions, 3)

    # Standard aspect settings for the plot

    plt.title(gene_name)
    # ax = self.figure.add_subplot(111)
    # ax = self.axes #plt.axes()

    # Plot profiles:

    graph_unit_list, rpkm_list = prep_data( graph_dataset_list=graph_dataset_list,
                                            binning_window=binning_window,
                                            plot_minmax=plot_minmax,
                                            plot_control=plot_control,
                                            plot_enrichment=plot_enrichment,
                                            plot_individual_data=plot_individual_data,
                                            show_rpkm=show_rpkm,
                                            plot_ci=plot_ci,
                                            normalize_scale=normalize_scale,
                                            plot_only_low_ci=plot_only_low_ci,
                                            plot_meta=plot_meta
                                            )

    plot_graph_units(graph_unit_list, axis, aa_positions)

    # length is 60~gene length~60
    length = len(aa_positions)

    plt.xlim(plot_range[0], plot_range[1] or length)



    plot_domains(gene_name, axis, length)

    axis.set_title(gene_name)
    x_label = "Position [Nucleotide]"
    if use_codons:
        x_label = "Position [codons]"

    axis.set_xlabel(x_label, fontweight=800)

    y_label = "Enrichment (co-IP/total)"
    if plot_only_low_ci:
        y_label = "Lower Confidance Interaval"
    if normalize_scale:
        y_label += " normalized 0..1"
    axis.set_ylabel(y_label, fontweight=800)

    axis.axhline(y=1.0, color='k', linestyle='--')
    axis.axhline(y=2.0, color='blue', linestyle='--')
    #    axhline(y=0.002, c="blue",linewidth=0.5,zorder=0)

    return rpkm_list

def plot_graph_units(graph_unit_list: List[GraphUnit], axis, aa_positions):
    for graph_unit in graph_unit_list:
        plot_graph_unit(graph_unit, axis, aa_positions)


def plot_graph_unit(graph_unit: GraphUnit, axis, aa_positions):
    axis.plot(aa_positions, graph_unit.mean_data, label=graph_unit.source_name, linestyle=graph_unit.line_style, marker=graph_unit.marker, color=graph_unit.color, lw=1) #marker=graph_unit.marker,
    if (graph_unit.max_data is not None) or (graph_unit.min_data is not None):
        axis.fill_between(aa_positions, graph_unit.max_data, graph_unit.min_data, linestyle=graph_unit.line_style, color=graph_unit.color, linewidth=0.0, alpha=0.3) #marker=graph_unit.marker,

