from gurobipy import *

try:
    #分割的密度
    npts = 1000
    
    #定义model
    m = Model()               
    
    #添加变量
    x = m.addVar(ub=10, vtype=GRB.CONTINUOUS, name='x')
    
    #定义分割点
    px = []
    f = []
    for i in range(npts):
        px.append(10 * i / (npts - 1))
        f.append((px[i]*px[i])-2*px[i] + 3)
    m.setPWLObj(x, px, f)
    
    #启动求解
    m.optimize()
    
    #获得求解结果
    print('Obj: %g' % m.ObjVal)
    for v in m.getVars():
        print('%s %f' % (v.VarName, v.X))
    
    m.write("PWL.lp")

except GurobiError:
    print('Error reported') 