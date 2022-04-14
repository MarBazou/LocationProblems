from PyQt5.uic import *

#import networkx as nx

import matplotlib

import matplotlib.pyplot as plt

import os

cur_dir = os.getcwd()

green = matplotlib.colors.to_hex([0.4, 0.7, 0.4])
blue = matplotlib.colors.to_hex([0.4, 0.4, 0.8])
violett = matplotlib.colors.to_hex([0.8, 0.4, 0.8])

color_list=[green,blue,violett]


red = matplotlib.colors.to_hex([0.9, 0.4, 0.3])

obnoxious_nodes = [(1, 2), (10, 20)]
desirable_nodes = [(4, 5), (17, 20)]
facility_nodes = []


def draw_graph(instance, file_name):
    if instance.desirable_dict:
        plt.scatter(*zip(*instance.desirable_dict.values()), c=green, )
    if instance.obnoxious_dict:
        plt.scatter(*zip(*instance.obnoxious_dict.values()), c=red)
    if instance.facility_dict:
        plt.scatter(*zip(*instance.facility_dict.values()), c=blue, marker="*")
    print(cur_dir + "\\" +file_name)
    plt.savefig(cur_dir + "\\" +file_name, bbox_inches="tight")

def draw_graph_multi(instance, file_name):
    i = 0
    for key in instance.facility_dict:
        if instance.nodes_to_facility_dict[key]:
            plt.scatter(*zip(*instance.nodes_to_facility_dict[key]), c=color_list[i])
        if instance.facility_dict:
            plt.scatter(*zip(*[instance.facility_dict[key]]), c=color_list[i], marker="*")
        i += 1
    if instance.obnoxious_dict:
        plt.scatter(*zip(*instance.obnoxious_dict.values()), c=red, marker="2")

    print(cur_dir + "\\" + file_name)
    plt.savefig(cur_dir + "\\" + file_name, bbox_inches="tight")




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
