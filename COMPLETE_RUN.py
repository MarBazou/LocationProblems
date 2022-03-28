import Eucledean_Approximation.RANDOM_INSTANCE_GENERATOR as RIG
import Eucledean_Approximation.AMPL_MODEL_SOLVER as AMS
import Eucledean_Approximation.VISUALIZATION as VIS #todo
import Eucledean_Approximation.BASIC_MODEL as BM

desirable_numb, obnoxious_numb, max_coord = 40, 7, 1200
facility_numb, d_goal, o_goal,f_interaction_goal= 2,"min_sum","max_sum",""

if __name__ == "__main__":
    Instance = RIG.instance_generator(desirable_numb, obnoxious_numb, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal)
    print(Instance.desirable_dict)
    Model = BM.DesiredSumObnoxiousSumModel(instance=Instance,approx_lvl_integer=3)
    print(Model.Instance.desirable_dict)
    Model_Solver = AMS.AMPL_MS(Model, "std_probl", "cplex")
    var_sol_dict, objective = Model_Solver.SolveNewProblem()
    #V_lizer=VIS.Visualizer(max_x,max_y,Instance,Model_Solver)
    #V_lizer.ShowUp()
    print(Instance.desirable_dict)
    print(Instance.obnoxious_dict)
    #print(V_lizer.x,V_lizer.y)
    print("new_a",var_sol_dict["new_a"])
    print("new_b",var_sol_dict["new_b"])
    print("Zb",var_sol_dict["Zb"])
    print("Z",var_sol_dict["Z"])
