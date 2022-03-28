param desirable_node_number;
param obnoxious_node_number;
param node_number:=desirable_node_number + obnoxious_node_number ;
param approx_level_integer ;
set D_NODES:= 1 .. desirable_node_number;
set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;
set NODES:= D_NODES union O_NODES;
param a_coord{NODES};
param b_coord{NODES};
param max_coord:=1000;
set Levels := 1 .. approx_level_integer ordered;
set Levels_Z := 0 .. approx_level_integer ordered;
param q{Levels};
param M:= 1500;
var new_a >=0 <= max_coord ;
var new_b >=0 <= max_coord ;
var a{NODES} ;
var b{NODES} ;
var z_1{NODES,Levels_Z} >=0;
var z_2{NODES,Levels_Z} >=0;
var y{NODES,Levels_Z} binary;
var x{NODES,Levels_Z} binary;
var Z{NODES} >=0;
var Z_max_des >=0;
var Z_min_ob >=0;

minimize GF:
 Z_max_des - Z_min_ob;

subject to INIT_11{k in NODES}: z_1[k,0] >= a[k]  ;
subject to INIT_12{k in NODES}: z_1[k,0] <= a[k] + x[k,0]*M;
subject to INIT_13{k in NODES}: z_1[k,0] >= -a[k] ;
subject to INIT_14{k in NODES}: z_1[k,0] <= -a[k] +(1-x[k,0])*M;
subject to INIT_21{k in NODES}: z_2[k,0] >= b[k] ;
subject to INIT_22{k in NODES}: z_2[k,0] <= b[k] + y[k,0] *M;
subject to INIT_23{k in NODES}: z_2[k,0] >= -b[k] ;
subject to INIT_24{k in NODES}: z_2[k,0] <= -b[k] +(1-y[k,0])*M;
subject to ABS_01{k in NODES}:a[k]>=0 - x[k,0] *M;
subject to ABS_02{k in NODES}:-a[k]>=0 - (1-x[k,0])*M;
subject to ABS_03{k in NODES}:b[k]>=0 - y[k,0] *M;
subject to ABS_04{k in NODES}:-b[k]>=0 - (1-y[k,0])*M;
subject to ABS_11{k in NODES,i in Levels}: z_1[k,i]>=z_1[k,i-1] - z_2[k,i-1] ;
subject to ABS_12{k in NODES,i in Levels}: z_1[k,i]<=z_1[k,i-1] - z_2[k,i-1] +(1 - y[k,i])*M ;
subject to ABS_13{k in NODES,i in Levels}: z_1[k,i]>=z_2[k,i-1] - z_1[k,i-1] ;
subject to ABS_14{k in NODES,i in Levels}: z_1[k,i]<=z_2[k,i-1] - z_1[k,i-1] +y[k,i]*M;
subject to MIN_11{k in NODES,i in Levels}: z_2[k,i]<=q[i] * z_1[k,i-1];
subject to MIN_12{k in NODES,i in Levels}: z_2[k,i]>=q[i] * z_1[k,i-1] - y[k,i]*M ;
subject to MIN_13{k in NODES,i in Levels}: z_2[k,i]<=q[i] * z_2[k,i-1] ;
subject to MIN_14{k in NODES,i in Levels}: z_2[k,i]>=q[i] * z_2[k,i-1] - (1 - y[k,i])*M ;
subject to MIN_15{k in NODES,i in Levels}: z_2[k,i-1] - z_1[k,i-1] >=0 - y[k,i]*M ;
subject to EUCL{k in NODES}: Z[k] = z_1[k,last(Levels)] +  z_2[k,last(Levels)] ;
subject to A_Diff{k in NODES}: a[k] = a_coord[k] - new_a ;
subject to B_Diff{k in NODES}: b[k] = b_coord[k] - new_b ;
subject to ZMAX{k in D_NODES}: Z_max_des >= Z[k] ;
subject to ZMIN{k in O_NODES}: Z_min_ob <= Z[k] ;
