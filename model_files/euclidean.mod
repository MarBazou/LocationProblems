param desirable_knot_number;
param obnoxious_knot_number;
param knot_number:=desirable_knot_number + obnoxious_knot_number ;
param depot_number;
param approx_level_integer ;
set D_KNOTS:= 1 .. desirable_knot_number;
set KNOTS:= D_KNOTS ;
set DEPOTS:= 1 .. depot_number; 
param a_coord{KNOTS};
param b_coord{KNOTS};
set Levels := 1 .. approx_level_integer;
set Levels_Z := 0 .. approx_level_integer;
param q{Levels};
param M:= 2000;
var new_a{DEPOTS} >=0 <=1000;
var new_b{DEPOTS} >=0 <=1000;
var a{KNOTS} ;
var b{KNOTS} ;
var a_d{KNOTS,DEPOTS} ;
var b_d{KNOTS,DEPOTS} ;
var p{KNOTS,DEPOTS} binary;
var z_1{KNOTS,Levels_Z} >=0;
var z_2{KNOTS,Levels_Z} >=0;
var y{KNOTS,Levels_Z} binary;
var x{KNOTS,Levels_Z} binary;
var Z{KNOTS} >=0;
var Z_max_des >=0;


minimize GF: Z_max_des;


subject to A_Diff{k in KNOTS,d in DEPOTS}: a_d[k,d] = a_coord[k] - new_a[d] ;
subject to B_Diff{k in KNOTS,d in DEPOTS}: b_d[k,d] = b_coord[k] - new_b[d] ;
subject to A_Diff_up{k in KNOTS,d in DEPOTS}: a[k]<=a_d[k,d]+(1-p[k,d])*2*M;
subject to A_Diff_low{k in KNOTS,d in DEPOTS}: a[k]>=a_d[k,d]-(1-p[k,d])*2*M;
subject to B_Diff_up{k in KNOTS,d in DEPOTS}: b[k]<=b_d[k,d]+(1-p[k,d])*2*M;
subject to B_Diff_low{k in KNOTS,d in DEPOTS}: b[k]>=b_d[k,d]-(1-p[k,d])*2*M;
subject to One_Depot{k in KNOTS}:sum{d in DEPOTS}p[k,d]=1;


subject to INIT_11{k in KNOTS}: z_1[k,0] >= a[k] ;
subject to INIT_12{k in KNOTS}: z_1[k,0] <= a[k] + x[k,0]*M;
subject to INIT_13{k in KNOTS}: z_1[k,0] >= -a[k] ;
subject to INIT_14{k in KNOTS}: z_1[k,0] <= -a[k] +(1-x[k,0])*M;
subject to INIT_21{k in KNOTS}: z_2[k,0] >= b[k] ;
subject to INIT_22{k in KNOTS}: z_2[k,0] <= b[k] + y[k,0] *M;
subject to INIT_23{k in KNOTS}: z_2[k,0] >= -b[k] ;
subject to INIT_24{k in KNOTS}: z_2[k,0] <= -b[k] +(1-y[k,0])*M;
subject to ABS_01{k in KNOTS}:a[k]>=0 - x[k,0] *M;
subject to ABS_02{k in KNOTS}:-a[k]>=0 - (1-x[k,0])*M;
subject to ABS_03{k in KNOTS}:b[k]>=0 - y[k,0] *M;
subject to ABS_04{k in KNOTS}:-b[k]>=0 - (1-y[k,0])*M;
subject to ABS_11{k in KNOTS,i in Levels}: z_1[k,i]>=z_1[k,i-1] - z_2[k,i-1]  ;
subject to ABS_12{k in KNOTS,i in Levels}: z_1[k,i]<=z_1[k,i-1] - z_2[k,i-1] +(1 - y[k,i])*M ;
subject to ABS_13{k in KNOTS,i in Levels}: z_1[k,i]>=z_2[k,i-1] - z_1[k,i-1] ;
subject to ABS_14{k in KNOTS,i in Levels}: z_1[k,i]<=z_2[k,i-1] - z_1[k,i-1] +y[k,i]*M;
subject to MIN_11{k in KNOTS,i in Levels}: z_2[k,i]<=q[i] * z_1[k,i-1] ;
subject to MIN_12{k in KNOTS,i in Levels}: z_2[k,i]>=q[i] * z_1[k,i-1] - y[k,i]*M ;
subject to MIN_13{k in KNOTS,i in Levels}: z_2[k,i]<=q[i] * z_2[k,i-1];
subject to MIN_14{k in KNOTS,i in Levels}: z_2[k,i]>=q[i] * z_2[k,i-1] - (1 - y[k,i])*M ;
subject to EUCL{k in KNOTS}: Z[k] = z_1[k,4] +  z_2[k,4] ;
subject to ZMAX{k in D_KNOTS}: Z_max_des >= Z[k] ;
end;

