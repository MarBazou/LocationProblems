param desirable_node_number;
param obnoxious_node_number;
param node_number:=desirable_node_number + obnoxious_node_number ;
param slice_number ;
set D_NODES:= 1 .. desirable_node_number;
set O_NODES:= desirable_node_number+1 .. desirable_node_number + obnoxious_node_number;
set NODES:= D_NODES union O_NODES;
param a_coord{NODES};
param b_coord{NODES};
param max_coord:=1000;
set SLICES := 1 .. slice_number ordered;
param sin{SLICES};
param cos{SLICES};
param M:= 3000;
var new_a >=0 <= max_coord ;
var new_b >=0 <= max_coord ;
var a{NODES} ;
var b{NODES} ;
var z_1{NODES} >=0;
var z_2{NODES} >=0;
var y{NODES} binary;
var x{NODES} binary;
var BinSlice{NODES,SLICES} binary;
var Z{NODES} >=0;
var Z_max_des >=0;
var Z_min_ob >=0, <=1000000000*obnoxious_node_number;

minimize GF:
 sum{k in D_NODES}Z[k] - sum{k in O_NODES}Z[k];

subject to EUCL{k in NODES, s in SLICES}: Z[k] >= a[k]*sin[s] +  b[k]*cos[s] ;
subject to EUCL2{k in O_NODES, s in SLICES}: Z[k] <= a[k]*sin[s] +  b[k]*cos[s] +M*(1-BinSlice[k,s]);
subject to EUCL3{k in O_NODES}: sum{s in SLICES}BinSlice[k,s]=1;
subject to A_Diff{k in NODES}: a[k] = a_coord[k] - new_a ;
subject to B_Diff{k in NODES}: b[k] = b_coord[k] - new_b ;
subject to ZMAX{k in D_NODES}: Z_max_des >= Z[k] ;
subject to ZMIN{k in O_NODES}: Z_min_ob <= Z[k] ;

