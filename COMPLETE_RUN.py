import math

import RANDOM_INSTANCE_GENERATOR as RIG
import AMPL_MODEL_SOLVER as AMS
# import VISUALIZATION as VIS #todo
import BASIC_MODEL as BM
import DRAW_LOCATIONS as DL

desirable_numb, obnoxious_numb, max_coord = 3, 3, 1000
facility_numb, d_goal, o_goal, f_interaction_goal = 1, "min_sum", "max_sum", ""
use_act = True

if __name__ == "__main__":
    if not use_act:
        Instance = RIG.instance_generator(desirable_numb, obnoxious_numb, facility_numb, max_coord, d_goal, o_goal,
                                          f_interaction_goal)
        RIG.WriteInstanceFile("actual", Instance)
    else:
        base_instance = RIG.ReadInstance("actual")
        Instance = RIG.BuiltSolInstance(base_instance, "", "", 1, facility_numb)
    print(Instance.desirable_dict)
    Model = BM.HybridDesiredSumObnoxiousSumModel(instance=Instance, approx_lvl_integer=3)
    print(Model.Instance.desirable_dict)
    Model_Solver = AMS.AMPL_MS(Model, "std_probl", "cplex")
    var_sol_dict, objective = Model_Solver.SolveNewProblem()
    print("new_a", var_sol_dict["new_a"])
    print("new_b", var_sol_dict["new_b"])
    Instance.facility_extract(var_sol_dict["new_a"], var_sol_dict["new_b"])
    try:
        print("B", var_sol_dict["B"])
        Instance.nodes_to_facility(var_sol_dict["B"])
    except:
        pass
    DL.draw_graph(Instance, "/images/location_fig")
    # V_lizer=VIS.Visualizer(max_x,max_y,Instance,Model_Solver)
    # V_lizer.ShowUp()
    print(Instance.desirable_dict)
    print(Instance.obnoxious_dict)
    # print(V_lizer.x,V_lizer.y)
    print("new_a", var_sol_dict["new_a"])
    print("new_b", var_sol_dict["new_b"])
    print("Z", var_sol_dict["Z"])
    #print("Z_max_des", var_sol_dict["Z_max_des"])


    a = var_sol_dict["new_a"][()]
    b = var_sol_dict["new_b"][()]
    p=0
    for k in Instance.desirable_dict:
        ae=(Instance.desirable_dict[k][0]-a)**2
        be=(Instance.desirable_dict[k][1]-b)**2
        e=math.sqrt(ae+be)
        p=p+e
        print(e)
    print(p)
    t = 0
    for k in Instance.obnoxious_dict:
        ae=(Instance.obnoxious_dict[k][0]-a)**2
        be=(Instance.obnoxious_dict[k][1]-b)**2
        e=math.sqrt(ae+be)
        print(e)
        t = t + e
    print(t)
    print(p-t)





