import sys

from PyQt5.QtGui import *

from PyQt5.uic import *

from PyQt5.Qt import QApplication
import BASIC_MODEL as BM
import RANDOM_INSTANCE_GENERATOR as RIG
import DRAW_LOCATIONS as DL
import AMPL_MODEL_SOLVER as AMS

# import pandas as pd

import matplotlib.pyplot as plt

import os

from PyQt5.uic import loadUi


class MyGui(object):

    def __init__(self, w):

        self.w = w
        self.w.show_pb.pressed.connect(self.ShowPressRoutine)
        self.w.solve_pb.pressed.connect(self.SolvePressRoutine)
        self.w.generate_pb.pressed.connect(self.GeneratePressRoutine)
        self.w.add_node_pb.pressed.connect(self.AddNodePressRoutine)
        self.w.generate_expl_pb.pressed.connect(self.GenerateExplicitInstance)
        self.expl_instance = RIG.INSTANCE([], [])

        self.w.tabWidget.currentChanged.connect(lambda: self.FillInstanceComboBox())
        self.FillAllComboBoxes()

        self.filtered_df = None

    def GenerateExplicitInstance(self):
        # todo
        file_name = self.w.expl_inst_name_lineEdit.text()
        i = 1
        d_dict, o_dict = {}, {}
        for node in self.expl_instance.desirable_nodes:
            d_dict[i] = node
            i += 1
        for node in self.expl_instance.obnoxious_nodes:
            o_dict[i] = node
            i += 1
        self.sol_instance = RIG.BuiltSolInstance(self.expl_instance, self.GetSolveData())
        RIG.WriteInstanceFile(file_name, self.sol_instance)
        self.ShowGraph("images/sanc_fig.png", self.expl_instance, self.w.expl_gen_label)
        self.w.plainTextEdit.clear()
        self.expl_instance.desirable_nodes = []
        self.expl_instance.obnoxious_nodes = []

    def FillAllComboBoxes(self):
        self.FillInstanceComboBox()
        self.FillDesirComboBox()
        self.FillObnoxComboBox()

    def ShowPressRoutine(self):
        print("bububu")
        instance_file = self.w.inst_comboBox.currentText()
        self.instance_to_solve = RIG.ReadInstance(instance_file)
        self.ShowGraph("images/sanc_fig.png", self.instance_to_solve, self.w.png_label)

    def ShowGraph(self, file_name, instance, label):
        DL.draw_graph(self.sol_instance, file_name)
        print(os.getcwd() + "\\" + file_name)
        pixmap = QPixmap(os.getcwd() + "\\" + file_name)
        plt.clf()
        label.setPixmap(pixmap)

        print("hallo1")

    def SolvePressRoutine(self):

        model = BM.Model(approx_level_integer=self.a_numb, instance=self.sol_instance)
        model_solver = AMS.AMPL_MS(model, "std_probl", "cplex")
        var_sol_dict, objective = model_solver.SolveNewProblem()
        print("new_a", var_sol_dict["new_a"])
        print("new_b", var_sol_dict["new_b"])
        facility_nodes = []
        for key in var_sol_dict["new_a"]:
            facility_nodes.append((var_sol_dict["new_a"][key], var_sol_dict["new_b"][key]))
        self.instance_to_solve.facility_nodes = facility_nodes
        self.ShowGraph("images/sanc_fig.png", self.instance_to_solve, self.w.png_label)

    def GeneratePressRoutine(self):
        file_name = self.w.inst_name_lineEdit.text()
        d_numb = self.w.desir_number_spinBox.value()
        o_numb = self.w.obnox_number_spinBox.value()
        max_x = self.w.max_x_spinBox.value()
        max_y = self.w.max_y_spinBox.value()
        d_dict, o_dict, facility_numb, max_x, max_y, d_goal, o_goal, f_interaction_goal = RIG.Generator(d_numb, o_numb,
                                                                                                        None, max_x,
                                                                                                        max_y, None,
                                                                                                        None,
                                                                                                        None)
        self.WriteInstanceFile(file_name, d_dict, o_dict)
        d_list = []
        o_list = []
        for key in d_dict:
            d_list.append(d_dict[key])
        for key in o_dict:
            o_list.append(o_dict[key])
        self.instance_generated = RIG.INSTANCE(d_list, o_list)
        self.ShowGraph("images/sanc_fig.png", self.instance_generated, self.w.gen_png_label)



    def AddNodePressRoutine(self):
        x = self.w.x_coord_spinBox.value()
        y = self.w.y_coord_spinBox.value()
        if self.w.desir_radioButton.isChecked():
            self.expl_instance.desirable_nodes.append((x, y))
            self.w.plainTextEdit.appendPlainText("d " + str(x) + " " + str(y))
        elif self.w.obnox_radioButton.isChecked():
            self.expl_instance.obnoxious_nodes.append((x, y))
            self.w.plainTextEdit.appendPlainText("o " + str(x) + " " + str(y))
        else:
            pass  # todo

    def FillInstanceComboBox(self):
        instances_path = os.getcwd() + "\\Instances"
        text_files = [f for f in os.listdir(instances_path) if f.endswith('.flp')]
        self.FillComboBox(self.w.inst_comboBox, text_files)

    def FillDesirComboBox(self):
        self.FillComboBox(self.w.desir_goal_comboBox, ["MinSum", "MinMax"])

    def FillObnoxComboBox(self):
        self.FillComboBox(self.w.obnox_goal_comboBox, ["MaxSum", "MaxMin"])

    def FillComboBox(self, cb, str_list):
        cb.clear()
        cb.addItems(str_list)

    def GetSolveData(self):
        d_goal = self.w.desir_goal_comboBox.currentText()
        o_goal = self.w.obnox_goal_comboBox.currentText()
        a_numb = self.w.approximation_number_spinBox.value()
        f_numb = self.w.facility_number_spinBox.value()
        return d_goal, o_goal, a_numb, f_numb



        # todo maxxmaxy


"""
    def FillComboBoxes(self):

        sanc_list = StateList(self.df)

        self.w.acteur_cb.addItems(sanc_list)

        sanc_type_list = ["all", "arms", "financial", "military", "other", "trade", "travel"]

        self.w.sanctioning_type_cb.addItems(sanc_type_list)

        success_list = GetAllPossibleEntries(self.df.success)

        self.w.result_cb.addItems(["all"] + success_list)

        obj_list = GetAllPossibleEntries(self.df.objective)

        self.w.objective_cb.addItems(["all"] + obj_list)

        self.w.alpha_property_cb.addItems(["year of end"])

        self.w.thickness_property_cb.addItems(["number of sanctionings"])

    def OnPressRoutine(self):

        self.Selections()

        pixmap = QPixmap(cur_dir + "\\sanc_fig.png")

        plt.clf()

        self.w.png_label.setPixmap(pixmap)

    def Selections(self):

        self.acteur = self.w.acteur_cb.currentText()

        self.sanc_type = self.w.sanctioning_type_cb.currentText()

        self.res = self.w.result_cb.currentText()

        self.obj = self.w.objective_cb.currentText()

        self.alpha = self.w.alpha_property_cb.currentText()

        self.thick = self.w.thickness_property_cb.currentText()

        if self.sanc_type == "all":

            self.filtered_df = self.df

        else:

            self.filtered_df = self.df[self.df.loc[:, self.sanc_type].isin([1])]

        if self.obj == "all":

            pass

        else:

            self.filtered_df = self.filtered_df[self.filtered_df['objective'].str.contains(self.obj)]

            print(self.filtered_df)

        if self.res == "all":

            pass

        else:

            self.filtered_df = self.filtered_df[self.filtered_df['success'].str.contains(self.res)]

        if self.w.sanctioner_radio.isChecked():

            SanctionedsToSanctioner(self.acteur, self.filtered_df)

        else:

            SanctionersToSanctioned(self.acteur, self.filtered_df)
"""

if __name__ == "__main__":
    # df = pd.read_csv(cur_dir + "\\gsdb_v1.csv", sep=";", encoding='utf-8', error_bad_lines=False)
    app = QApplication(sys.argv)
    w = loadUi("facility_location_opt.ui")
    mg = MyGui(w)
    # .FillComboBoxes()
    print("6")
    # w.show_pb.pressed.connect(mg.OnPressRoutine)
    print("7")
    w.show()
    sys.exit(app.exec_())
