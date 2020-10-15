<center><font size = 10>Gurobi Tutorial</font></center>

[toc]



## 1. Gurobi 建模基本流程概念

### 1. 建模基本流程

1. Problem Instance: 待优化的问题
2. Model Gnerator: 将数据组合成模型，产生计算机模型对象

3. Model Instance: 存在于内存的一个完整数学模型
4. Gurobi Optimizer: Gurobi 优化求解
5. Solution Retrieval: 根据需要读取优化结果
6. Analysis: 对结果进行分析 (敏感度分型等)
7. 重复Step1-6，直到获得理想结果



### 2. 建模基本概念

1. Parameter

	- 控制优化器的行为，需要在优化启动前设置
2. Attributes

	- 控制模型(包括模型、变量、约束、目标等对象)的特性
	- 例如，一个模型里面有`Constraints` 、 `Variables` 、 `Special Ordered Sets` 这些Attributes，而这些东西自己本身也有一些Attributes
3. Enviroment

	- 一个环境内可以有多个模型
	- 包含模型和全局参数的一个容器，也是许可控制的节点
	- 在Python中，环境会根据默认参数自动建立，也可手动更改这些环境



### 3. 建模过程

​	所有建模流程均以一下流程进行，不建议混合在一起。若混合在一起则会导致模型运行变慢。

1. 创建模型
	- m = gp.Model()
2. 创建所有变量	
	- m.addVar()
	- m.addVars()
3. 设置目标函数
   - m.setObjective()
4. 创建所有限制条件
   - m.addConstr()
   - m.addConstrs()
5. 运行求解器
   - m.optimize()





## 2. Tuplelist / Tupledict

### 1. 简介

​	在优化建模过程中，经常需要对下标数据进行挑选组合。但是Python的 list / tuple / dict 用来做这件事情的时候，就需要用到循环+if进行筛选，效率非常低，所以需要采用Gurobi的扩展对象 `Tuplelist` 和 `Tupledict` 来做这件事情



### 2. 特点

1. `tuplelist` 
   - 用于建立下标的完整集合
   - 可以使用 `.select()` 去搜索所需的内容
     - '*' 代表任意匹配项
     - ['X', 'Y'] 代表可以匹配 [] 内任意一个元素
     - 如 `.select([1,2], '*')` 即代表搜索出第一个元素为1或2，第二元素任意的下标组合

2. `tupledict`
   - 用于建立变量
   - 可用使用 `.quicksum()` / `.prod()`  对变量进行加减乘的操作
- `quicksum` 其实就是相当于一个$\sum$符号, 其函数里面的就是在这个$\sum$循环内
  
3. List Comprehension
   - 用于列表解析for语句，即我们常在限制条件里写的 $\forall$
   - 例如
     - $\sum_{i \in I} x_{i,j} <= 1 \ \ \ \forall j \in J$
     - m.addConstrs( (x.sum('*', j <= 1 for j in J)), name = 'con' )



## 3. SOS - Special Ordered Set

- SOS1
  - 在集合内的一系列变量中，只有一个为非零变量
  - 即$\{y_1, y_2,...,y_m\}$为SOS1时，仅有一个$y_j$非0
  - 在线性规划中使用SOS能使得求解的速度更快
  - 例子
    - 现在要从5个仓库中选一个出来，每一个仓库有各自的cost和size
    - 设x1, x2, ...., x5为是否选对应仓库 (则xi为SOS1)
    - 式子
      - $cost = 100x_1 + 180x_2 + 320x_3 + 450x_4 + 600x_5$
      - $size = 10x_1 + 20x_2 + 40_x3 + 60x_4 + 80x_5$
      - $x_1 + x_2 + x_3 + x_4 + x_5 = 1$ (即SOS Constraint)

- SOS2
  - 在集合内的一系列变量中，最多只有两个非零变量， 如果存在两个非零变量，则他们必须在集合内是邻近的
  - 即$\{y_1, y_2,...,y_m\}$为SOS2时，最多有两个相邻的$y_j, y_{j+1}$非0；当然，只有一个非零或没有非0亦可存在



- 仅支持最多两个变量相乘(或二次方)








