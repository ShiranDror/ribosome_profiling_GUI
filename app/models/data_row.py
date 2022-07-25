import numpy as np

class DataRow(object):
    """
    This class object holds the data of a single "row". Meaning, a single experiment, IP and control
    """
    # (data, control, unnormalized_data, total_reads, control_unnormalized_data, control_total_reads)
    def __init__(self,
                 rpm_normalized_data: np.float_,
                 rpm_normalized_control_data: np.float_,
                 unnormalized_data: np.int_,
                 unnormalized_control_data: np.int_,
                 total_reads: int,
                 control_total_reads: int
                 ):
        self.rpm_normalized_data = rpm_normalized_data
        self.rpm_normalized_control_data = rpm_normalized_control_data
        self.unnormalized_data = unnormalized_data
        self.unnormalized_control_data = unnormalized_control_data
        self.total_reads = total_reads
        self.control_total_reads = control_total_reads
        self.gene_length = len(unnormalized_data)
  
