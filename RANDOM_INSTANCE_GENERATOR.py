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
import os
from random import randint


class INSTANCE(object):
    def __init__(self, desirable_nodes, obnoxious_nodes, facility_nodes=[]):
        self.desirable_nodes = desirable_nodes
        self.obnoxious_nodes = obnoxious_nodes
        self.facility_nodes = facility_nodes


class SolInstance(object):
    def __init__(self, desirable_dict, obnoxious_dict, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal):
        print("huhu")
        self.desirable_dict = desirable_dict
        self.obnoxious_dict = obnoxious_dict
        self.facility_dict = {}
        self.max_coord = max_coord
        self.facility_numb = facility_numb
        self.d_goal = d_goal
        self.o_goal = o_goal
        self.f_interaction_goal = f_interaction_goal
        self.node_coord_a_dict, self.node_coord_b_dict = self.construct_coord_dicts()
        self.nodes_to_facility_dict={}
        # obstacle
        # forbiddenareas
        # weights
        self.solution = None

    def facility_extract(self, a_dict, b_dict):
        for key in a_dict:
            self.facility_dict[key] = (a_dict[key], b_dict[key])

    def nodes_to_facility(self,big_b_dict):
        for key in self.facility_dict:
            self.nodes_to_facility_dict[key]=[]
        if self.facility_numb>1:
            for key in big_b_dict:
                if big_b_dict[key]==1:
                    self.nodes_to_facility_dict[key[0]].append(self.desirable_dict[key[1]])





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



def WriteInstanceFile(file_name, instance):
    i_file = open(os.getcwd() + "\\Instances\\" + file_name + ".flp", "w")
    i_file.write("d\n")
    for key in instance.desirable_dict:
        i_file.write(str(instance.desirable_dict[key][0]) + " " + str(instance.desirable_dict[key][1]) + "\n")
    i_file.write("o\n")
    i = 1
    for key in instance.obnoxious_dict:
        if i == len(instance.obnoxious_dict):
            i_file.write(str(instance.obnoxious_dict[key][0]) + " " + str(instance.obnoxious_dict[key][1]) + "\n")
        else:
            i_file.write(str(instance.obnoxious_dict[key][0]) + " " + str(instance.obnoxious_dict[key][1]) + "\n")
        i += 1
    i_file.close()

def ReadInstance(instance_file):
    print(instance_file)
    print(os.getcwd())
    if_cont = iter(open(os.getcwd() + "\\Instances\\" + instance_file + ".flp"))
    print(if_cont)
    state = None
    d_list = []
    o_list = []
    for line in if_cont:
        line = line.strip("\n")
        print(line)
        if line == "o":
            state = "obnoxious"
            continue
        if line == "d":
            state = "desirable"
            continue
        if line != "o" and line != "d" and line != "":
            integer_map = map(int, line.split(" "))
            integer_list = list(integer_map)
        if state == "obnoxious":
            o_list.append(tuple(integer_list))
        elif state == "desirable":
            d_list.append(tuple(integer_list))
        else:
            pass
    return INSTANCE(d_list, o_list)

def BuiltSolInstance(instance,d_goal, o_goal, a_numb, f_numb):
    desirable_dict, obnoxious_dict = {}, {}
    i = 0
    for node in instance.desirable_nodes:
        i += 1
        desirable_dict[i] = node
    k = i
    for node in instance.obnoxious_nodes:
        k += 1
        obnoxious_dict[k] = node
    print(desirable_dict, obnoxious_dict, f_numb, 1000, 1000, d_goal, o_goal)
    sol_instance = SolInstance(desirable_dict, obnoxious_dict, f_numb, 1000, d_goal, o_goal, None)
    return sol_instance