'''
Created on 08.08.2018

@author: Markus Bozau


Visualisierung
mehrere factories
verbotene Gebiete
Barrieren
runden

'''
from math import sqrt
import os
import time
from random import randint
import pygame


class WriteFiles(object):
    
    
    def __init__(self,approx_level_integer,desirable_knot_dict,obnoxious_knot_dict,desirable_goal,obnoxious_goal,fact_number=1): #goals 1 fermat weber  bzw summe        2 centerproblem
        directory=os.getcwd()
        self.lp_filename=directory+"\\euclidean.lp"
        self.mod_filename=directory+"\\euclidean.mod"
        self.dat_filename=directory+"\\euclidean.dat"
        self.run_filename=directory+"\\euclidean.run"
        self.gurobi_solver="C:\\Users\\marku\\OneDrive\\Desktop\\gurobi.exe"
        self.o_filename=os.getcwd()+"\\euclidean.sol"
        #self.o_filename="o_sudo.txt"
        self.approx_level_integer=approx_level_integer
        self.desirable_knot_dict=desirable_knot_dict
        self.desirable_knot_number=len(self.desirable_knot_dict)
        self.obnoxious_knot_dict=obnoxious_knot_dict
        self.obnoxious_knot_number=len(self.obnoxious_knot_dict)
        self.desirable_goal=desirable_goal
        self.obnoxious_goal=obnoxious_goal
        self.fact_number=fact_number
        
        
    def Approx_Constr(self):
    
        yield("subject to INIT_11{k in KNOTS}: z_1[k,0] >= a[k]  ;" )      #initialisierung der ersten ebene damit haetten wir manhatten Norm
        yield("subject to INIT_12{k in KNOTS}: z_1[k,0] <= a[k] + x[k,0]*M;" )
        yield("subject to INIT_13{k in KNOTS}: z_1[k,0] >= -a[k] ;" )
        yield("subject to INIT_14{k in KNOTS}: z_1[k,0] <= -a[k] +(1-x[k,0])*M;" )
        yield("subject to INIT_21{k in KNOTS}: z_2[k,0] >= b[k] ;" )
        yield("subject to INIT_22{k in KNOTS}: z_2[k,0] <= b[k] + y[k,0] *M;" ) 
        yield("subject to INIT_23{k in KNOTS}: z_2[k,0] >= -b[k] ;")
        yield("subject to INIT_24{k in KNOTS}: z_2[k,0] <= -b[k] +(1-y[k,0])*M;")
        
        yield("subject to ABS_01{k in KNOTS}:a[k]>=0 - x[k,0] *M;")
        yield("subject to ABS_02{k in KNOTS}:-a[k]>=0 - (1-x[k,0])*M;")
        yield("subject to ABS_03{k in KNOTS}:b[k]>=0 - y[k,0] *M;")
        yield("subject to ABS_04{k in KNOTS}:-b[k]>=0 - (1-y[k,0])*M;")
        
        
        yield("subject to ABS_11{k in KNOTS,i in Levels}: z_1[k,i]>=z_1[k,i-1] - z_2[k,i-1] ;" )   #rekursiver Aufbau der Betragsfunktion f'_i
        yield("subject to ABS_12{k in KNOTS,i in Levels}: z_1[k,i]<=z_1[k,i-1] - z_2[k,i-1] +(1 - y[k,i])*M ;" )
        yield("subject to ABS_13{k in KNOTS,i in Levels}: z_1[k,i]>=z_2[k,i-1] - z_1[k,i-1] ;" )
        yield("subject to ABS_14{k in KNOTS,i in Levels}: z_1[k,i]<=z_2[k,i-1] - z_1[k,i-1] +y[k,i]*M;" )
        

        
        yield("subject to MIN_11{k in KNOTS,i in Levels}: z_2[k,i]<=q[i] * z_1[k,i-1];" )   #rekursiver Aufbau der Minimumfunktion f''_i
        yield("subject to MIN_12{k in KNOTS,i in Levels}: z_2[k,i]>=q[i] * z_1[k,i-1] - y[k,i]*M ;" )       # geaendert man kann den binaeren teil auch noch dran hauen an die <= restriktionen
        yield("subject to MIN_13{k in KNOTS,i in Levels}: z_2[k,i]<=q[i] * z_2[k,i-1] ;" )   # besser jeder test war laufzeit technisch wesentlich performanter (haette ich so nicht erwartet)
        yield("subject to MIN_14{k in KNOTS,i in Levels}: z_2[k,i]>=q[i] * z_2[k,i-1] - (1 - y[k,i])*M ;" )  #ueberall durchgefuehrt im test faktor 30 schneller
        
        #yield("subject to MIN_15{k in KNOTS,i in Levels}: z_2[k,i-1] - z_1[k,i-1] >=0 - y[k,i]*M ;")   #Schalter fuer y_i binary variable der Minimumfunktion f''_i
        #yield("subject to MIN_16{k in KNOTS,i in Levels}: z_1[k,i-1] - z_2[k,i-1] >= 0 - (1 - y[k,i])*M ;") #vermutlich ueflue durch ABS 11-14
        
        yield("subject to EUCL{k in KNOTS}: Z[k] = z_1[k,%s] +  z_2[k,%s] ;" %(self.approx_level_integer,self.approx_level_integer))  #Approximierter Wert fuer euklidische Entfernung  
        
        if self.desirable_goal==2:
            yield("subject to ZMAX{k in D_KNOTS}: Z_max_des >= Z[k] ;" ) #Maximum der erwuenschten Entfernungen
        if self.obnoxious_goal==2 and self.obnoxious_knot_number!=0:
            yield("subject to ZMIN{k in O_KNOTS}: Z_min_ob <= Z[k] ;")  #Minimum der erwuenschten Entfernungen
        
        #yield("subject to bla1: new_a=450;" )        
        #yield("subject to bla2: new_b=500;" )     
        
        
        yield("end;\n")  
        
    

    def ChainRoots(self,root_integer=2):
        i=1
        q_list=[]
        q_i=0
        while i<=self.approx_level_integer:
            q_i=sqrt(q_i + 2)
            q_list.append(q_i)
            i=i+1
        return q_list    
    
    def Coord_Diffs(self):
        yield("subject to A_Diff{k in KNOTS}: a[k] = a_coord[k] - new_a ;")  #Approximierter Wert fuer euklidische Entfernung  
        yield("subject to B_Diff{k in KNOTS}: b[k] = b_coord[k] - new_b ;")
        yield("\n")
    
    def Defs(self):
        yield("param desirable_knot_number;")
        yield("param obnoxious_knot_number;")
        yield("param knot_number:=desirable_knot_number + obnoxious_knot_number ;")
        yield("param approx_level_integer ;")
        yield("set D_KNOTS:= 1 .. desirable_knot_number;")
        if self.obnoxious_knot_number!=0:
            yield("set O_KNOTS:= desirable_knot_number+1 .. desirable_knot_number + obnoxious_knot_number;")
            yield("set KNOTS:= D_KNOTS union O_KNOTS;")
        else:
            yield("set KNOTS:= D_KNOTS;")
        yield("param a_coord{KNOTS};")
        yield("param b_coord{KNOTS};")
        
        
        yield("set Levels := 1 .. approx_level_integer;")
        yield("set Levels_Z := 0 .. approx_level_integer;")
        yield("param q{Levels};")
        yield("param M:= 2000;")
        yield("var new_a >=0 <=1000;")
        yield("var new_b >=0 <=1000;")
        yield("var a{KNOTS} ;")
        yield("var b{KNOTS} ;")
        yield("var z_1{KNOTS,Levels_Z} >=0;")
        yield("var z_2{KNOTS,Levels_Z} >=0;")
        yield("var y{KNOTS,Levels_Z} binary;")
        yield("var x{KNOTS,Levels_Z} binary;")
        yield("var Z{KNOTS} >=0;")
        
        if self.desirable_goal==2:
            yield("var Z_max_des >=0;")
        
        if self.obnoxious_goal==2 and self.obnoxious_knot_number!=0:
            yield("var Z_min_ob >=0;")
            
        yield("\n")
        
        
        
    def Goal_Func(self):
        gf_string="minimize GF:"
        if self.desirable_goal==0:
            gf_string=gf_string
        elif self.desirable_goal==1:
            gf_string=gf_string+" sum{k in D_KNOTS}Z[k]"
        else:
            gf_string=gf_string+" Z_max_des"
        if self.obnoxious_goal==0 or self.obnoxious_knot_number==0:
            gf_string=gf_string
        elif self.obnoxious_goal==1:
            gf_string=gf_string +" - sum{k in O_KNOTS}Z[k]"
        else:    
            gf_string=gf_string +" - Z_min_ob"
        gf_string=gf_string+";"    
            
        yield(gf_string)
        yield("\n")
    
    def BarrierConstraints(self):
        pass
    
    def StartSolver(self):
        

        failed=False
        timelimit=6000000
     
        glpk_solver="C:\\Users\\Markus Bozau\\Downloads\\winglpk-4.65\\glpk-4.65\\w64\\glpsol.exe"
        process=subprocess.Popen([glpk_solver,"--math","--check","-m",self.mod_filename,"-d",self.dat_filename,"--wlp",self.lp_filename])
    
        for  i in range(timelimit):
            if not process.poll() is None:
                if process.poll() !=0:
                    print("failed")
                    failed=True
                else:
                    print("succeeded")
                break
            time.sleep(2)
        else:
            process.terminate()
    
            print("failed caused by too less given time")
            failed=True

    
    
        solve_process=subprocess.Popen([self.gurobi_solver,"TimeLimit=6000","MIPGap=0.0001","ResultFile="+self.o_filename,self.lp_filename,"MIPGap= 0.8"])#"LogFile="+os.getcwd()+"\sudo.log","ResultFile="+os.getcwd()+"\sudo.sol",self.lp_filename,"MIPGap= 0.8"])#,"NodefileStart=4","Threads =3"])

        while solve_process.poll() is None:
            time.sleep(2)

        
        
        
        #ampl= "C:\\Python27\\AMPL_Scite_Kurslizenz\\AMPL\\ampl.exe"
   
        #process=subprocess.Popen([ampl, self.run_filename],shell=True)
        #while process.poll() is None:
       #     time.sleep(2)
      
        
    def WriteModFile(self):
        mod_file=open(self.mod_filename,'w')
        
        for line in self.Defs():
            
            mod_file.write(line + "\n")
         
        for line in self.Goal_Func():
            
            mod_file.write(line + "\n")
            
        for line in self.Coord_Diffs():
            
            mod_file.write(line + "\n")
            
        for line in self.Approx_Constr():
            
            mod_file.write(line + "\n")
            
        mod_file.close()
            
        
        
    def WriteRunFile(self):
        run_file=open(self.run_filename,'w')
        
        for line in self.RunFileContent():
            
            run_file.write(line + '\n')
            
        run_file.close()
 
 
    def RunFileContent(self):
        
        yield "option solver " + self.gurobi_solver + " ;"
        yield "model " + self.mod_filename + " ;"
        yield "data "  + self.dat_filename + " ;"
        yield ""
        yield "solve;"
        yield ""
        yield "display new_a  >" + self.o_filename+ " ;"
        yield "display new_b  >" + self.o_filename+ " ;"
        #yield "display {(z,s,k) in Zeilen cross Spalten cross Zahlen : nummer[z,s,k]>0}  >" + self.o_filename+ " ;"
        yield "close " + self.o_filename+  " ;"
      

      
    def WriteDatFile(self):
        dat_file=open(self.dat_filename, 'w')
        
        for line in self.DatFileContent():
            
            dat_file.write(line + '\n')
            
        dat_file.close()

     
    def DatFileContent(self):        
        yield("param desirable_knot_number := %s;"%(self.desirable_knot_number))
        yield("param obnoxious_knot_number := %s;"%(self.obnoxious_knot_number))
        yield("param approx_level_integer := %s ;" %(self.approx_level_integer))
        a_string=""
        b_string=""
        for knot in self.desirable_knot_dict:
            a_string=a_string+str(knot)+" %s "%(self.desirable_knot_dict[knot][0])
        for knot in self.obnoxious_knot_dict:
            a_string=a_string+str(knot)+" %s "%(self.obnoxious_knot_dict[knot][0])
        yield("param a_coord:=%s;"%(a_string))
        for knot in self.desirable_knot_dict:
            b_string=b_string+str(knot)+" %s "%(self.desirable_knot_dict[knot][1])
        for knot in self.obnoxious_knot_dict:
            b_string=b_string+str(knot)+" %s "%(self.obnoxious_knot_dict[knot][1])
        yield("param b_coord:=%s;"%(b_string))
        
        q_list=self.ChainRoots(2)
        i=1
        q_string=""
        for q_i in q_list:
            q_string=q_string+str(i)+" "+str(q_i)+" "
            i=i+1
        yield("param q:= %s ;" %(q_string))
        yield("\n")   
           
           
           
           

    def GetSolution(self):
        
        whole_solution=self.ReadSolution()
        x,y=self.FormatSolution(whole_solution)
        
        return x,y
        
      
    def ReadSolution(self):
        sol_file=open(self.o_filename,'r')
        
        counter=0
        whole_solution=[]
        print(whole_solution)
        for line in sol_file:
            if counter==0:
                counter+=1
            else:
                whole_solution.append(line)
                counter+=1
        print(whole_solution)
        sol_file.close()    
        return whole_solution
   
      
    def FormatSolution(self,whole_solution):
        
        #whole_solution=whole_solution.split()
        for i in range(len(whole_solution)):
            whole_solution[i]=whole_solution[i].split(" ")
            #print(whole_solution[i])
        print("hallo")
        print(whole_solution)
        
        for sol in whole_solution:
            if sol[0]=="new_a":
                x=sol[1]
            elif sol[0]=="new_b":
                y=sol[1]
            #sol[0]=sol[0].strip('(')
            #sol[0]=sol[0].strip(')')
            #sol[0]=sol[0].strip('Z')
            #sol[0]=sol[0].split(',')
        x=x.strip("\n")
        y=y.strip("\n")   
        x=float(x)    
        y=float(y)    
        x=int(x)
        y=int(y)
        return x,y         
       
        
 

def InstanceGenerator(desirable_numb,obnoxious_numb,max_x,max_y):
    desirable_dict={}
    obnoxious_dict={}
    i=0
    while i<desirable_numb:
        i=i+1
        desirable_dict[i]=[randint(0,max_x),randint(0,max_y)]
    j=i
    while j<desirable_numb+obnoxious_numb:
        j=j+1
        obnoxious_dict[j]=[randint(0,max_x),randint(0,max_y)]
    return desirable_dict,obnoxious_dict

def SolveNewProblem(desirable_dict,obnoxious_dict):
    
    
    #Wf=WriteFiles(5,{1:[700,600],2:[200,400],3:[200,500],4:[700,500],5:[200,600],6:[700,400]},{7:[400,200]},1,1,1)  
    Wf=WriteFiles(5,desirable_dict,obnoxious_dict,2,2,1) 
    Wf.WriteModFile() 
    Wf.WriteDatFile()  
    Wf.WriteRunFile()   
    Wf.StartSolver()
    x,y=Wf.GetSolution()
    print(x,y)
    return x,y


black,green,red,blue,yellow=(0,0,0),(0,250,100),(200,0,0),(0,0,200),(200,200,0)



max_x, max_y=1000,1000 
pygame.init()
done=False
clock=pygame.time.Clock()
screen=pygame.display.set_mode((max_x, max_y))
pygame.display.set_caption("facility_location")
desirable_dict,obnoxious_dict=InstanceGenerator(100, 0, max_x, max_y)
#desirable_dict,obnoxious_dict={1:[70,60],2:[20,400],3:[260,540],4:[700,505],5:[209,60],6:[700,465],7:[70,40]},{8:[140,20],9:[490,780]}

screen.fill(black)
for entr in desirable_dict:
    pygame.draw.circle(screen,green,desirable_dict[entr],3,2)
for entr in obnoxious_dict:
    pygame.draw.circle(screen,red,obnoxious_dict[entr],3,2)
pygame.draw.rect(screen, blue, (475,0,50,50),1)
pygame.display.flip()
x,y=None,None
on=True
while not done:
    clock.tick(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 475<=event.pos[0]<=525 and 0<=event.pos[1]<=50:
                x,y=SolveNewProblem(desirable_dict,obnoxious_dict)

                pygame.draw.circle(screen,yellow,(x,y),5,2)
                pygame.display.flip()
    if x!=None and y!=None:
        if on==True:
            pygame.draw.circle(screen,yellow,(x,y),3,2)
            pygame.display.flip()
            on=False
        else:
            pygame.draw.circle(screen,black,(x,y),3,2)
            pygame.display.flip()
            on=True
pygame.quit()










