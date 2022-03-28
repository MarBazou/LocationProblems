import Eucledean_Approximation.RANDOM_INSTANCE_GENERATOR as RIG
import Eucledean_Approximation.AMPL_MODEL_SOLVER as AMS
import Eucledean_Approximation.BASIC_MODEL as BM
import time

desirable_numb, obnoxious_numb, max_coord = 40, 7, 1200
facility_numb, d_goal, o_goal, f_interaction_goal = 2,"min_sum","max_sum",""

if __name__ == "__main__":
    gt1=0
    gt2=0
    for i in range(100):
        Instance = RIG.instance_generator(desirable_numb, obnoxious_numb, facility_numb, max_coord, d_goal, o_goal, f_interaction_goal)
        print(Instance.desirable_dict)
        Model = BM.DesiredMaxObnoxiousMinModel(instance=Instance,approx_lvl_integer=4)
        Model2 = BM.DesiredMaxObnoxiousMinModel2(instance=Instance, approx_lvl_integer=4)
        #Model = CM.Model(instance=Instance, approx_lvl_integer=3)

        print(Model.Instance.desirable_dict)
        Model_Solver = AMS.AMPL_MS(Model, "std_probl", "cplex")
        Model_Solver2 = AMS.AMPL_MS(Model2, "std_probl", "cplex")
        a=time.time()
        var_sol_dict, objective = Model_Solver.SolveNewProblem()
        b=time.time()
        var_sol_dict, objective = Model_Solver2.SolveNewProblem()
        c=time.time()
        t1=b-a
        t2=c-b
        gt1+=t1
        gt2+=t2
    gt1=gt1/100
    gt2=gt2/100
    print("gt1: ",gt1,"; gt2: ",gt2)

    #V_lizer=VIS.Visualizer(max_x,max_y,Instance,Model_Solver)
    #V_lizer.ShowUp()
    print(Instance.desirable_dict)
    print(Instance.obnoxious_dict)
    #print(V_lizer.x,V_lizer.y)
    print("new_a",var_sol_dict["new_a"])
    print("new_b",var_sol_dict["new_b"])
    print("Zb",var_sol_dict["Zb"])
    print("Z",var_sol_dict["Z"])