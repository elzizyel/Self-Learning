import gurobipy as gp

try:
    # read the lp_file
    m = gp.read('LP_Example.lp')

    # Optimize
    m.optimize()

    # Print result
    for v in m.getVars():
        print('{} {}'.format(v.varName, v.x))
    print('Obj: {}'.format(m.objVal))

except gp.GurobiError as e:
    print('Error Code ' + str(e.errno) + ':' + str(e))

except AttributeError:
    print('Encountered an attribute error')
