## 1. 基础介绍

LP-Format 是用来读写记录线性规划的一种语法格式。相比于MPS-Format，它更加的易读，更符合人的自然书写格式。它的限制也很明显，一个LP-File不能保存多个模型。当读模型文件时，LP-Files不按列原先的顺序进行保存。

`source: https://www.gurobi.com/documentation/8.1/refman/lp_format.html`



## 2. 基础语法

### 2.0 基本概念

- 使用回车以及空格来作为分隔符
- 反斜线 \ 为comment开始的标志，在其之后的该行内容均被忽视
- 所有变量都需要有自己独特的名字，且变量名少于255个字符，并且不能包含任何数学符号、关键字、或以数字开头
  -  以英文字母开头就行，且不要用bounds、min这些有特殊含义的关键字
  - 比如 'x+y+z' 会被认为是一个变量名，而'x + y + z'会被认为是三个变量的一个表达式
- 其结构由几个部分构成，每一个部分表示优化模型内的一块逻辑。每一个部分以特殊的关键词开头，(如: Bounds、Subject To、Generals、End.....)并且必须以某一种固定的顺序出现，虽然里面几种特殊的部分是允许出现顺序不一的



### 2.1 Objective Section

​	LP-File出现的第一个部分必须是目标函数部分。这一部分由以下六个关键字开始['Minimize', 'Maxmize', 'Minimum', 'Maxmium', 'Min', 'Max']，且大小写不敏感。这些关键字可以单独出现，表示只有一个目标函数；也可以出现多次，表示这个模型有多个目标函数。

#### 2.1.1 Single-Objective Case

- 由一个一阶或者二阶的表达式构成

- 由 '名字' + ':' + '空格' + '表达式' 构成

- 表达式由 '+' 或者 '-' 符号进行分割，可以写在一行内，也可以写在多行内。以下两个例子等价

  - ```markdown
    obj1: x1 + 2 x2  + 4 x3 
    ```
  
  - ```markdown
    obj1: x1 + 2 x2
    + 4 x3
    ```

- 当表达式为二阶时，二阶的部分需要在 '[   ]' 方括号内。以下为需要写在方括号内的例子
  - 平方:  `2 x ^ 2` 
  - 积: `3 x * y`

- 例子

  - ```markdown
    Minimize
      obj: 3.1 x + 4.5 y + 10 z + [ x ^ 2 + 2 x * y + 3 y ^ 2 ] / 2 
    ```

#### 2.2.2 Multi-Objective Case

​	在多目标优化里，会伴随多个目标函数，其中每一个目标函数都有自己的子关键字。这其中子关键字里包含了目标函数的Name、Priority、Weight、AbsTol、RelTol。

- **具体的意思之后再详细了解，暂时还没有深入到多目标**

- 例子

  - ```markdown
    Minimize multi-objectives
    	obj1: Priority=2 Weight=1 AbsTol=0 RelTol=0
    		3.1 x + 4.5 y + 10 z
    	obj2: Priority=1 Weight=1 AbsTol=0 RelTol=0
    		10 x + 0.1 y
    ```



### 2.3 Constraints Section

​	LP-File出现的第二部分必须是限制部分。这一部分由以下四个关键字开始['Subject To', 'Such That', 'ST', S.T.']，且大小写不敏感。

#### 2.3.1 Normal Constaints Section

- 每一个限制条件由 '名字' + ':' + '空格' + ':' + '一阶表达式' + '[二阶表达式]' + '比较符号' + '数值' 构成

  - 比较符号: > 、 >= 、 = 、 < 、 <=
  - 在LP-format中，是不分别严格不等的。所以 > 和 >= 是等价的
  - 需注意，在表达式左侧不包含常数项，表达式右侧不包含变量。(需要把常数项放到表达式右侧)

- 例子

  - ```markdown
    c0: 2.5 x + 2.3 y + 5.3 z <= 8.1
    qc0: 3.1 x + 4.5 y + 10 z + [ x ^ 2 + 2 x * y + 3 y ^ 2 ] <= 10
    ```

#### 2.3.2 Indicator Constraints

- Indicator Constraint即指示器限制。它表示的是，给定一个二元变量等于0或1的情况下，需要满足的条件。

  - 由'name' + ':' + ' ' + 'binary variable' + ' ' + '=' + ' ' + '->' + '表达式'

  - 例子

    - ```mark
      c0: b1 = 1 -> 2.5 x + 2.3 y + 5.3 z <= 8.1
      ```

    - 即当二元变量b1等于1时，需要满足 2.5x+2.3y+5.3z<=8.1 的条件



###  2.4 Lazy Constraints Section

​	惰性约束部分可以是LP-File的下一个部分，但是它是**optional**的。它由关键字 ['Lazy Constarints'+ 'level']开始，其中level可以是1-3中的数字（当没有标明level时，默认其为1）。

- **具体的意思之后再详细了解，暂时还没有深入到惰性约束部分**

- 大概的意思是，求解器会先不管这一部分的限制条件，找到最优解之后，会再来看是否满足这些惰性约束部分，若满足则解成立，若不满足则会把违背的惰性约束部分放进约束部分，重新求解。

- 例子

  - ```mark
    Lazy Constraints
      c0: 2.5 x + 2.3 y + 5.3 z <= 8.1
    Lazy Constraints 2
      c1: 1.5 x + 3.3 y + 4.3 z <= 8.1
    ```



### 2.5 Bounds Section

​	LP-File的下一部分为边界部分，这一部分由以下关键字开始['Bounds']，且大小写不敏感。它里面有一系列变量的边界。

- `Inf` 为可以用于Bounds Section内的一种关键字, 表示无穷大

- `free` 为可以用于Bounds Section内的一种关键字，表示其无限制

- 该部分为**optional**的，因为默认所有变量都`0 < vars < Inf` 

- 例子

  - ```markdown
    Bounds
      0 <= x0 <= 1
      x1 <= 1.2
      x2 >= -Inf
      x3 free
    ```



### 2.6 Variable Type Section

​	该部分为指定变量的类型，可以使用的关键字有['Binary', 'Binaries', 'Bin', 'General', 'Generals', 'Gen', 'Semi-Continuous', 'Semis', 'Semi']，分别代表二分类、整数、半连续。如果一个变量有多个变量类型，则类型为最后一个指定的变量类型。

- 该部分为**optional**的，因为默认所有变量都为`continuous`的
- **`Semi-Continuous` 之后再详细了解。**

- 例子

  - ```markdown
    Binary
    	x y 
    Generals
    	z
    Semi-Continuous
    	a
    ```



### 2.7 Special Ordered Set Section (SOS Section)

- **用于分段线性函数的建模，之后再详细了解**



### 2.8 PWLObj Section

- **用于分段线性函数的建模,之后再详细了解**

​	

### 2.9 General Constraint Section

​	该部分捕获了更多的general constriants，这一部分由以下关键字开始['General Constraints', 'Gneral Constraint', 'Gencons', 'G.C.']，且大小写不敏感。

​	内部包含以下关键字['MIN', 'MAX', 'OR', 'AND', 'ABS']。且大小写不敏感。

- 通俗来讲，就是这一部分的限制条件又创建了一个新的变量，该变量依赖于其他变量生成，并且该变量可以放到Bounds、Constraints等等部分里

- 跟随着`MAX`、`MIN`的需要一个非空的变量或数值列表

- 跟随着`OR`、`AND` 的需要一个二元变量列表

- 跟随着`ABS` 的只有一个变量

- 例子

  - ```markdown
    General Constraints
     gc0: r1 = MAX ( x1 , x2 , x10 , 0.7 )
     gencons1: r2 = MIN ( y0 , 10 , y1 , r1 )
     and1: r = AND ( b1 , b2 )
     or1: r = OR ( b3 , b4 )
     GC14: xabs = ABS ( x )
    ```



### 2.10 End Section

​	该部分必为LP-File的最后一部分，表示终结。



## 3. 例子

```markdown
\* LP format Example *\
Maximize
  obj1: 3.1 x + 4.5 y + 10 z + [ x ^ 2 + 2 x * y + 3 y ^ 2 ] / 2
Subject To
  c0: x + y = 1
  c1: x + 5 y + 2 z <= 10
  qc0: x + y + [ x ^ 2 - x * y + 3 y ^ 2 ] <= 5
Bounds
  0 <= x <= 5
  z >= 2
Generals
  x y z
End
```























