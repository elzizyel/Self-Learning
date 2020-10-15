# 该部分为netflow.py的前置基础部分
# 主要是介绍了如何使用简洁的方式而不是for循环去创建与调用一些有多维含义的变量

# Import Env
import gurobipy as gp

# -----------------------------------------------------------------------------------
# --------------------------------- 性质介绍 -----------------------------------------
# -----------------------------------------------------------------------------------
# tuplelist和tupledict在使用select或者sum的时候，速度会比for循环快很多很多很多

# tuplelist的性质
# 1. 可以使用select去选择想要的pattern
#    其中'*'可以表示任意值
#    若某一部分以列表的形式表示，则代表这个列表内的任意值都可被选出
l = gp.tuplelist([(x, y) for x in range(1, 4) for y in range(1, 4)])
print("l.select(2, '*')", l.select(2, '*'))
print("l.select([1, 3], '*')", l.select([1, 3], '*'))
print("l.select('*', 2)", l.select('*', 2))

# tupledict的性质
# 1. 可以pack
names, lower, upper = gp.multidict(
    {'x': [0, 1],
     'y': [1, 2],
     'z': [0, 3]}
)
print('names: ', names)
print('lower: ', lower)
print('upper: ', upper)

# 2. 可以使用.sum() / .prod() 来获取其式子 之和/ 积之和
vars = gp.tupledict({
    (1, 1): 1,
    (1, 2): 2,
    (1, 3): 3,
    (2, 1): 4,
    (2, 2): 5,
    (2, 3): 6,
    (3, 1): 7,
    (3, 2): 8,
    (3, 3): 9
})
coeff = gp.tupledict({
    (1, 1): 2,
    (1, 2): 0.6,
    (1, 3): 3,
    (2, 1): 7,
    (2, 2): 5,
    (2, 3): 3,
    (3, 1): 1.4,
    (3, 2): 2.5,
    (3, 3): 0.1
})
# 即vars(1,1) + vars(2,1) +  vars(3,1)
print("vars.sum('*',1): ", vars.sum('*',1))

# 即 sum(coeff(x,y)*vars(x,y)) where x in all and y in all
print("vars.prod(coeff): ", vars.prod(coeff))

# 即coeff(2,1)*vars(2,1) + coeff(2,2)*vars(2,2） + coeff(2,1)*vars(2,3）
print("vars.prod(coeff, 2, '*'): ", vars.prod(coeff, 2, '*'))

# -----------------------------------------------------------------------------------
# --------------------------------- 应用展示 -----------------------------------------
# -----------------------------------------------------------------------------------

# 创建一组3*3的下标
# 其实使用gp.tuplelist 还是 现在使用的list均可以
l = [(x, y) for x in range(1, 4) for y in range(1, 4)]

# 创建模型
m = gp.Model('test')

# 将下标代表的变量加入模型
# 这一步将l转化为tupledict
d = m.addVars(l, name='d')

# 更新模型
m.update()

# d.select() 类似sql里的like, 选出符合函数内表示的变量
print("d.select('*', 3): ", d.select('*', 3))
print("d.select(3, '*'): ", d.select(3, '*'))
print("d.select([1, 2], 2): ", d.select([1, 2], 3))

# d.sum() 是select的进阶，即按规则选出后再相加
print("d.sum('*', 3): ", d.sum('*', 3))
print("d.sum(3, '*'): ", d.sum(3, '*'))
print("d.sum([1, 2], 2): ", d.sum([1, 2], 3))

# d.prod() 是sum的进阶, 即.sum()只能处理相加系数为1的情况
# 而.prod() 为按规则选出后，再按prod(X)内X的系数相加
# 其实这里用dict还是gp.tupledict均可行
coeff = {
    (1, 1): 2,
    (1, 2): 0.6,
    (1, 3): 3,
    (2, 1): 7,
    (2, 2): 5,
    (2, 3): 3,
    (3, 1): 1.4,
    (3, 2): 2.5,
    (3, 3): 0.1
}
print("d.prod(coeff): ", d.prod(coeff))
print("d.prod(coeff, 2, '*'): ", d.prod(coeff, 2, '*'))
print("d.prod(coeff, [1, 2], '*'): ", d.prod(coeff, [1, 2], [2, 3]))



