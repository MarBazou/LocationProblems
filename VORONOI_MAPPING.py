
'''
Created on 30.05.2017

modularisierung dh ausgliedern von Funktionen

attractive points

umstellen der sicht per button auf display

schnittpolytope

optimalloesungen berechnen

@author: Markus
'''
import math
import time

# x = pg.init()
from math import sqrt

disp_x = 1000
disp_y = 1000

class DC_Problem(object):
    def __init__(self, repulsive_nodes_list, attractive_nodes_list):
        self.x_vec=Vector(1,0)
        self.repulsive_nodes_list = self.CreatenodeObjs(repulsive_nodes_list, RepNode)
        self.attractive_nodes_list = self.CreatenodeObjs(attractive_nodes_list, AtrNode)
        self.rep_cut_lines = self.GetCutLineToNodes(self.repulsive_nodes_list)
        self.atr_cut_lines = self.GetCutLineToNodes(self.attractive_nodes_list)
        self.CalculateAllPolarAngles(self.repulsive_nodes_list)
        self.CalculateAllPolarAngles(self.attractive_nodes_list)#fertig
        self.SortNodes(self.repulsive_nodes_list)
        self.SortNodes(self.attractive_nodes_list)


        #self.repulsive_polytope_list = self.GetRepPolytopes()
        #self.attractive_polytope_list = self.GetAtrPolytopes()
        #self.cut_polytope_list = self.GetCutPolytopes()

    def CreatenodeObjs(self, node_list, node_Type):#erstellt Listen von Knoten des mitgegebenen Typs
        node_obj_list = []
        for node in node_list:
            node_obj_list.append(node_Type(node[0], node[1]))
        return node_obj_list

    def GetCutLineToNodes(self,nodes_list):#Erstellt Cutlines zwischen zwei Knoten und sortiert die Cutlines den Knoten zu
        cut_lines=[]
        for i in range(len(nodes_list)):
            node_A=nodes_list[i]
            for j in range(len(nodes_list)):
                node_B=nodes_list[j]
                if i < j:
                    cut_line=Cut_Line(node_A,node_B)
                    node_A.belonging_cutlines.append(cut_line)
                    node_B.belonging_cutlines.append(cut_line)
                    cut_lines.append(cut_line)
        return cut_lines

    def CalculateAllPolarAngles(self,node_list):#fertig
        for node_A in node_list:
            for node_B in node_list:
                if node_A!=node_B:
                    diff_vec=Vector(node_B.x-node_A.x,node_B.y-node_A.y)
                    angle=self.CalcPolarAngle(diff_vec)
                    node_A.angle_to_other_nodes_dict[node_B]=angle

    def SortNodes(self,node_list):#fertig
        for node in node_list:
            node.SortNodesByAngle()

    def CalcPolarAngle(self,vec):#fertig #calculates the polar angle of an vector. so thatit is increasing counter clockwise
        scalar_prod=self.x_vec.x*vec.x+self.x_vec.y*vec.y
        length_prod=self.x_vec.length*vec.length
        alpha=math.acos(scalar_prod/length_prod)
        alpha=alpha/(2*math.pi)*360
        if vec.y<0:
            alpha=360-alpha
        return alpha

    def RepulsiveVoronoi(self):
        self.  (self.repulsive_nodes_list)

    def CalculateVoronoiMap(self,node_list):#todo
        pass









########################################################



    def GetRepPolytopes(self):
        polytope_list = []
        for repulsive_node in self.repulsive_nodes_list:
            allowed_node_dict = {}
            for line in self.line_to_rep_node_dict[repulsive_node]:
                allowed_node_dict[line] = repulsive_node
            polytope_list.append(
                CreatePolytope(self.line_to_rep_node_dict[repulsive_node], allowed_node_dict, repulsive_node, True, None))
        return polytope_list

    def GetAtrPolytopes(self):
        polytope_list = []
        for node in self.attractive_nodes_list:
            allowed_node_dict = {}
            attractive_node = node
            for line in self.line_to_atr_node_dict[node]:
                allowed_node_dict[line] = attractive_node
            polytope_list.append(
                CreatePolytope(self.line_to_atr_node_dict[node], allowed_node_dict, attractive_node, False, None))
        return polytope_list

    def GetCutPolytopes(self):
        polytope_list = []
        for atr_poly in self.attractive_polytope_list:
            for rep_poly in self.repulsive_polytope_list:
                # cut_poly_nodes=atr_poly.node_list+rep_poly.node_list
                allowed_node_dict = self.GetAllowednodeDictForCutPoly(atr_poly, rep_poly)
                cut_poly_list = atr_poly.line_list + rep_poly.line_list
                polytope_list.append(CreatePolytope(cut_poly_list, allowed_node_dict, None, False,
                                                  (atr_poly.reference_node, rep_poly.reference_node)))
        return polytope_list




class Node(object):
    def __init__(self, x_koord, y_koord):
        self.x = x_koord
        self.y = y_koord
        self.angle_to_other_nodes_dict={}
        self.angle_sorted_nodes=[]

    def SortNodesByAngle(self):#fertig
        self.angle_sorted_nodes=list(self.angle_to_other_nodes_dict.keys())
        self.angle_sorted_nodes.sort(key=lambda x: self.angle_to_other_nodes_dict[x])

class IntersecNode(Node):
    def __init__(self,x_koord,y_koord,line_a,line_b):
        Node.__init__(self,x_koord,y_koord)
        self.intersec_line_a=line_a
        self.intersec_line_b=line_b
        self.belonging_cutlines=[]

class AtrNode(Node):
    def __init__(self,x_koord,y_koord):
        Node.__init__(self,x_koord,y_koord)
        self.belonging_cutlines=[]

class RepNode(Node):
    def __init__(self,x_koord,y_koord):
        Node.__init__(self,x_koord,y_koord)
        self.belonging_cutlines=[]
        self.bounded=None

    def CheckIfBoundedVPolytope(self):
        for i in range(len(self.angle_sorted_nodes)):
            if i!=len(self.angle_sorted_nodes):
                angle_diff=self.angle_to_other_nodes_dict[self.angle_sorted_nodes[i+1]]-self.angle_to_other_nodes_dict[self.angle_sorted_nodes[i]]
                node_A=self.angle_sorted_nodes[i]
                node_B=self.angle_sorted_nodes[i+1]
            else:
                angle_diff=360-self.angle_to_other_nodes_dict[self.angle_sorted_nodes[i]]+self.angle_to_other_nodes_dict[self.angle_sorted_nodes[0]]
                node_A = self.angle_sorted_nodes[i]
                node_B = self.angle_sorted_nodes[0]
            if angle_diff>=180:
                return False,node_A, node_B
            else:
                return True

    def CalcVPolytope(self):
        line_segs=[]
        self.all_lines_to_skip=[]
        for node in self.angle_sorted_nodes:
            if node != self.angle_sorted_nodes[-1]:
                prev_node=self.angle_sorted_nodes[self.angle_sorted_nodes.index[node]-1]
                next_node=self.angle_sorted_nodes[self.angle_sorted_nodes.index[node]+1]
            else:
                break
            act_line, next_line, prev_line=self.FindRelevantLine(node,prev_node,next_node)
            if act_line in self.all_lines_to_skip:
                continue
            line_seg, lines_to_skip=self.CalcVPolytopeLineSegment(act_line,next_line,prev_line)
            self.all_lines_to_skip+=lines_to_skip
            line_segs.append(line_seg) #todo hier weiter und alles kommentieren


    def CalcVPolytopeLineSegment(self,act_line,next_line,prev_line):
        lines_to_skip=[]
        prev_intersec_node = GetLineIntersection(act_line, prev_line)
        next_intersec_node = GetLineIntersection(act_line, next_line)
        for line in self.belonging_cutlines:
            if line != act_line and line !=next_line and line != prev_line and line not in self.all_lines_to_skip:
                new_intersec_node=GetLineIntersection(line,act_line)
                if WithinRectangle(prev_intersec_node,next_intersec_node, new_intersec_node):
                    between_prev_line=self.IsLineBetweenNodeAndLine(prev_line,line)
                    if between_prev_line:
                        lines_to_skip.append(prev_line)
                        prev_line=line
                        prev_intersec_node=new_intersec_node
                    else:
                        lines_to_skip.append(next_line)
                        next_line=line
                        next_intersec_node=new_intersec_node
        return Line_Segment(prev_intersec_node,next_intersec_node), lines_to_skip


    def IsLineBetweenNodeAndLine(self,line, line_to_test):
        lot=Line(line.start_point,self)
        test_line_intersec=GetLineIntersection(line_to_test,lot)
        return WithinRectangle(self,line.start_point,test_line_intersec)






    def FindRelevantLine(self,node,prev_node,next_node):
        for cut_line in self.belonging_cutlines:
            if cut_line.node_A == prev_node:
                prev_line = cut_line
            if cut_line.node_B == prev_node:
                prev_line = cut_line
            if cut_line.node_A == next_node:
                next_line = cut_line
            if cut_line.node_B == next_node:
                next_line = cut_line
            if cut_line.node_A == node:
                act_line = cut_line
            if cut_line.node_B == node:
                act_line = cut_line
        return act_line,next_line,prev_line




class Vector(object):
    def __init__(self,x_koord, y_koord,):
        self.x,self.y =x_koord, y_koord
        self.length = sqrt(self.x**2+self.y**2)

class Line(object): #node_A and node_B are two arbitrary but different points on the line
    def __init__(self, node_A,node_B):
        self.node_A=node_A
        self.node_B=node_B
        self.direct_vec, self.start_point = self.GetDirectAndStart()
        self.end=None
        self.start=None

    def GetDirectAndStart(self):
        x_diff = 1. * self.node_A.x - 1. * self.node_B.x
        y_diff = 1. * self.node_A.y - 1. * self.node_B.y
        return Vector(y_diff, x_diff), self.node_A

    def GetCompleteLine(self):
        if self.direct_vec.x != 0:
            self.end_x = disp_x
            self.start_x = 0
            self.end_y = (disp_x - self.start_point.x) / self.direct_vec.x * self.direct_vec.y + self.start_point.y
            self.start_y = (0 - self.start_point.x) / self.direct_vec.x * self.direct_vec.y + self.start_point.y
        else:
            self.end_x = self.start_point.x
            self.start_x = self.start_point.x
            self.end_y = disp_y
            self.start_y = 0
        self.end = Node(self.end_x, self.end_y,None)
        self.start = Node(self.start_x, self.start_y,None)

class Line_Segment(Line):#node_A and node_B are the end Points pf the Segment
    def __init__(self,node_A, node_B):
        Line.__init__(self,node_A, node_B)

class Cut_Line(Line):#node_A and node_B are the points orthogonal to the cut_line which lays centered between them
    def __init__(self, node_A, node_B):
        Line.__init__(self,node_A, node_B)
        self.end=None
        self.start=None

    def GetDirectAndStart(self):
        x_diff = 1. * self.node_A.x - 1. * self.node_B.x
        y_diff = 1. * self.node_A.y - 1. * self.node_B.y
        return Vector(-y_diff, x_diff), Node(1. * self.node_B.x + 0.5 * x_diff, self.node_B.y + 0.5 * y_diff)


class Polytope(object):
    def __init__(self, node_list, bounded, bounded_dict, line_list, allowed_nodes_dict, reference_node, repulsive=True,
                 cut_node_tuple=None, lines_to_corners_dict=None):
        self.node_list = node_list
        self.bounded = bounded
        self.bounded_dict = bounded_dict
        self.line_list = line_list
        self.allowed_nodes_dict = allowed_nodes_dict
        self.reference_node = reference_node
        self.repulsive = repulsive
        self.cut_node_tuple = cut_node_tuple
        self.lines_to_corners_dict = lines_to_corners_dict  #
        self.optimal_corner = None
        self.optimal_value = None
        self.show_a_r = False

def GetLineIntersection(line_A, line_B):
    if line_B.direct_vec.x != 0 and line_B.direct_vec.y != 0:

        if 1.0 * line_A.direct_vec.x / line_B.direct_vec.x != 1.0 * line_A.direct_vec.y / line_B.direct_vec.y:
            if line_A.direct_vec.y != 0:

                beta = 1.0 * (line_A.direct_vec.y * (line_A.start_point.x - line_B.start_point.x)
                              + line_A.direct_vec.x * (line_B.start_point.y - line_A.start_point.y)) / \
                       (1.0 * (line_B.direct_vec.x * line_A.direct_vec.y - line_B.direct_vec.y * line_A.direct_vec.x))

                x = line_B.start_point.x + beta * line_B.direct_vec.x
                y = line_B.start_point.y + beta * line_B.direct_vec.y
            else:
                alpha = (line_B.direct_vec.y * (line_B.start_point.x - line_A.start_point.x)
                         + line_B.direct_vec.x * (line_A.start_point.y - line_B.start_point.y)) / (
                                    line_A.direct_vec.x * line_B.direct_vec.y - line_A.direct_vec.y *
                                    line_B.direct_vec.x)
                x = line_A.start_point.x + alpha * line_A.direct_vec.x
                y = line_A.start_point.y
        else:
            return None
    elif line_B.direct_vec.x == 0 and line_A.direct_vec.x == 0:
        return None
    elif line_B.direct_vec.y == 0 and line_A.direct_vec.y == 0:
        return None
    elif line_B.direct_vec.y == 0 and line_B.direct_vec.x == 0:
        return None
    else:
        if line_A.direct_vec.y != 0:

            beta = (line_A.direct_vec.y * (line_A.start_point.x - line_B.start_point.x) + line_A.direct_vec.x * (
                        line_B.start_point.y - line_A.start_point.y)) / (
                               line_B.direct_vec.x * line_A.direct_vec.y - line_B.direct_vec.y * line_A.direct_vec.x)
            x = line_B.start_point.x + beta * line_B.direct_vec.x
            y = line_B.start_point.y + beta * line_B.direct_vec.y
        else:
            alpha = (line_B.direct_vec.y * (line_B.start_point.x - line_A.start_point.x)) / (
                                line_A.direct_vec.x * line_B.direct_vec.y)
            x = line_B.start_point.x
            y = line_A.start_point.y
    return IntersecNode(x, y,line_A,line_B)


def WithinRectangle(node_a,node_b,node_to_test):
    if min(node_a.x,node_b.x)<=node_to_test.x<=max(node_a.x,node_b.x) and min(node_a.y,node_b.y)<=node_to_test.y<=max(node_a.y,node_b.y):
        return True
    else:
        return False

if __name__=="__main__":
    repulsive_nodes_list=[(5,500),(400,30),(700,600)]
    attractive_nodes_list=[(200,200),(200,100),(100,200),(250,270),(90,50),(400,190)]
    DC=DC_Problem(repulsive_nodes_list, attractive_nodes_list)
    for node in DC.repulsive_nodes_list:
        print(node.angle_to_other_nodes_dict)
        print(node.angle_sorted_nodes)
    for node in DC.attractive_nodes_list:
        if node.x==200 and node.y==200:
            print(node.angle_to_other_nodes_dict)
            print(node.angle_sorted_nodes)
            for n in node.angle_sorted_nodes:
                print(n.x,n.y,node.angle_to_other_nodes_dict[n])
