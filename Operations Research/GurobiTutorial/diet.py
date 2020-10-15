import gurobipy as gp
from gurobipy import GRB

# Import data
categories, minNutrition, maxNutrition = gp.multidict({
    'calories': [1800, 2000],
    'protein': [91, GRB.INFINITY],
    'fat': [0, 65],
    'sodium': [0, 1779]
})

foods, cost = gp.multidict({
    'hamburger': 2.49,
    'chicken': 2.89,
    'hot dog': 1.50,
    'fries': 1.89,
    'macaroni': 2.09,
    'pizza': 1.99,
    'salad': 2.49,
    'milk': 0.89,
    'ice cream': 1.59
})

nutritionValues = {
    ('hamburger', 'calories'): 410,
    ('hamburger', 'protein'): 24,
    ('hamburger', 'fat'): 26,
    ('hamburger', 'sodium'): 730,
    ('chicken', 'calories'): 420,
    ('chicken', 'protein'): 32,
    ('chicken', 'fat'): 10,
    ('chicken', 'sodium'): 1190,
    ('hot dog', 'calories'): 560,
    ('hot dog', 'protein'): 20,
    ('hot dog', 'fat'): 32,
    ('hot dog', 'sodium'): 1800,
    ('fries', 'calories'): 380,
    ('fries', 'protein'): 4,
    ('fries', 'fat'): 19,
    ('fries', 'sodium'): 270,
    ('macaroni', 'calories'): 320,
    ('macaroni', 'protein'): 12,
    ('macaroni', 'fat'): 10,
    ('macaroni', 'sodium'): 930,
    ('pizza', 'calories'): 320,
    ('pizza', 'protein'): 15,
    ('pizza', 'fat'): 12,
    ('pizza', 'sodium'): 820,
    ('salad', 'calories'): 320,
    ('salad', 'protein'): 31,
    ('salad', 'fat'): 12,
    ('salad', 'sodium'): 1230,
    ('milk', 'calories'): 100,
    ('milk', 'protein'): 8,
    ('milk', 'fat'): 2.5,
    ('milk', 'sodium'): 125,
    ('ice cream', 'calories'): 330,
    ('ice cream', 'protein'): 8,
    ('ice cream', 'fat'): 10,
    ('ice cream', 'sodium'): 180
}

# Create Model
m = gp.Model('diet')

# Create Vars
# 创建key是食物，value待定的tupledict
buyNum = m.addVars(foods, name='buyNum', vtype=GRB.INTEGER)

# Create Objective
m.setObjective(buyNum.prod(cost), GRB.MINIMIZE)

# Create Constraints
# 来自于所有营养成分需要在其上下限之间
# 使用 '== [a, b]' 表示在[a,b]范围之内
m.addConstrs(
    (gp.quicksum(nutritionValues[f, c] * buyNum[f] for f in foods) == [
        minNutrition[c], maxNutrition[c]] for c in categories), "_"
)
# 也可用该方法来添加constraints
# m.addRange(expr, lhs, rhs, name)
# for c in categories:
#     m.addRange(
#         gp.quicksum(nutritionValues[f, c] * buyNum[f] for f in foods),
#         minNutrition[c], maxNutrition[c], c
#     )


def printSolution():
    '''
    :return: 优化结果
    '''
    if m.status == GRB.OPTIMAL:
        print('\nCost: %g' % m.objVal)
        print('\nBuy:')
        buyx = m.getAttr('x', buyNum)
        for f in foods:
            if buyNum[f].x > 0:
                print('%s %g' % (f, buyx[f]))
    else:
        print('No solution')


# Solve
m.optimize()
printSolution()

# Add constraints and Solve
print('\nAdding constraint: at most 5 servings of dairy')
m.addConstr(buyNum.sum(['milk', 'ice cream']) <= 6, 'limit_dairy')
m.optimize()
printSolution()
