from math import sqrt
import os








































class Model(object):

    def __init__(self, approx_level_integer, instance):  # goals 1 fermat weber  bzw summe        2 centerproblem
        directory = os.getcwd()
        self.approx_level_integer = approx_level_integer
        self.Instance = instance
        self.desirable_node_number = len( self.Instance.desirable_dict)
        self.obnoxious_node_number = len( self.Instance.obnoxious_dict)
        self.var_name_array = ["new_a","new_b","a", "b", "z_1", "z_2", "y", "x", "Z","Zb"]
        self.obj_string = "GF"
        self.ModString()
        self.DatString()

    def Approx_Constr(self):
        approx_const_string = "subject to INIT_11{f in F_NODES,k in NODES}: z_1[f,k,0] >= a[f,k]  ;\n "  # initialisierung der ersten ebene damit haetten wir manhatten Norm
        approx_const_string += "subject to INIT_12{f in F_NODES,k in NODES}: z_1[f,k,0] <= a[f,k] + x[f,k,0]*M;\n"
        approx_const_string += "subject to INIT_13{f in F_NODES,k in NODES}: z_1[f,k,0] >= -a[f,k] ;\n"
        approx_const_string += "subject to INIT_14{f in F_NODES,k in NODES}: z_1[f,k,0] <= -a[f,k] +(1-x[f,k,0])*M;\n"
        approx_const_string += "subject to INIT_21{f in F_NODES,k in NODES}: z_2[f,k,0] >= b[f,k] ;\n"
        approx_const_string += "subject to INIT_22{f in F_NODES,k in NODES}: z_2[f,k,0] <= b[f,k] + y[f,k,0] *M;\n"
        approx_const_string += "subject to INIT_23{f in F_NODES,k in NODES}: z_2[f,k,0] >= -b[f,k] ;\n"
        approx_const_string += "subject to INIT_24{f in F_NODES,k in NODES}: z_2[f,k,0] <= -b[f,k] +(1-y[f,k,0])*M;\n"

        approx_const_string += "subject to ABS_01{f in F_NODES,k in NODES}:a[f,k]>=0 - x[f,k,0] *M;\n"
        approx_const_string += "subject to ABS_02{f in F_NODES,k in NODES}:-a[f,k]>=0 - (1-x[f,k,0])*M;\n"
        approx_const_string += "subject to ABS_03{f in F_NODES,k in NODES}:b[f,k]>=0 - y[f,k,0] *M;\n"
        approx_const_string += "subject to ABS_04{f in F_NODES,k in NODES}:-b[f,k]>=0 - (1-y[f,k,0])*M;\n"

        approx_const_string += "subject to ABS_11{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]>=z_1[f,k,i-1] - z_2[f,k,i-1] ;\n"  # rekursiver Aufbau der Betragsfunktion f'_i
        approx_const_string += "subject to ABS_12{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]<=z_1[f,k,i-1] - z_2[f,k,i-1] +(1 - y[f,k,i])*M ;\n"
        approx_const_string += "subject to ABS_13{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]>=z_2[f,k,i-1] - z_1[f,k,i-1] ;\n"
        approx_const_string += "subject to ABS_14{f in F_NODES,k in NODES,i in Levels}: z_1[f,k,i]<=z_2[f,k,i-1] - z_1[f,k,i-1] +y[f,k,i]*M;\n"

        approx_const_string += "subject to MIN_11{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]<=q[i] * z_1[f,k,i-1];\n"  # rekursiver Aufbau der Minimumfunktion f''_i

        approx_const_string += "subject to MIN_12{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]>=q[i] * z_1[f,k,i-1] - y[f,k,i]*M ;\n"  # geaendert man kann den binaeren teil auch noch dran hauen an die <= restriktionen
        approx_const_string += "subject to MIN_13{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]<=q[i] * z_2[f,k,i-1] ;\n"  # besser jeder test war laufzeit technisch wesentlich performanter (haette ich so nicht erwartet)
        approx_const_string += "subject to MIN_14{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i]>=q[i] * z_2[f,k,i-1] - (1 - y[f,k,i])*M ;\n"  # ueberall durchgefuehrt im test faktor 30 schneller

        approx_const_string += "subject to MIN_15{f in F_NODES,k in NODES,i in Levels}: z_2[f,k,i-1] - z_1[f,k,i-1] >=0 - y[f,k,i]*M ;\n"   #Schalter fuer y_i binary variable der Minimumfunktion f''_i
        # ("subject to MIN_16{f in F_NODES,k in NODES,i in Levels}: z_1[k,i-1] - z_2[k,i-1] >= 0 - (1 - y[k,i])*M ;\n") #vermutlich ueflue durch ABS 11-14

        approx_const_string += "subject to EUCL{f in F_NODES,k in NODES}: Z[f,k] = z_1[f,k,%s] +  z_2[f,k,%s] ;\n" % (
            self.approx_level_integer, self.approx_level_integer)  # Approximierter Wert fuer euklidische Entfernung
        return approx_const_string

    def Other_Constr(self):
        other_const_string = ""
        if self.Instance.d_goal == "MinMax":
            other_const_string += "subject to ZMAX{k in D_NODES,f in F_Nodes}: Z_max_des >= Z[f,k]-(1-Zb[f,k])*M  ;\n"  # Maximum der erwuenschten Entfernungen
            self.var_name_array.append("Z_max_des")#todo now it minimizes the max distance for all distances possible would also be the sum of the maxima
        if self.Instance.o_goal == "MaxMin" and self.obnoxious_node_number != 0:
            other_const_string += "subject to ZMIN{k in O_NODES}: Z_min_ob <= Z[k] ;\n"#todo  # Minimum der unerwuenschten Entfernungen
            self.var_name_array.append("ZMIN")
        other_const_string += "end;\n"
        return other_const_string

    def ChainRoots(self, root_integer=2):
        i = 1
        q_list = []
        q_i = 0
        while i <= self.approx_level_integer:
            q_i = sqrt(q_i + 2)
            q_list.append(q_i)
            i = i + 1
        return q_list

    def Coord_Diffs(self):
        coord_dif_string = "subject to A_Diff{f in F_NODES,k in D_NODES}: a[f,k] >= a_coord[k] - new_a[f] - M*(1-Zb[f,k]);\n"  # Approximierter Wert fuer euklidische Entfernung
        coord_dif_string += "subject to A_Diff_2{f in F_NODES,k in D_NODES}: a[f,k] <= a_coord[k] - new_a[f] + M*(1-Zb[f,k]);\n"  # Approximierter Wert fuer euklidische Entfernung
        coord_dif_string += "subject to B_Diff{f in F_NODES,k in D_NODES}: b[f,k] >= b_coord[k] - new_b[f] - M*(1-Zb[f,k]);\n"
        coord_dif_string += "subject to B_Diff_2{f in F_NODES,k in D_NODES}: b[f,k] <= b_coord[k] - new_b[f] + M*(1-Zb[f,k]);\n"

        coord_dif_string += "subject to A_Diff_obnoxious{f in F_NODES,k in O_NODES}: a[f,k] >= a_coord[k] - new_a[f];\n"  # Approximierter Wert fuer euklidische Entfernung
        coord_dif_string += "subject to A_Diff_obnoxious2{f in F_NODES,k in O_NODES}: a[f,k] <= a_coord[k] - new_a[f];\n"  # Approximierter Wert fuer euklidische Entfernung
        coord_dif_string += "subject to B_Diff_obnoxious{f in F_NODES,k in O_NODES}: b[f,k] >= b_coord[k] - new_b[f];\n"
        coord_dif_string += "subject to B_Diff_obnoxious2{f in F_NODES,k in O_NODES}: b[f,k] <= b_coord[k] - new_b[f];\n"

        coord_dif_string += "subject to Matching{k in NODES}: sum{f in F_NODES}Zb[f,k]=1;\n"


        return coord_dif_string

    def Defs(self):
        def_string =  "param desirable_node_number;\n"
        def_string += "param obnoxious_node_number;\n"
        def_string += "param facility_node_number;\n"
        def_string += "param node_number:=desirable_node_number + obnoxious_node_number ;\n"
        def_string += "param approx_level_integer ;\n"
        def_string += "set D_NODES:= 1 .. desirable_node_number;\n"
        def_string += "set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;\n"
        def_string += "set NODES:= D_NODES union O_NODES;\n"
        def_string += "set F_NODES:= 1 .. facility_node_number;\n"
        def_string += "param a_coord{NODES};\n"
        def_string += "param b_coord{NODES};\n"

        def_string += "set Levels := 1 .. approx_level_integer;\n"
        def_string += "set Levels_Z := 0 .. approx_level_integer;\n"
        def_string += "param q{Levels};\n"
        def_string += "param M:= 2000;\n"
        def_string += "var new_a{F_NODES} >=0 <= %s ;\n" %(self.Instance.max_coord)
        def_string += "var new_b{F_NODES} >=0 <= %s ;\n" %(self.Instance.max_coord)

        def_string += "var a{F_NODES,NODES} ;\n"
        def_string += "var b{F_NODES,NODES} ;\n"
        def_string += "var z_1{F_NODES,NODES,Levels_Z} >=0;\n"
        def_string += "var z_2{F_NODES,NODES,Levels_Z} >=0;\n"
        def_string += "var y{F_NODES,NODES,Levels_Z} binary;\n"
        def_string += "var x{F_NODES,NODES,Levels_Z} binary;\n"
        def_string += "var Z{F_NODES,NODES} >=0;\n"
        def_string += "var Zb{F_NODES,NODES} binary;"

        if self.Instance.d_goal == "MinMax":
            def_string += "var Z_max_des >=0;\n"

        if self.Instance.o_goal == "MaxMin" and self.obnoxious_node_number != 0:
            def_string += "var Z_min_ob >=0;\n"

        return def_string

    def Goal_Func(self):  # todo
        gf_string = "minimize GF:"
        if self.Instance.d_goal == "":
            gf_string = gf_string
        elif self.Instance.d_goal == "MinSum":
            gf_string = gf_string + " sum{f in F_NODES,k in D_NODES}Z[f,k]"
        elif self.Instance.d_goal == "MinMax":
            gf_string = gf_string + " Z_max_des"
        if self.Instance.o_goal == "" or self.obnoxious_node_number == 0:
            gf_string = gf_string
        elif self.Instance.o_goal == "MaxSum":
            gf_string = gf_string + " -sum{f in F_NODES,k in O_NODES}Z[f,k]"
        elif self.Instance.o_goal == "MaxMin":
            gf_string = gf_string + " - Z_min_ob"
        gf_string = gf_string + ";\n"
        return gf_string

    def BarrierConstraints(self):
        pass

    def ModString(self):
        self.mod_string = self.Defs()+"\n"
        self.mod_string += self.Goal_Func()
        self.mod_string += self.Coord_Diffs()
        self.mod_string += self.Approx_Constr()
        self.mod_string += self.Other_Constr()

        return self.mod_string

    def DatString(self):
        self.dat_string = "param desirable_node_number := %s;\n" % (self.desirable_node_number)
        self.dat_string += "param obnoxious_node_number := %s;\n" % (self.obnoxious_node_number)
        self.dat_string += "param facility_node_number := %s;\n" % (self.Instance.facility_numb)
        self.dat_string += "param approx_level_integer := %s ;\n" % (self.approx_level_integer)
        a_string = ""
        b_string = ""
        for node in  self.Instance.desirable_dict:
            a_string = a_string + str(node) + " %s " % ( self.Instance.desirable_dict[node][0])
        for node in  self.Instance.obnoxious_dict:
            a_string = a_string + str(node) + " %s " % ( self.Instance.obnoxious_dict[node][0])
        self.dat_string += "param a_coord:=%s;\n" % (a_string)
        for node in  self.Instance.desirable_dict:
            b_string = b_string + str(node) + " %s " % ( self.Instance.desirable_dict[node][1])
        for node in  self.Instance.obnoxious_dict:
            b_string = b_string + str(node) + " %s " % ( self.Instance.obnoxious_dict[node][1])
        self.dat_string += "param b_coord:=%s;\n" % (b_string)

        q_list = self.ChainRoots(2)
        i = 1
        q_string = ""
        for q_i in q_list:
            q_string = q_string + str(i) + " " + str(q_i) + " "
            i = i + 1
        self.dat_string += "param q:= %s ;\n" % (q_string)
        return self.dat_string
