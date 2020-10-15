# Maximize
#   obj1: x + y + 2 z
# Subject To
#   c0: x + 2 y + 3 z <= 4
#   c1: x + y >= 1
# Binary
#   x y z
# End

# Import Env
import gurobipy as gp
from gurobipy import GRB

try:
    # Create a new model
    m = gp.Model('mip1')

    t = 4

    # Create variables
    x = m.addVar(vtype=GRB.BINARY, name='x')
    y = m.addVar(vtype=GRB.BINARY, name='y')
    z = m.addVar(vtype=GRB.BINARY, name='z')

    # Set Objective
    m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

    # Add constraint
    m.addConstr(x + 2 * y + 3 * z <= t, 'c0')
    m.addConstr(x + y >= 1, 'c1')

    # Optimize Model
    m.optimize()

    # Print result
    for v in m.getVars():
        print('{} {}'.format(v.varName, v.x))
    print('Obj: {}'.format(m.objVal))

except gp.GurobiError as e:
    print('Error Code ' + str(e.errno) + ':' + str(e))

except AttributeError:
    print('Encountered an attribute error')
