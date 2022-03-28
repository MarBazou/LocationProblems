'''
Created on 04.11.2021

@author: Markus Bozau

Todo: obstacles
      forbiddenareas
      weights
      die andere linearisierung implementieren
      verschiedene Modelle für verschiedene Zielfunktionen erstellen
      die Betragsrestriktionen kann evtl geändert werden ohne integer

HowTo:
call Instance Generator with integers for:
desirable_numb
obnoxious_numb
max_x
max_y
'''

from random import randint


class INSTANCE(object):
    def __init__(self, desirable_nodes, obnoxious_nodes, facility_nodes=None):
        self.desirable_nodes = desirable_nodes
        self.obnoxious_nodes = obnoxious_nodes
        self.facility_nodes = facility_nodes


class SolInstance(object):
    def __init__(self, desirable_dict, obnoxious_dict, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal):
        self.desirable_dict = desirable_dict
        self.obnoxious_dict = obnoxious_dict
        self.max_coord = max_coord
        self.facility_numb = facility_numb
        self.d_goal = d_goal
        self.o_goal = o_goal
        self.f_interaction_goal = f_interaction_goal
        self.node_coord_a_dict, self.node_coord_b_dict = self.construct_coord_dicts()
        # obstacle
        # forbiddenareas
        # weights
        self.solution = None

    def construct_coord_dicts(self):
        node_coord_a_dict, node_coord_b_dict = {}, {}
        for node in self.desirable_dict:
            node_coord_a_dict[node] = self.desirable_dict[node][0]
        for node in self.obnoxious_dict:
            node_coord_a_dict[node] = self.obnoxious_dict[node][0]
        for node in self.desirable_dict:
            node_coord_b_dict[node] = self.desirable_dict[node][1]
        for node in self.obnoxious_dict:
            node_coord_b_dict[node] = self.obnoxious_dict[node][1]
        return node_coord_a_dict, node_coord_b_dict


def instance_generator(desirable_numb, obnoxious_numb, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal):
    return generator(desirable_numb, obnoxious_numb, facility_numb, max_coord, d_goal, o_goal,
                     f_interaction_goal)


def generator(desirable_numb, obnoxious_numb, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal):
    desirable_dict = {}
    obnoxious_dict = {}
    i = 0
    while i < desirable_numb:
        i = i + 1
        desirable_dict[i] = [randint(0, max_coord), randint(0, max_coord)]
    j = i
    while j < desirable_numb + obnoxious_numb:
        j = j + 1
        obnoxious_dict[j] = [randint(0, max_coord), randint(0, max_coord)]
    return SolInstance(desirable_dict, obnoxious_dict, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal)
