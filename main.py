from array import *
import sys
from copy import copy, deepcopy
import math
def Get_Data():
    rows=int(input("Number of sources: "))
    cols=int(input("Number of destinations: "))
    S=[]
    for i in range(1,rows+1):
        S.append([float(j) for j in input("Supply for Source {0}: ".format(i)).split()])
        i+=1
    T=[]
    for i in range(1,rows+1):
        T.append([float(j) for j in input("Costs for Source {0} and each destination in ascending order: ".format(i)).split()]+S[i-1])
    T.append([float(j) for j in input("Demand for each destination in enumerated order: ").split()])

    total_supply=list(map(sum, S))
    Total_Supply=sum(total_supply)

    Total_Demand=sum(map(float, T[rows]))
        
    Difference=float(Total_Demand-Total_Supply)
    if (Difference>0):
        T.insert(rows, ([0]*cols))
        T[rows].append(Difference)
        return T, rows, cols, Difference
    elif (Difference<0):
        for i in range(0,rows):
            T[i].insert(cols, 0)
        T[rows].append(-1*Difference)
        return T, rows, cols, Difference
    else:
        return T, rows, cols, Difference
def Set_Initial_Basic_Variables():
    print("\nCost Tableau:")
    for row in Cost:
        print(row)
    for i in range(0,rows):
        for j in range(0,cols):
            Basic_Var[i][j]=0
    for h in range(0,rows):
        for k in range(0,cols):
            for j in range(0,cols):
                col_totals[j]=0
                for i in range(0,rows):
                    col_totals[j]+=Basic_Var[i][j]
            for i in range(0,rows):
                row_totals[i]=0
                for j in range(0,cols):
                    row_totals[i]+=Basic_Var[i][j]
            if row_totals[h]<Basic_Var[h][cols] and col_totals[k]<Basic_Var[rows][k]:
                Basic_Var[h][k]=min(abs(row_totals[h]-Basic_Var[h][cols]), abs(col_totals[k]-Basic_Var[rows][k]))   
            else:
                continue 
    for i in range(1, rows):
        for j in range(0,cols-1):
            if Basic_Var[i][j+1]>0 and Basic_Var[i-1][j]>0 and Basic_Var[i-1][j+1]==0 and Basic_Var[i][j]==0: 
                Basic_Var[i][j]=0.00001
    print("\nInitial Basic Variable Tableau:")
    for row in Basic_Var:
        print(row)
    return Basic_Var
def Set_Basic_Variables(x,y):
    print("Cost Tableau:")
    for row in Cost:
        print(row)
    for i in range(0,rows):
        for j in range(0,cols):
            Basic_Var[i][j]=0
    for h in range(0,rows):
        for k in range(0,cols):
            for j in range(0,cols):
                col_totals[j]=0
                for i in range(0,rows):
                    col_totals[j]+=Basic_Var[i][j]
            for i in range(0,rows):
                row_totals[i]=0
                for j in range(0,cols):
                    row_totals[i]+=Basic_Var[i][j]
            if row_totals[h]<Basic_Var[h][cols] and col_totals[k]<Basic_Var[rows][k]:
                Basic_Var[h][k]=min(abs(row_totals[h]-Basic_Var[h][cols])), abs(col_totals[k]-Basic_Var[rows][k])   
            else:
                continue 
    if Basic_Var[x][y]==0:
        Basic_Var[x][y]=0.001
    print("\nBasic Variable Tableau:")
    for row in Basic_Var:
        print(row)
    return Basic_Var
def Form_Initial_Ui_and_Vi():
    for i in range(0,rows):
        Cost[i].append('null')
    Cost.append(['null']*cols)
    Cost[0][cols+1]=0
    print()
    for h in range(0,rows):
        for k in range(0,cols):
            if Basic_Var[h][k]!=0:
                if Cost[h][cols+1]=='null':
                    Cost[h][cols+1]=Cost[h][k]-Cost[rows+1][k]
                else:
                    Cost[rows+1][k]=Cost[h][k]-Cost[h][cols+1]
            else:
                continue
    print("U_i and V_i Tableau")
    for row in Cost:
        print(row)
def Form_Ui_and_Vi():
    for i in range(0,rows):
        Cost[i][cols+1]='null' 
    for j in range (0,cols):
        Cost[rows+1][j]='null' 
    Cost[0][cols+1]=0
    print()
    m=0
    t=0
    while (t<=(rows*cols)):
        t+=1
        for h in range(0,rows):
            for k in range(0,cols):
                if Basic_Var[h][k]!=0 or Basic_Var[h][k]!=0.0: # or (h==x and k==y)
                    if Cost[h][cols+1]=='null' and  Cost[rows+1][k]!='null':
                        Cost[h][cols+1]=float(Cost[h][k])-float(Cost[rows+1][k])
                    elif Cost[rows+1][k]=='null' and Cost[h][cols+1]!='null':
                        Cost[rows+1][k]=Cost[h][k]-Cost[h][cols+1]
                    else:
                        continue
                    continue
    print("\nU_i and V_i Tableau")
    for row in Cost:
        print(row)
def Form_Wi_and_Test():
    for h in range(0,rows):
        for k in range(0,cols):
            if Basic_Var[h][k]==0:
                W_i[h][k]=Cost[h][k]-Cost[h][cols+1]-Cost[rows+1][k]
            else:
                continue
    print('\nW_i Tableau')
    for row in W_i:
        print(row)
    z=0
    for i in range(0,rows):
        for j in range(0,cols):
            if W_i[i][j]<0:
                z+=1
            else:
                continue
    if z==0:
        print("\nWe're done!")
        print_results()
        quit()
    else:
        print('We are not done')
        return Basic_Var
def Find_Minimum():
    min=W_i[0][0]
    for h in range(0,rows):
        for k in range(0,cols):
            if W_i[h][k]<min:
                min=W_i[h][k]
            else:
                continue
    print('\nFound min', min)
    for x in range(0,rows):
        for y in range(0,cols):
            if W_i[x][y]==min:
                print('position of min: ', x,y)
                return W_i,W_i[x][y],x,y
            else:
                continue
def Set_New_Basic_Var(rows,cols):
    for h in range(0,rows):
        for k in range(0,cols):
            if h==x and k==y:
                Testing_Tableau[h][k]='n.n.'
            elif Basic_Var[h][k]==0:
                Testing_Tableau[h][k]='null'
            else:
                Testing_Tableau[h][k]='n.n.'
                continue
    #print('True or False Tableau')
    #for row in Testing_Tableau:
    #    print(row)
    g=0
    while g<=(rows*cols):
        for i in range(0,rows):
            for j in range(0,cols):
                nan_row_count=0
                nan_row_count=Testing_Tableau[(x+i)%rows].count('n.n.')
                nan_col_count=0
                for h in range(0,rows):
                    if Testing_Tableau[(x+h)%rows][(y+j)%cols]=='n.n.':
                        nan_col_count+=1
                    else:
                        continue
                if nan_row_count<2 or nan_col_count<2:
                    Testing_Tableau[(x+i)%rows][(y+j)%cols]='null'
                else:
                    g+=1
                    continue
    #print("\nValidation")
    #for row in Testing_Tableau:
    #    print(row)
    #m=1
    for i in range(0,rows):
        for j in range(0,cols):
            row_look_for_another_basic_variable = Testing_Tableau[(x+i)%rows].count('n.n.')

            for k in range(0,cols):
                col_look_for_another_basic_variable=0
                for h in range(0,rows):
                    if Testing_Tableau[(x+h)%rows][(y+k)%cols]=='n.n.':
                        col_look_for_another_basic_variable+=1
                    else:
                        continue
            good_row_count=Testing_Tableau[(x+i)%rows].count('good')
            good_col_count=0
            for h in range(0,rows):
                if Testing_Tableau[(x+h)%rows][(y+j)%cols]=='good':
                    good_col_count+=1
                else:
                    continue
            if ((x+i)%rows==x and (y+j)%cols==y):
                Testing_Tableau[(x+i)%rows][(y+j)%cols]='good'
            elif (Testing_Tableau[(x+i)%rows][(y+j)%cols]=='null' 
                or (row_look_for_another_basic_variable==0 and col_look_for_another_basic_variable==0) 
                or good_row_count>=2 or good_col_count>=2
                or ((x+i)%rows==i and (y+j)%cols==j and good_row_count<2 and good_col_count<2)):
                Testing_Tableau[(x+i)%rows][(y+j)%cols]='bad'
            else:
                Testing_Tableau[(x+i)%rows][(y+j)%cols]='good'
def Finding_Odds_and_Evens(rows,cols):
    Testing_Tableau[x][y]='even'
    for i in range(0,rows):
        for j in range(0,cols):
            even_row_count=Testing_Tableau[(x+i)%rows].count('even')
            odd_row_count=Testing_Tableau[(x+i)%rows].count('odd')
            even_col_count=0
            for k in range(0,rows):
                if Testing_Tableau[(x+k)%rows][(y+j)%cols]=='even':
                    even_col_count+=1
                else:
                    continue
            odd_col_count=0
            for h in range(0,rows):
                if Testing_Tableau[(x+h)%rows][(y+j)%cols]=='odd':
                    odd_col_count+=1
                else:
                    continue
            if Testing_Tableau[(x+i)%rows][(y+j)%cols]=='good':
                if even_col_count==1 or even_row_count==1:
                    Testing_Tableau[(x+i)%rows][(y+j)%cols]='odd'
                elif odd_col_count==1 or odd_row_count==1:
                    Testing_Tableau[(x+i)%rows][(y+j)%cols]='even'
                else:
                    for k in range(0,cols): #horizontal movement
                        if Testing_Tableau[(x+i)%rows][(y+k)%cols]=='even':
                            Testing_Tableau[(x+i)%rows][(y+j)%cols]='odd'
                            break
                        elif Testing_Tableau[(x+i)%rows][(y+k)%cols]=='odd':
                            Testing_Tableau[(x+i)%rows][(y+j)%cols]='even'
                            break
                        else:
                            for h in range(0,rows): #vertical movement
                                if Testing_Tableau[(x+h)%rows][(y+j)%cols]=='even':
                                    Testing_Tableau[(x+i)%rows][(y+j)%cols]='odd'
                                    break
                                elif Testing_Tableau[(x+h)%rows][(y+j)%cols]=='odd':
                                    Testing_Tableau[(x+i)%rows][(y+j)%cols]='even'
                                    break
                                else:
                                    continue
            else:
                continue
    print('\nevens and odds')
    for row in Testing_Tableau:
        print(row)
    min_odd=[]
    for f in range(0,rows):
        for g in range(0,cols):
            if Testing_Tableau[(f+x)%rows][(g+y)%cols]=='odd':
                min_odd.append(Basic_Var[(f+x)%rows][(g+y)%cols])
            else:
                continue
    print('min', min_odd)
    minimum=min_odd[0]
    for row in range(0,len(min_odd)):
        if min_odd[row]<=minimum:
            minimum=min_odd[row]
        else:
            continue
    print('min', minimum)
    for m in range(0,rows):
        for n in range(0,cols):
            if Testing_Tableau[(m+i)%rows][(n+j)%cols]=='odd':
                Basic_Var[(m+i)%rows][(n+j)%cols]=(Basic_Var[(m+i)%rows][(n+j)%cols]-minimum)
            elif Testing_Tableau[(m+i)%rows][(n+j)%cols]=='even':
                Basic_Var[(m+i)%rows][(n+j)%cols]=(Basic_Var[(m+i)%rows][(n+j)%cols]+minimum)
                latest='even'
            else:
                continue
    print('\nBasic Variable Tableau {}'.format(t))
    for row in Basic_Var:
        print(row)
    Basic_Var[x][y]=minimum
    return Basic_Var
def print_results():
    for h in range(0,rows):
        for k in range(0,cols):
            Basic_Var[h][k]=round(Basic_Var[h][k])
    print("\nFinal Tableau")
    for row in Basic_Var:
        print(row)
    final_basic_vars=[]
    final_costs=[]
    Total_Cost=0
    for i in range(0,rows):
        for j in range(0,cols):
            if Basic_Var[i][j]!=0:
                final_basic_vars.append(Basic_Var[i][j])
                final_costs.append(Cost[i][j])
                Expanded_Total_Cost=zip(final_basic_vars, final_costs)
                Total_Cost+=Cost[i][j]*Basic_Var[i][j]
            else:
                continue
    print('The total cost is: ${:0.2f}.'.format(Total_Cost))


Cost,rows,cols,Difference=Get_Data()

Basic_Var=deepcopy(Cost)
if Difference>0:
    rows=rows+1
    cols=cols
elif Difference<0:
    rows=rows
    cols=cols+1
else:
    rows=rows
    cols=cols
t=2
col_totals=[0]*cols
row_totals=[0]*rows
Set_Initial_Basic_Variables()
Form_Initial_Ui_and_Vi()
W_i=deepcopy(Basic_Var)
Form_Wi_and_Test()
W_i,min_Basic_Var,x,y=Find_Minimum()                        
Testing_Tableau=deepcopy(Basic_Var)
Set_New_Basic_Var(rows,cols)
Finding_Odds_and_Evens(rows,cols)
while True:
    t+=1
    Form_Ui_and_Vi()
    W_i=deepcopy(Basic_Var)
    dummy=Form_Wi_and_Test()
    W_i,min_Basic_Var,x,y=Find_Minimum()       
    Testing_Tableau=deepcopy(Basic_Var)
    Set_New_Basic_Var(rows,cols)
    Basic_Var=Finding_Odds_and_Evens(rows,cols)
print_results()