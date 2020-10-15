from gurobipy import *
import random

def MutiObj(model, where):
    if where == GRB.Callback.MULTIOBJ:
        print (".................")
        print(model.cbGet(GRB.Callback.MULTIOBJ_OBJCNT))
        input()
    if where == GRB.Callback.MIPNODE:
        print ("*****************")
        print (model.cbGet(GRB.Callback.MIPNODE_NODCNT))
        input()

try:
    N = 20
    random.seed(1)
    
    #产生随机 Tmatrix 和 Cmatrix
    Tmatrix = {(i+1,j+1):random.randint(0,100) for i in range(N) for j in range(N)}
    Cmatrix = {(i+1,j+1):random.randint(0,100) for i in range(N) for j in range(N)}
    
    #定义 model
    m = Model('MultiAssignment')
    
    #添加变量
    x = m.addVars(Tmatrix.keys(), vtype=GRB.BINARY, name='x')
    
    #添加约束
    m.addConstrs((x.sum('*',j+1)== 1 for j in range(N)),'C1')
    m.addConstrs((x.sum(i+1,'*')== 1 for i in range(N)),'C2')
    
    #设置多目标 权重
    #m.setObjectiveN(x.prod(Tmatrix),  index=0, weight=0.1, name='obj1')
    #m.setObjectiveN(-x.prod(Cmatrix), index=1, weight=0.5, name='obj2')
    
    #设置多目标 优先级
    m.setObjectiveN(x.prod(Tmatrix),  index=0,  priority=1, abstol=0, reltol=0, name='obj1')
    m.setObjectiveN(-x.prod(Cmatrix), index=1,  priority=2, abstol=100, reltol=0, name='obj2')
    
    #设置logFile的名称
    m.setParam(GRB.Param.LogFile, 'MultiAssignmentLog.log')
    
    xxx = 1
    #启动求解
    m.optimize(MutiObj)

    #获得求解结果
    for i in Tmatrix.keys():
        if x[i].x>0.9:
            print ("工人 %d \t ----> \t 工作 %d" %(i[0], i[1]))
            
    for i in range(2):
        m.setParam(GRB.Param.ObjNumber, i)
        print('Obj%d = '%(i+1), m.ObjNVal)
        
    #将model输出到 lp格式文件中
    m.write('MultiAssinment.lp')
    
except GurobiError:
    print('Error reported')    