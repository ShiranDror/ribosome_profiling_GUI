import matplotlib.pyplot as plt
import numpy as np

def plot_domains(gene_name, axis, length, use_codons: bool = True):
     if gene_name == "FAS2":
        axis.axvspan(0, 94, alpha=0.2, color='orange', label="Codons 1-94")
        _, ymax = plt.ylim()
        _, ymax = axis.get_ylim()
        # ymax = plt.gca().get_ylim()
        # ymax = 
        y_correction = int(-0.1*ymax)
        # np.linspace(start=0,stop=length-120,num=length-119, dtype= int)
        xs = list(range(int(length)-40))
        ys = np.full(int(length)-40, y_correction)
        domain_markers = [(0, 94), (140, 302), (328, 539), (603, 940), (1015, 1661), (1747, 1886), (1110, 1173)]

        # color /A:1-94 #c23b23
        # 2dlabels text MPT size 30 bold True color #c23b23 margin 5

        # color /A:140-302 #f39a27
        # 2dlabels text ACP size 30 bold True color #f39a27 margin 5

        # color /A:328-539 #eada52
        # 2dlabels text SD1α size 30 bold True color #eada52 margin 5

        # color /A:603-940 #03c03c
        # 2dlabels text KR size 30 bold True color #03c03c margin 5

        # color /A:1015-1661 #579abe
        # 2dlabels text KS size 30 bold True color #579abe margin 5

        # color /A:1747-1886 #976ed7
        # 2dlabels text PPT size 30 bold True color #976ed7 margin 5

        # color /A:1110-1173 #5edfdb
        # 2dlabels text SD2α size 30 bold True color #5edfdb margin 5

        markers_on = create_range_list(domain_markers)
        marker_height = 7.0
        marker_width = 1.0
        verts = [
                (-marker_width/2, -marker_height/2),  # left, bottom
                (-marker_width/2, marker_height/2),  # left, top
                (marker_width/2, marker_height/2),  # right, top
                (marker_width/2, -marker_height/2),  # right, bottom
                (0., 0.),  # ignored
            ]
        axis.plot(xs, ys, marker=verts, markersize=7, color="#993333", linewidth=3, markevery=markers_on, label="Domains")

def create_range_list(tuple_list):
    answer = list()
    for tup in tuple_list:
        answer += list(range(tup[0], tup[1]))
    answer = np.unique(np.sort(answer))
    return list(answer)