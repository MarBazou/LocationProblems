
from PyQt5.uic import *

import networkx as nx

import matplotlib

import matplotlib.pyplot as plt

import os

cur_dir  = os.getcwd()



green = matplotlib.colors.to_hex([0.4, 0.7, 0.4])
blue = matplotlib.colors.to_hex([0.4, 0.4, 0.8])
red = matplotlib.colors.to_hex([0.9, 0.4, 0.3])



obnoxious_nodes=[(1,2),(10,20)]
desirable_nodes=[(4,5),(17,20)]
facility_nodes=[]



def DrawGraph(instance):
    if instance.desirable_nodes!=[]:
        plt.scatter(*zip(*instance.desirable_nodes),c=green)
    if instance.obnoxious_nodes!=[]:
        plt.scatter(*zip(*instance.obnoxious_nodes),c=red)
    if instance.facility_nodes:
        plt.scatter(*zip(*instance.facility_nodes),c=blue)
    plt.savefig(cur_dir + "/sanc_fig", bbox_inches="tight")




"""

def LabelIt(G, end_nodes, start_nodes):
    new_dict = {}

    for node in G.nodes:
        new_dict[node] = [nx.shell_layout(G, [start_nodes, end_nodes])[node][0] * 1.05,
                          nx.shell_layout(G, [start_nodes, end_nodes])[node][1] * 1.05]

    label_dict = {}

    for node in end_nodes:
        label_dict[node] = node

    for node in start_nodes:
        label_dict[node] = node

    nx.draw_networkx_labels(G, pos=new_dict, labels=label_dict, font_size=8)


def GetAllPossibleEntries(df_column):
    new_list = []

    column_list = list(df_column)

    for i in range(len(column_list)):
        s_list = column_list[i].split(", ")

        new_list = new_list + s_list

    new_list = list(set(new_list))

    new_list.sort()

    return new_list


def StateList(df):
    sanc_list_1 = list(set(list(df.sanctioned_state)))

    sanc_list_2 = GetAllPossibleEntries(df.sanctioning_state)

    sanc_list = list(set(sanc_list_1 + sanc_list_2))

    sanc_list.sort()

    return sanc_list
"""