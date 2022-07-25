"""  """
import pathlib
import matplotlib.pyplot as plt
from funcs.db import load_datasources, create_database
from funcs.extract_data import extract_data
from funcs.plot_funcs.plot_funcs_main import plot_data


def init_db():
    database_folder = pathlib.Path(__file__).parent.absolute() / "database"
    database_folder.mkdir(parents=True, exist_ok=True)
    database_folder = database_folder / "sqlite3.db"
    create_database(database_folder.resolve())


# def plot_to_file(relevant_ids: list,
#                 gene_name: str,
#                 filename: str,
#                 bin_window: int = 60,
#                 plot_controls: bool = False,
#                 plot_minmax: bool = True,
#                 use_normalized_data: bool = True,
#                 get_rpm: bool = True
#     ):
#     """ """
#     full_sources_list = load_datasources()
#     data_sources = []
#     for datasource in full_sources_list:
#         name, _desc, color, isactive = datasource.GetSQLTuple()
#         ds_id = datasource.GetId()
#         print(ds_id, name, color, isactive)
#         if ds_id in relevant_ids:
#             data_sources.append(datasource)

#     graph_data = []
#     for data_source in data_sources:
#         try:
#             graph_data.append(extract_data(gene_name, data_source))
#         except:
#             print("Could not open gene: " + gene_name + " from data source: " + data_source.Name)
        
        

#     figure = plt.figure(figsize=(10, 6))
#     ax = figure.add_subplot(111)
#     plot_data(graph_data, ax, bin_window, plot_minmax, plot_controls, use_normalized_data, not get_rpm)
    
#     plt.savefig(filename, format="svg", transparent=True, dpi=1200)
#     plt.show()

if __name__ == "__main__":
    init_db()
    # genename = "FAS2"
    # plot_to_file(relevant_ids=[21],
    #             gene_name=genename,
    #             filename='C:/Users/Shiran/Desktop/'+genename+"_plot.svg",
    #             bin_window=60,
    #             plot_controls=False,
    #             plot_minmax=True,
    #             use_normalized_data=True,
    #             get_rpm=True
    # )

