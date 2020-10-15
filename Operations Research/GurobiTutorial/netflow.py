# Solve a multi-commodity flow problem. Two products ('Pencils', 'Pens')
# are produced in 2 cities ('Detroit', 'Denver') and must be sent to
# warehouses in 3 cities ('Boston', 'NewYork', 'Seattle') to satisfy demand ('inflow[h,i')
#
# Flows on the transportation network must respect arc capacity constraints ('capacity[i, j').
# The objective is to minimize the sum of the arc transportation costs ('cost[i, j')

# Import Envs
import gurobipy as gp
from gurobipy import GRB

# Base data
commodities = ['Pencils', 'Pens']
nodes = ['Detroit', 'Denver', 'Boston', 'New York', 'Seattle']

arcs, capacity = gp.multidict({
    ('Detroit', 'Boston'): 100,
    ('Detroit', 'New York'): 80,
    ('Detroit', 'Seattle'): 120,
    ('Denver', 'Boston'): 120,
    ('Denver', 'New York'): 120,
    ('Denver', 'Seattle'): 120
})

# Cost for triplets commodity-source-destination
cost = {
    ('Pencils', 'Detroit', 'Boston'): 10,
    ('Pencils', 'Detroit', 'New York'): 20,
    ('Pencils', 'Detroit', 'Seattle'): 60,
    ('Pencils', 'Denver', 'Boston'): 40,
    ('Pencils', 'Denver', 'New York'): 40,
    ('Pencils', 'Denver', 'Seattle'): 30,
    ('Pens', 'Detroit', 'Boston'): 20,
    ('Pens', 'Detroit', 'New York'): 20,
    ('Pens', 'Detroit', 'Seattle'): 80,
    ('Pens', 'Denver', 'Boston'): 60,
    ('Pens', 'Denver', 'New York'): 70,
    ('Pens', 'Denver', 'Seattle'): 30
}

# Demand for pairs of commodity-city
inflow = {
    ('Pencils', 'Detroit'): 50,
    ('Pencils', 'Denver'): 60,
    ('Pencils', 'Boston'): -50,
    ('Pencils', 'New York'): -50,
    ('Pencils', 'Seattle'): -10,
    ('Pens', 'Detroit'): 60,
    ('Pens', 'Denver'): 40,
    ('Pens', 'Boston'): -40,
    ('Pens', 'New York'): -30,
    ('Pens', 'Seattle'): -30
}


# Create Model
m = gp.Model('net_flow')

# Create Vars
flow = m.addVars(commodities, arcs, obj=cost, name='flow', )

# Arc-Capacity Constraints
m.addConstrs(
    (flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), 'cap'
)

# Equivalent version using Python looping
# for i, j in arcs:
#     m.addConstrs(
#         sum(flow[h, i, j] for h in commodities) <= capacity[i, j], 'cap[{}, {}]'.format(i, j)
#     )

# Flow-conservation constraints
m.addConstrs(
    (flow.sum(h, '*', j) + inflow[h, j] == flow.sum(h, j, '*') for h in commodities for j in nodes), "node"
)

# Alternate version:
# m.addConstrs(
#     (gp.quicksum(flow[h, i, j] for i, j in arcs.select('*', j)) + inflow[h, j] ==
#      gp.quicksum(flow[h, j, k] for j, k in arcs.select(j, '*'))
#      for h in commodities for j in nodes), 'node'
# )


# Compute the optimal solution
m.optimize()

# Print solution
if m.status == GRB.OPTIMAL:
    solution = m.getAttr('x', flow)
    for h in commodities:
        print('\nOptimal flows for %s' % h)
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h, i, j]))
