from math import sqrt
import os
import math
import sympy




class Model(object):
    def __init__(self, instance, approx_lvl_integer):
        directory = os.getcwd()
        self.Instance = instance
        self.approx_lvl_integer = approx_lvl_integer
        self.q_dict = self.chain_roots()
        self.slices = 2 ** (self.approx_lvl_integer + 2)
        self.theta_list = self.calculate_theta()
        self.sin_dict, self.cos_dict = self.calculate_trigon()
        print("sin",self.sin_dict)
        print("q", self.q_dict)
        self.obj_string = "GF"
        self.objective = 1000000
        self.var_sol_dict = {}
        self.var_name_array, self.def_list, self.goal_list, self.const_list = self.model_cont()
        self.set_data_dict, self.param_data_dict = self.data_cont()
        self.mod_string = ""
        self.mod_string_construct()
        self.dat_string = ""
        self.dat_string_construct()

        # todo >= or = # initialisierung der ersten ebene damit haetten wir manhatten Norm

    def model_cont(self):
        var_name_array = self.var_cont()
        def_list = self.def_cont()
        goal_list = self.goal_cont()
        const_list = self.const_cont()
        return var_name_array, def_list, goal_list, const_list

    @staticmethod
    def var_cont():
        return []

    @staticmethod
    def def_cont():
        return []

    @staticmethod
    def goal_cont():
        return []

    @staticmethod
    def const_cont():
        return []

    def data_cont(self):
        """set_data_dict = {"E": self.Instance.edges_oneway}
        param_data_dict = {"V_numb": len(self.Instance.nodes)}
        return set_data_dict, param_data_dict"""
        return {}, {}

    @staticmethod
    def built_string_from_string_list(string_list):
        big_string = ''
        for strg in string_list:
            big_string += strg + "\n"
        return big_string

    def constraints(self):
        return self.built_string_from_string_list(self.const_list)

    def definitions(self):
        return self.built_string_from_string_list(self.def_list)

    def goal_fun(self):
        return self.built_string_from_string_list(self.goal_list)

    def mod_string_construct(self):
        self.mod_string += self.definitions() + "\n"
        self.mod_string += self.goal_fun() + "\n"
        self.mod_string += self.constraints()

    def dat_string_construct(self):  # at the moment just sets todo parameters
        for key in self.param_data_dict:
            if isinstance(self.param_data_dict[key], (int, float)):
                self.dat_string_param_from_single(self.param_data_dict[key], key)
            if isinstance(self.param_data_dict[key], dict):
                self.dat_string_param_from_dict(self.param_data_dict[key], key)
            if isinstance(self.param_data_dict[key], list):
                self.dat_string_param_from_list(self.param_data_dict[key], key)
        for key in self.set_data_dict:
            if isinstance(self.set_data_dict[key], dict):
                self.dat_string_set_from_dict(self.set_data_dict[key], key)
            elif isinstance(self.set_data_dict[key], list):
                self.dat_string_set_from_list(self.set_data_dict[key], key)
        self.dat_string

    def dat_string_param_from_single(self, single, param_name):
        self.dat_string += "param " + param_name + (":= %s;\n" % single)

    def dat_string_param_from_dict(self, dictionary, param_name):
        b_string = ""
        for key in dictionary:
            b_string = b_string + " " + str(key) + " " + str(dictionary[key])
        self.dat_string += "param " + param_name + (":=%s;\n" % b_string)

    def dat_string_param_from_list(self, lst, param_name):
        b_string = ""
        for element in lst:
            b_string = b_string + " " + str(lst.index(element) + 1) + " " + str(element)
        self.dat_string += "param " + param_name + (":=%s;\n" % b_string)

    def dat_string_set_from_dict(self, dictionary, set_name):
        for key in dictionary:
            b_string = ""
            for ele in dictionary[key]:
                b_string = b_string + " " + str(ele)
            self.dat_string += "set " + set_name + ("[%s]:=%s;\n" % (key, b_string))

    def dat_string_set_from_list(self, d_list, set_name):
        b_string = ""
        for ele in d_list:
            b_string = b_string + " " + str(ele)
        self.dat_string += "set " + set_name + (":=%s;\n" % b_string)

    def chain_roots(self):
        i = 1
        q_dict = {}
        q_i = 0
        while i <= self.approx_lvl_integer:
            q_i = sympy.sqrt(q_i + 2)
            q_dict[i] = sympy.N(q_i)
            i = i + 1
        return q_dict

    def calculate_theta(self):
        theta = 2*sympy.pi / self.slices
        theta_list = []
        for i in range(self.slices):
            theta_list.append((i + 1) * theta)
        return theta_list

    def calculate_trigon(self):
        sin_dict, cos_dict = {}, {}
        i = 1
        for theta in self.theta_list:
            sin_dict[i] = sympy.N(sympy.sin(theta))
            cos_dict[i] = sympy.N(sympy.cos(theta))
            i += 1
        return sin_dict, cos_dict


"""
########################################################################################################################
# Fermat Weber 

# INIT11 - initialisierung der ersten ebene damit haetten wir manhatten Norm
# ABS11  - rekursiver Aufbau der Betragsfunktion f'_i
# MIN11  - rekursiver Aufbau der Minimumfunktion f''_i
# MIN12  - geaendert man kann den binaeren teil auch noch dran hauen an die <= restriktionen
# MIN13  - besser jeder test war laufzeit technisch wesentlich performanter (haette ich so nicht erwartet)
# Min14  - ueberall durchgefuehrt im test faktor 30 schneller
# MIN15  - Schalter fuer y_i binary variable der Minimumfunktion f''_i
# EUCL   - Approximierter Wert fuer euklidische Entfernung
# ZMAX   - Maximum der Entfernungen erwuenschter Nodes
# ZMIN   - Minimum der Entfernungen unerwuenschter Nodes

# ("subject to MIN_16{k in NODES,i in Levels}: z_1[k,i-1] - z_2[k,i-1] >= 0 - (1 - y[k,i])*M ;\n")  
# vermutlich ueflue durch ABS 11-14
"""


class DesiredMaxObnoxiousMinModel(Model):
    def __init__(self, instance, approx_lvl_integer):
        Model.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def var_cont():
        return ["new_a", "new_b", "a", "b", "z_1", "z_2", "y", "x", "Z"]

    @staticmethod
    def def_cont():
        return ["param desirable_node_number;",
                "param obnoxious_node_number;",
                "param node_number:=desirable_node_number + obnoxious_node_number ;",
                "param approx_level_integer ;",
                "set D_NODES:= 1 .. desirable_node_number;",
                "set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;",
                "set NODES:= D_NODES union O_NODES;",
                "param a_coord{NODES};",
                "param b_coord{NODES};",
                "param max_coord:=1000;",
                "set Levels := 1 .. approx_level_integer ordered;",
                "set Levels_Z := 0 .. approx_level_integer ordered;",
                "param q{Levels};",
                "param M:=2000;",
                "var new_a >=0, <= max_coord ;",
                "var new_b >=0, <= max_coord ;",
                "var a{NODES} ;",
                "var b{NODES} ;",
                "var z_1{NODES,Levels_Z} >=0;",
                "var z_2{NODES,Levels_Z} >=0;",
                "var y{NODES,Levels_Z} binary;",
                "var x{NODES,Levels_Z} binary;",
                "var Z{NODES} >=0;",
                "var Z_max_des >=0;",
                "var Z_min_ob >=0, <=1000000000*obnoxious_node_number;"
                ]

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " Z_max_des - Z_min_ob;"]
        # " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"
        # " sum{k in D_NODES}Z[k]- Z_min_ob;"
        # "Z_max_des - sum{k in O_NODES}Z[k];"

    @staticmethod
    def const_cont():
        return ["subject to INIT_11{k in NODES}: z_1[k,0] >= a[k]  ;",
                "subject to INIT_12{k in O_NODES}: z_1[k,0] <= a[k] + x[k,0]*M;",
                "subject to INIT_13{k in NODES}: z_1[k,0] >= -a[k] ;",
                "subject to INIT_14{k in O_NODES}: z_1[k,0] <= -a[k] +(1-x[k,0])*M;",
                "subject to INIT_21{k in NODES}: z_2[k,0] >= b[k] ;",
                "subject to INIT_22{k in O_NODES}: z_2[k,0] <= b[k] + y[k,0] *M;",
                "subject to INIT_23{k in NODES}: z_2[k,0] >= -b[k] ;",
                "subject to INIT_24{k in O_NODES}: z_2[k,0] <= -b[k] +(1-y[k,0])*M;",



                "subject to ABS_11{k in NODES,i in Levels}: z_1[k,i]>=z_1[k,i-1] - z_2[k,i-1] ;",
                "subject to ABS_12{k in O_NODES,i in Levels}: z_1[k,i]<=z_1[k,i-1] - z_2[k,i-1] +(1 - y[k,i])*M ;",
                "subject to ABS_13{k in NODES,i in Levels}: z_1[k,i]>=z_2[k,i-1] - z_1[k,i-1] ;",
                "subject to ABS_14{k in O_NODES,i in Levels}: z_1[k,i]<=z_2[k,i-1] - z_1[k,i-1] +y[k,i]*M;",

                "subject to MIN_11{k in NODES,i in Levels}: z_2[k,i]<=q[i] * z_1[k,i-1];",
                "subject to MIN_12{k in D_NODES,i in Levels}: z_2[k,i]>=q[i] * z_1[k,i-1] - y[k,i]*M ;",
                "subject to MIN_13{k in NODES,i in Levels}: z_2[k,i]<=q[i] * z_2[k,i-1] ;",
                "subject to MIN_14{k in D_NODES,i in Levels}: z_2[k,i]>=q[i] * z_2[k,i-1] - (1 - y[k,i])*M ;",
                "subject to MIN_15{k in D_NODES,i in Levels}: z_2[k,i-1] - z_1[k,i-1] >=0 - y[k,i]*M ;",

                "subject to EUCL{k in NODES}: Z[k] = z_1[k,last(Levels)] +  z_2[k,last(Levels)] ;",

                "subject to A_Diff{k in NODES}: a[k] = a_coord[k] - new_a ;",
                "subject to B_Diff{k in NODES}: b[k] = b_coord[k] - new_b ;",

                "subject to ZMAX{k in D_NODES}: Z_max_des >= Z[k] ;",
                "subject to ZMIN{k in O_NODES}: Z_min_ob <= Z[k] ;"

                ]

    """
    "subject to LCuts5{k in NODES}:  Z[k]  <= 1.005*(z_1[k,0] + z_2[k,0]);",
    "subject to LCuts1{k in NODES}:  Z[k]  >= 1/q[1]*(a[k] + b[k]);",
    "subject to LCuts2{k in NODES}:  Z[k]  >= 1/q[1]*(-a[k] + b[k]);",
    "subject to LCuts3{k in NODES}:  Z[k]  >= 1/q[1]*(a[k] - b[k]);",
    "subject to LCuts4{k in NODES}:  Z[k]  >= 1/q[1]*(-a[k] - b[k]);"
    ]"""

    # todo not necessary but maybe faster with ABS01-04

    def data_cont(self):
        set_data_dict = {}
        param_data_dict = {"desirable_node_number": len(self.Instance.desirable_dict),
                           "obnoxious_node_number": len(self.Instance.obnoxious_dict),
                           "approx_level_integer": self.approx_lvl_integer,
                           "a_coord": self.Instance.node_coord_a_dict,
                           "b_coord": self.Instance.node_coord_b_dict,
                           "q": self.q_dict}
        return set_data_dict, param_data_dict


class DesiredSumObnoxiousSumModel(DesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"]


class DesiredSumObnoxiousMinModel(DesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "sum{k in D_NODES}Z[k]- Z_min_ob;"]
        # "Z_max_des - sum{k in O_NODES}Z[k];"


class DesiredMaxObnoxiousSumModel(DesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "Z_max_des - sum{k in O_NODES}Z[k];"]


########################################################################################################################
########################################################################################################################
#
# other modelling technique
#
# China
#
########################################################################################################################
########################################################################################################################

class ChinaDesiredMaxObnoxiousMinModel(Model):
    def __init__(self, instance, approx_lvl_integer):
        Model.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def var_cont():
        return ["new_a", "new_b", "a", "b", "z_1", "z_2", "y", "x", "Z"]

    @staticmethod
    def def_cont():
        return ["param desirable_node_number;",
                "param obnoxious_node_number;",
                "param node_number:=desirable_node_number + obnoxious_node_number ;",
                "param slice_number ;",
                "set D_NODES:= 1 .. desirable_node_number;",
                "set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;",
                "set NODES:= D_NODES union O_NODES;",
                "param a_coord{NODES};",
                "param b_coord{NODES};",
                "param max_coord:=1000;",
                "set SLICES := 1 .. slice_number ordered;",
                "param sin{SLICES};",
                "param cos{SLICES};",
                "param M:= 3000;",
                "var new_a >=0 <= max_coord ;",
                "var new_b >=0 <= max_coord ;",
                "var a{NODES} ;",
                "var b{NODES} ;",
                "var z_1{NODES} >=0;",
                "var z_2{NODES} >=0;",
                "var y{NODES} binary;",
                "var x{NODES} binary;",
                "var BinSlice{NODES,SLICES} binary;",
                "var Z{NODES} >=0;",
                "var Z_max_des >=0;",
                "var Z_min_ob >=0, <=1000000000*obnoxious_node_number;"]
    # big M has to be (2* max coord )*(sqrt 2)/2 + max dist which is max coord * sqrt 2 = 2*sqrt 2 * max coord

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " Z_max_des - Z_min_ob;"]
        # " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"
        # " sum{k in D_NODES}Z[k]- Z_min_ob;"
        # "Z_max_des - sum{k in O_NODES}Z[k];"

    def data_cont(self):
        set_data_dict = {}
        param_data_dict = {"desirable_node_number": len(self.Instance.desirable_dict),
                           "obnoxious_node_number": len(self.Instance.obnoxious_dict),
                           "slice_number": self.slices,
                           "sin": self.sin_dict,
                           "cos": self.cos_dict,
                           "a_coord": self.Instance.node_coord_a_dict,
                           "b_coord": self.Instance.node_coord_b_dict}
        return set_data_dict, param_data_dict

    @staticmethod
    def const_cont():
        return [
                "subject to EUCL{k in NODES, s in SLICES}: Z[k] >= a[k]*sin[s] +  b[k]*cos[s] ;",
                "subject to EUCL2{k in O_NODES, s in SLICES}: Z[k] <= a[k]*sin[s] +  b[k]*cos[s] +M*(1-BinSlice[k,s]);",
                "subject to EUCL3{k in O_NODES}: sum{s in SLICES}BinSlice[k,s]=1;",

                "subject to A_Diff{k in NODES}: a[k] = a_coord[k] - new_a ;",
                "subject to B_Diff{k in NODES}: b[k] = b_coord[k] - new_b ;",

                "subject to ZMAX{k in D_NODES}: Z_max_des >= Z[k] ;",
                "subject to ZMIN{k in O_NODES}: Z_min_ob <= Z[k] ;"]


class ChinaDesiredSumObnoxiousSumModel(ChinaDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"]


class ChinaDesiredSumObnoxiousMinModel(ChinaDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "sum{k in D_NODES}Z[k]- Z_min_ob;"]
        # "Z_max_des - sum{k in O_NODES}Z[k];"


class ChinaDesiredMaxObnoxiousSumModel(ChinaDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "Z_max_des - sum{k in O_NODES}Z[k];"]


########################################################################################################################
########################################################################################################################
#
# hybrid
#
# Mine
#
########################################################################################################################
########################################################################################################################


class HybridDesiredMaxObnoxiousMinModel(Model):
    def __init__(self, instance, approx_lvl_integer):
        Model.__init__(self, instance, approx_lvl_integer)


    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " Z_max_des - Z_min_ob;"]
        # " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"
        # " sum{k in D_NODES}Z[k]- Z_min_ob;"
        # "Z_max_des - sum{k in O_NODES}Z[k];"

    def data_cont(self):
        set_data_dict = {}
        param_data_dict = {"desirable_node_number": len(self.Instance.desirable_dict),
                           "obnoxious_node_number": len(self.Instance.obnoxious_dict),
                           "approx_level_integer": self.approx_lvl_integer,
                           "slice_number": self.slices,
                           "sin": self.sin_dict,
                           "cos": self.cos_dict,
                           "a_coord": self.Instance.node_coord_a_dict,
                           "b_coord": self.Instance.node_coord_b_dict,
                           "q": self.q_dict}
        return set_data_dict, param_data_dict


    @staticmethod
    def var_cont():
        return ["new_a", "new_b", "a", "b", "z_1", "z_2", "y", "x", "Z"]

    @staticmethod
    def def_cont():
        return ["param desirable_node_number;",
                "param obnoxious_node_number;",
                "param node_number:=desirable_node_number + obnoxious_node_number ;",
                "param approx_level_integer ;",
                "param slice_number ;",
                "set SLICES := 1 .. slice_number ordered;",
                "param sin{SLICES};",
                "param cos{SLICES};",
                "set D_NODES:= 1 .. desirable_node_number;",
                "set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;",
                "set NODES:= D_NODES union O_NODES;",
                "param a_coord{NODES};",
                "param b_coord{NODES};",
                "param max_coord:=1000;",
                "set Levels := 1 .. approx_level_integer ordered;",
                "set Levels_Z := 0 .. approx_level_integer ordered;",
                "param q{Levels};",
                "param M:= 2000;",
                "var new_a >=0, <= max_coord ;",
                "var new_b >=0, <= max_coord ;",
                "var a{NODES} ;",
                "var b{NODES} ;",
                "var z_1{NODES,Levels_Z} >=0;",
                "var z_2{NODES,Levels_Z} >=0;",
                "var y{NODES,Levels_Z} binary;",
                "var x{NODES,Levels_Z} binary;",
                "var Z{NODES} >=0;",
                "var Z_max_des >=0;",
                "var Z_min_ob >=0, <=1000000000*obnoxious_node_number;"
                ]

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " Z_max_des - Z_min_ob;"]
        # " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"
        # " sum{k in D_NODES}Z[k]- Z_min_ob;"
        # "Z_max_des - sum{k in O_NODES}Z[k];"

    @staticmethod
    def const_cont():
        return ["subject to A_Diff{k in NODES}: a[k] = a_coord[k] - new_a ;",
                "subject to B_Diff{k in NODES}: b[k] = b_coord[k] - new_b ;",
                "subject to INIT_11{k in O_NODES}: z_1[k,0] >= a[k]  ;",
                "subject to INIT_12{k in O_NODES}: z_1[k,0] <= a[k] + x[k,0]*M;",
                "subject to INIT_13{k in O_NODES}: z_1[k,0] >= -a[k] ;",
                "subject to INIT_14{k in O_NODES}: z_1[k,0] <= -a[k] +(1-x[k,0])*M;",
                "subject to INIT_21{k in O_NODES}: z_2[k,0] >= b[k] ;",
                "subject to INIT_22{k in O_NODES}: z_2[k,0] <= b[k] + y[k,0] *M;",
                "subject to INIT_23{k in O_NODES}: z_2[k,0] >= -b[k] ;",
                "subject to INIT_24{k in O_NODES}: z_2[k,0] <= -b[k] +(1-y[k,0])*M;",

                "subject to ABS_11{k in O_NODES,i in Levels}: z_1[k,i]>=z_1[k,i-1] - z_2[k,i-1] ;",
                "subject to ABS_12{k in O_NODES,i in Levels}: z_1[k,i]<=z_1[k,i-1] - z_2[k,i-1] +(1 - y[k,i])*M ;",
                "subject to ABS_13{k in O_NODES,i in Levels}: z_1[k,i]>=z_2[k,i-1] - z_1[k,i-1] ;",
                "subject to ABS_14{k in O_NODES,i in Levels}: z_1[k,i]<=z_2[k,i-1] - z_1[k,i-1] +y[k,i]*M;",

                "subject to MIN_11{k in O_NODES,i in Levels}: z_2[k,i]<=q[i] * z_1[k,i-1];",
                "subject to MIN_13{k in O_NODES,i in Levels}: z_2[k,i]<=q[i] * z_2[k,i-1] ;",

                "subject to EUCL_O{k in O_NODES}: Z[k] = z_1[k,last(Levels)] +  z_2[k,last(Levels)] ;",

                "subject to ZMIN{k in O_NODES}: Z_min_ob <= Z[k] ;",

                "subject to EUCL_D{k in D_NODES, s in SLICES}: Z[k] >= a[k]*sin[s] +  b[k]*cos[s] ;",
                "subject to ZMAX{k in D_NODES}: Z_max_des >= Z[k] ;"]

class HybridDesiredSumObnoxiousSumModel(ChinaDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"]


class HybridDesiredSumObnoxiousMinModel(ChinaDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "sum{k in D_NODES}Z[k]- Z_min_ob;"]
        # "Z_max_des - sum{k in O_NODES}Z[k];"


class HybridDesiredMaxObnoxiousSumModel(ChinaDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "Z_max_des - sum{k in O_NODES}Z[k];"]

########################################################################################################################
########################################################################################################################
#
# Multi Depot
#
# Mine
#
########################################################################################################################
########################################################################################################################


class MultiDesiredMaxObnoxiousMinModel(Model):
    def __init__(self, instance, approx_lvl_integer):
        Model.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def var_cont():
        return ["new_a", "new_b", "a", "b", "z_1", "z_2", "y", "x", "Z", "B","Z_max_des","Z_min_ob"]

    @staticmethod
    def def_cont():
        return ["param facility_node_number;"
                "param desirable_node_number;",
                "param obnoxious_node_number;",
                "param node_number:=desirable_node_number + obnoxious_node_number ;",
                "param approx_level_integer ;",
                "set D_NODES:= 1 .. desirable_node_number;",
                "set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;",
                "set F_NODES:= 101 .. 100+facility_node_number; ",
                "set NODES:= D_NODES union O_NODES;",
                "param a_coord{NODES};",
                "param b_coord{NODES};",
                "param max_coord:=1000;",
                "set Levels := 1 .. approx_level_integer ordered;",
                "set Levels_Z := 0 .. approx_level_integer ordered;",
                "param q{Levels};",
                "param M:= 1500;",
                "var new_a{F_NODES} >=0, <= max_coord ;",
                "var new_b{F_NODES} >=0, <= max_coord ;",
                "var a{F_NODES,NODES} ;",
                "var b{F_NODES,NODES} ;",
                "var z_1{F_NODES,NODES,Levels_Z} >=0;",
                "var z_2{F_NODES,NODES,Levels_Z} >=0;",
                "var y{F_NODES,NODES,Levels_Z} binary;",
                "var x{F_NODES,NODES,Levels_Z} binary;",
                "var Z{F_NODES,NODES} >=0;",
                "var Z_max_des >=0;",
                "var Z_min_ob >=0, <=1000000000*obnoxious_node_number;"
                "var B{F_NODES,D_NODES} binary;"]

    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "Z_max_des+  Z_min_ob;"]
        # " sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];"
        # " sum{k in D_NODES}Z[k]- Z_min_ob;"
        # "Z_max_des - sum{k in O_NODES}Z[k];"

    @staticmethod
    def const_cont():
        return ["subject to INIT_11{f in F_NODES,k in NODES}: z_1[f,k,0] >= a[f,k]  ;",
                "subject to INIT_12{f in F_NODES,k in O_NODES}: z_1[f,k,0] <= a[f,k] + x[f,k,0]*M;",
                "subject to INIT_13{f in F_NODES,k in NODES}: z_1[f,k,0] >= -a[f,k] ;",
                "subject to INIT_14{f in F_NODES,k in O_NODES}: z_1[f,k,0] <= -a[f,k] +(1-x[f,k,0])*M;",
                "subject to INIT_21{f in F_NODES,k in NODES}: z_2[f,k,0] >= b[f,k] ;",
                "subject to INIT_22{f in F_NODES,k in O_NODES}: z_2[f,k,0] <= b[f,k] + y[f,k,0] *M;",
                "subject to INIT_23{f in F_NODES,k in NODES}: z_2[f,k,0] >= -b[f,k] ;",
                "subject to INIT_24{f in F_NODES,k in O_NODES}: z_2[f,k,0] <= -b[f,k] +(1-y[f,k,0])*M;",

                "subject to ABS_11{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]>=z_1[f,k,i-1] - z_2[f,k,i-1] ;",
                "subject to ABS_12{f in F_NODES,k in O_NODES,i in Levels}: z_1[f,k,i]<=z_1[f,k,i-1] - z_2[f,k,i-1] +(1 - y[f,k,i])*M ;",
                "subject to ABS_13{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]>=z_2[f,k,i-1] - z_1[f,k,i-1] ;",
                "subject to ABS_14{f in F_NODES,k in O_NODES,i in Levels}: z_1[f,k,i]<=z_2[f,k,i-1] - z_1[f,k,i-1] +y[f,k,i]*M;",

                "subject to MIN_11{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]<=q[i] * z_1[f,k,i-1];",
                "subject to MIN_12{f in F_NODES,k in D_NODES,i in Levels}: z_2[f,k,i]>=q[i] * z_1[f,k,i-1] - y[f,k,i]*M ;",
                "subject to MIN_13{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]<=q[i] * z_2[f,k,i-1] ;",
                "subject to MIN_14{f in F_NODES,k in D_NODES,i in Levels}: z_2[f,k,i]>=q[i] * z_2[f,k,i-1] - (1 - y[f,k,i])*M ;",
                "subject to MIN_15{f in F_NODES,k in D_NODES,i in Levels}: z_2[f,k,i-1] - z_1[f,k,i-1] >=0 - y[f,k,i]*M ;",

                "subject to EUCL{f in F_NODES,k in NODES}: Z[f,k] = z_1[f,k,last(Levels)] +  z_2[f,k,last(Levels)] ;",

                "subject to A_Diff{f in F_NODES,k in NODES}: a[f,k] = a_coord[k] - new_a[f] ;",
                "subject to B_Diff{f in F_NODES,k in NODES}: b[f,k] = b_coord[k] - new_b[f] ;",

                "subject to ZMAX{f in F_NODES,k in D_NODES}: Z_max_des >= Z[f,k] - M*(1-B[f,k]) ;",
                "subject to ZMIN{f in F_NODES,k in O_NODES}: Z_min_ob <= Z[f,k] ;",

                "subject to OneFactory{k in D_NODES}: sum{f in F_NODES} B[f,k]=1;"]


    def data_cont(self):
        set_data_dict = {}
        param_data_dict = {"facility_node_number": self.Instance.facility_numb,
                           "desirable_node_number": len(self.Instance.desirable_dict),
                           "obnoxious_node_number": len(self.Instance.obnoxious_dict),
                           "approx_level_integer": self.approx_lvl_integer,
                           "a_coord": self.Instance.node_coord_a_dict,
                           "b_coord": self.Instance.node_coord_b_dict,
                           "q": self.q_dict}
        return set_data_dict, param_data_dict

class MultiDesiredSumObnoxiousSumModel(MultiDesiredMaxObnoxiousMinModel):
    def __init__(self, instance, approx_lvl_integer):
        DesiredMaxObnoxiousMinModel.__init__(self, instance, approx_lvl_integer)

    @staticmethod
    def const_cont():
        return ["subject to INIT_11{f in F_NODES,k in NODES}: z_1[f,k,0] >= a[f,k]  ;",
                "subject to INIT_12{f in F_NODES,k in O_NODES}: z_1[f,k,0] <= a[f,k] + x[f,k,0]*M;",
                "subject to INIT_13{f in F_NODES,k in NODES}: z_1[f,k,0] >= -a[f,k] ;",
                "subject to INIT_14{f in F_NODES,k in O_NODES}: z_1[f,k,0] <= -a[f,k] +(1-x[f,k,0])*M;",
                "subject to INIT_21{f in F_NODES,k in NODES}: z_2[f,k,0] >= b[f,k] ;",
                "subject to INIT_22{f in F_NODES,k in O_NODES}: z_2[f,k,0] <= b[f,k] + y[f,k,0] *M;",
                "subject to INIT_23{f in F_NODES,k in NODES}: z_2[f,k,0] >= -b[f,k] ;",
                "subject to INIT_24{f in F_NODES,k in O_NODES}: z_2[f,k,0] <= -b[f,k] +(1-y[f,k,0])*M;",

                "subject to ABS_11{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]>=z_1[f,k,i-1] - z_2[f,k,i-1] ;",
                "subject to ABS_12{f in F_NODES,k in O_NODES,i in Levels}: z_1[f,k,i]<=z_1[f,k,i-1] - z_2[f,k,i-1] +(1 - y[f,k,i])*M ;",
                "subject to ABS_13{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]>=z_2[f,k,i-1] - z_1[f,k,i-1] ;",
                "subject to ABS_14{f in F_NODES,k in O_NODES,i in Levels}: z_1[f,k,i]<=z_2[f,k,i-1] - z_1[f,k,i-1] +y[f,k,i]*M;",

                "subject to MIN_11{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]<=q[i] * z_1[f,k,i-1];",
                "subject to MIN_12{f in F_NODES,k in D_NODES,i in Levels}: z_2[f,k,i]>=q[i] * z_1[f,k,i-1] - y[f,k,i]*M ;",
                "subject to MIN_13{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]<=q[i] * z_2[f,k,i-1] ;",
                "subject to MIN_14{f in F_NODES,k in D_NODES,i in Levels}: z_2[f,k,i]>=q[i] * z_2[f,k,i-1] - (1 - y[f,k,i])*M ;",
                "subject to MIN_15{f in F_NODES,k in D_NODES,i in Levels}: z_2[f,k,i-1] - z_1[f,k,i-1] >=0 - y[f,k,i]*M ;",

                "subject to EUCL{f in F_NODES,k in D_NODES}: Z[f,k] >= z_1[f,k,last(Levels)] +  z_2[f,k,last(Levels)] -M*(1-B[f,k]);",
                "subject to EUCL2{f in F_NODES,k in O_NODES}: Z[f,k] = z_1[f,k,last(Levels)] +  z_2[f,k,last(Levels)] ;",

                "subject to A_Diff{f in F_NODES,k in NODES}: a[f,k] = a_coord[k] - new_a[f] ;",
                "subject to B_Diff{f in F_NODES,k in NODES}: b[f,k] = b_coord[k] - new_b[f] ;",

                "subject to ZMAX{f in F_NODES,k in D_NODES}: Z_max_des >= Z[f,k] ;",
                "subject to ZMIN{f in F_NODES,k in O_NODES}: Z_min_ob <= Z[f,k] ;",

                "subject to OneFactory{k in D_NODES}: sum{f in F_NODES} B[f,k]=1;"]


    @staticmethod
    def goal_cont():
        return ["minimize GF:",
                "sum{f in F_NODES,k in D_NODES} Z[f,k] -  Z_min_ob;"]