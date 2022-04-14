
'''
Created on 04.11.2021

@author: Markus Bozau


HowTo:
mod_strng := string of complete Mod
dat_strng := string of complete Dat
file_strng := string of the wished file name
solver_strng := string of solver (cplex or gurobi)
variable_strng_array := array containing the strings of the variable names
obj_strng := string of the goal function name
'''

import os
from amplpy import AMPL
from amplpy.environment import Environment
import amplpy

class AMPL_MS(object):
    def __init__(self, model, file_string, solver_string):  # goals 1 fermat weber  bzw summe        2 centerproblem
        directory = os.getcwd()
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.mod_string = model.mod_string
        self.dat_string = model.dat_string
        self.file_string = file_string
        self.solver_string = solver_string
        self.var_string_array = model.var_name_array
        self.obj_string = model.obj_string
        self.mod_filename = self.dir_path + "\\model_files\\" + self.file_string + ".mod"
        self.dat_filename = self.dir_path + "\\model_files\\" + self.file_string + ".dat"
        self.gurobi_solver = "C:\\Users\\marku\\OneDrive\\Desktop\\AMPL\\gurobi.exe"
        self.cplex_solver = "C:\\Users\\marku\\OneDrive\\Desktop\\AMPL\\cplex.exe"
        self.o_filename = os.getcwd() + "\\" + self.file_string + ".sol"
    # fertig
    def WriteModFile(self):
        self.WriteFile(self.mod_string, self.mod_filename)
    # fertig
    def WriteDatFile(self):
        if os.path.exists(self.dat_string):
            os.remove(self.dat_string)
        else:
            print("The file does not exist")
        self.WriteFile(self.dat_string, self.dat_filename)
    # fertig
    def WriteFile(self,strng,file_name):
        mod_file = open(file_name, 'w')
        mod_file.write(strng + "\n")
        mod_file.close()


    # fertig
    def StartSolver(self):
        ampl = AMPL(Environment('C:\\Users\\marku\\OneDrive\\Desktop\\AMPL'))

        class MyOutputHandler(amplpy.OutputHandler):
            """
            Class used as an output handler. It only prints the solver output.
            Must implement :class:`amplpy.OutputHandler`.
            """

            def output(self, kind, msg):
                if kind == amplpy.Kind.SOLVE:
                    assert ampl.isBusy()
                    print('Solver: {}'.format(msg))
                if kind == amplpy.Kind.SHELL_OUTPUT:
                    assert ampl.isBusy()
                    print('Shell: {}'.format(msg))
                if kind == amplpy.Kind.SHELL_MESSAGE:
                    assert ampl.isBusy()
                    print('Shell_msg: {}'.format(msg))

        ampl.setOption('solver', 'cplex')
        ampl.setOption('cplex_options', 'mipdisplay=2')
        # Read the model and data files.
        ampl.read(self.mod_filename)
        ampl.readData(self.dat_filename)
        # outputHandler = MyOutputHandler()
        # ampl.setOutputHandler(outputHandler)
        ampl.solve()

        var_dict={}
        for v in self.var_string_array:
            sol = {}
            ampl_var = ampl.getVariable(v)
            print(ampl_var)
            for var_tupel in ampl_var:
                ind_tuple = var_tupel[0]
                var = var_tupel[1]
                value = var.value()
                sol[ind_tuple] = value
            var_dict[v]=sol

        ampl_obj = ampl.getObjective(self.obj_string)
        obj = ampl_obj.value()
        return var_dict, obj

    def SolveNewProblem(self):
        self.WriteModFile()
        self.WriteDatFile()
        sol, objective = self.StartSolver()
        return sol, objective




def main():
    print("nothing to do here")
    pass

if __name__ == "__main__":
    main()
