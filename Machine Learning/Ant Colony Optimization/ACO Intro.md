<center><font size = 10>蚁群算法</font></center>
## 基础介绍

通过 S-ACO (Simple Ant Colony Optimization) 来介绍蚁群算法的基本概念

蚂蚁从巢穴出发, 会经过很多节点(components), 节点之间由很多路径(arcs)连接，最后蚂蚁到达有食物的地方。

每只蚂蚁会在arcs上留下信息素(Pheromone), 且蚂蚁会在选择往哪个components走的时候, 有更大概率选择Pheromone多的那条arcs。

所以对于S-ACO:

初始化: 在每条路径上先设置恒定的信息素量



**Pheromone Update**

这里面分为两步, 第一步是蚂蚁从巢穴到达终点, 第二步是蚂蚁从终点返回巢穴

蚂蚁从巢穴到达终点的时候不留下信息素, 只有在返回的时候才会留下信息素

在原路返回的时候, 蚂蚁会自动将循环的路径给删除掉(Loop Elimination)

比如 起点-2-5-3-2-5-7-8-终点 会被简化成 起点-2-5-7-8-终点, 以简化后的路径作为返回路径并且留下信息素



且简化后的路径越短, 留下的信息素越多

当蚂蚁k走过路径之后$\tau_{new} \leftarrow \tau_{orig} + \Delta \tau^k$ ($\tau$为信息素)

$\Delta \tau^k$的选择有多种方法, 一种是每只蚂蚁携带恒定的信息素，平均分配到路径上。

另一种是根据一个function，蚂蚁走的路径越短，在各条arc上留下的信息素越多(e.g. $\Delta \tau^k = \frac{1}{L^k}$)



总结: *在消除掉循环之后, 会根据本次解的质量, 在走过的路径上加上一定量的信息素, 解的质量越好, 留下的信息素越多; 所以之后的蚂蚁会更倾向于往路径短的地方走*



**Pheromone Trail Evaporate**

为了防止路径过快的收敛至局部最优, 我们需要随着时间将信息素给蒸发掉

在算法里的表达为:

每次蚂蚁从一个节点移动到下一个节点, 或者完成一次循环(从初始点-终点-初始点), 信息素**可以**根据下式衰减

$\tau \leftarrow (1 - \rho) \tau^k$ , where $\rho \in (0,1]$



**总结: 每只蚂蚁从初始点移动到终点, 根据本次路径的质量会在移动的路径上留下信息素, 且质量越高, 留下的信息素会越多; 蚂蚁在选择移动路径的时候, 路径上信息素越多, 被选择的概率就会越高, 使得蚂蚁更容易往路径短的地方走; 信息素会随着时间蒸发, 以防止陷入局部最优解**





## Max-Min Ant System(MMAS)

最大最小蚂蚁系统是目前来说效果最好的蚁群算法



**每条路径上的信息素有阈值上限与下限:**

当路径上的信息素被蒸发的少于下限了, 会强制使得该条路径上的信息素保持下限。这使得蚂蚁有可能去探索这条路径

当路径上留的信息素高于上限了, 会强制该条路径上的信息素维持上限。这使得算法不会收敛至局部最优值



每次找到了更短的路径, 信息素的上下限就会被更新

$\tau_{max}$ = $1 / {\rho C^*}$, where $C^*$ is the length of the optimal tour

所以每一次寻找到了更好的路径， $\tau_{max}$ 就要被更新

$\tau_{min} = \tau_{max} / a$, where a is  a parameter



**初始信息素以及蒸发限制:**

每条路径上的信息素在初始时均被设置成最大值, 且蒸发的系数被设置的很小, 这使得整个算法*more explorative*, 更具有探索性(每条路径被探索的概率都很大)

并且, 在多次迭代之后, 如果算法的结果没有变的更好/停滞住了, 我们会重新初始化各条路径的信息素(根据已知信息素最大值设置)



**更新信息素: **

$\tau_{new} \leftarrow \tau_{orig} +  \Delta \tau^{best}_{ij}$, where $ \Delta \tau^{best}_{ij} = \frac{1}{C^{best}}$

$C^{best}$ 可以是本次迭代中最好的蚂蚁, 也可以是所有迭代中最好的蚂蚁

根据经验一般小型的TSP用本次迭代最佳蚂蚁， 大型TSP用所有迭代最佳蚂蚁

当使用了local search, 一般都是用所有迭代中的最佳蚂蚁



**总结: 这上面的所有设置, 使得整套蚂蚁系统具有更高的探索性, 但是同样的, 我们应该设置更多的iteration让算法能找到更加好的solution**





## Iterated Local Search(迭代领域搜索)

领域搜索使得启发性算法(遗传、蚁群、退火、爬山等等)的搜索空间更大。

一般来说MMAS+ILS可以处理500以上城市的TSP问题; 而一般的蚁群算法只能处理50+城市的TSP问题



**k-opt**

The k-exchange neighborhood of a candidate solution s is the set of candidate solution s' that can be obtained from s by exchanging k solution components

*A set of k arcs is replaced by a different set of k arcs*

即更换k条路径, 选择这k次结果中最好的一次

就是原先蚂蚁选择了一条路径从初始点走到了终点, 我们将其定义为s

k-opt就是我们从中选择k条路径, 用另外的k条路径去代替它, 如果另外的路径结果更好, 则用结果更好的路径作为本次搜索的结果。

例如, 对于2-opt, 原来的路径为(b,c) (a,f) --> 被(a,c) (b,f) 代替

比如 A-B-C-D-E-F-G, 从中随机选两个点, 比方说B和F 则倒序成 A-B-E-D-C-F-G , 也为一种2-opt

![Box 3.2](/Users/elziz/Self-Learning/Machine-Learning/Ant Colony Optimization/Box 3.2.png) 

上图即为opt-3的一种替代方案

一般来说, opt-3有8种可选的替代路径, 其中4种其实本质上是opt-2, 另外4种才是opt-3。

理论上来说, 随着opt-k的k越大, 那么**最终**搜索出来的结果也就越好。



且在使用了领域搜索之后, $\beta$ 启发性因子的设置非常重要, 有可能$\beta = 0$的时候结果最好。





## AS的参数具体设置

1. 初始化:

   m只蚂蚁被放在随机选择的m个城市中, 每只蚂蚁通过如下概率选择下一个前往的城市:

$$
p^k_{ij}(t) = \frac{[\tau_{ij}(t)]^{\alpha}*[\eta_{ij}]^{\beta}}{\sum_{l\in N^k_i}[\tau_{il}(t)]^{\alpha} * [\eta_{il}]^{\beta}},\ \ \ \ if \ j \in N^k_i
$$

​       k 代表蚂蚁 K

​       $\tau$是路径上的信息素浓度

​       $\eta$是启发信息, 一般而言是路径的一个函数, 在TSP问题里, 均使用 $\eta = 1 / d_{ij}$

​       $N_i^k$是蚂蚁K的可以前往的节点, 即邻近的且没有被走过的节点



2. 当m只蚂蚁都完成了一次Hamiltonian cycles, 进行信息素的更新:

   先降低所有路径上的信息素 by a constant factor (evaporation)

   然后让每只蚂蚁都留下信息素

   arc(i, j)的信息素更新公式:

$$
\tau_{ij}(t+1) = \rho * \tau_{ij}(t) + \sum_{k=1}^{m}\Delta \tau_{ij}^k(t)
$$



​	其中, $\rho$是路径的信息素持久度, 所以 $1-\rho$即为evaporation, 且$0< \rho < 1$

​	$\Delta \tau_{ij}^k(t)$是蚂蚁K留在arc(i, j)里的信息素量

​	在AS中:
$$
\Delta \tau_{ij}^k(t) = 
\begin{cases}
1/L^k(t), \ if \ arc(i,j)\ is\ used\ by\ ant\ k\ in\ iteration t \\
0\ \ \ \ \ \ \ \ \ \ \ , \ otherwise
\end{cases}
$$
​	其中$L^k(t)$是蚂蚁K的总路程长度

​	总而言之, 就是这只蚂蚁完成一次旅程的总路程越短, 它在它走过的路径上留下的信息素越多





## MMAS 的参数设置

1. 初始化:

   所有路径的信息素都被设置为$\tau_{max}$ (在第一次循环之前, 可以先设定一个非常大的
   $\tau_{max}$, 然后在第一次循环过后强制更新$\tau_{max}$以及$\tau_{min}$)

   

   不管怎么更新信息素, 所有路径的信息素都在$[\tau_{min},\tau_{max}]$范围内

   其中, 
   $$
   \tau_{max} = \frac{1}{1-\rho}*\frac{1}{f(s^{opt})}
   $$
   $f(s^{opt})$ is the optimal solution value for a specific problem

   

   

   $$
   \tau_{min} = \frac{\tau_{max}(1 - \sqrt[n]{p_{best}})}{(avg-1)\sqrt[n]{p_{best}}}
   $$

   $n$是节点个数

   $avg=n/2$ , 最开始蚂蚁需要从n-1个点中选一个点走, 第二次要在n-2个点中选一个点走, 以此类推, 则就**平均**而言, 每一次选择下一个节点往哪走, 蚂蚁有$2/n$种选择

   $p_{best}$ 是当*MMAS*收敛时, 找到最佳方法的概率 - 我们通过控制它来选择$\tau_{min}$ - 算法收敛时, 蚂蚁在每一步都选择了**正确**的节点的概率

   当$p_{best} = 1$时, $\tau_{min} = 0$ | 即100%找到正确的道路, 其他错误道路的信息素都可以为0了

   

   每一次一个更好的$f(s^{opt})$被发现, $\tau_{max}(t)和\tau_{min}(t)$就会更新一次，所以每条路径上的信息素限制范围是在变化的




2. 蚂蚁移动概率

   m只蚂蚁被放在随机选择的m个城市中, 每只蚂蚁通过如下概率选择下一个前往的城市:
   $$
   p^k_{ij}(t) = \frac{[\tau_{ij}(t)]^{\alpha}*[\eta_{ij}]^{\beta}}{\sum_{l\in N^k_i}[\tau_{il}(t)]^{\alpha} * [\eta_{il}]^{\beta}},\ \ \ \ if \ j \in N^k_i
   $$
    k 代表蚂蚁 K

    $\tau$是路径上的信息素浓度

    $\eta$是启发信息, 一般而言是路径的一个函数, 在TSP问题里, 均使用 $\eta = 1 / d_{ij}$

    $N_i^k$是蚂蚁K的可以前往的节点, 即邻近的且没有被走过的节点




3. 信息素更新:

   在MMAS中, 每轮循环后只有一只蚂蚁走过的路径被用来更新信息素
   $$
   \tau_{ij}(t+1) = \rho * \tau_{ij}(t) + \Delta \tau^{best}_{ij}
   $$
   其中, $\Delta \tau_{ij}^{best} = 1 / f(s^{best})$ ; $s^{best}$既可以是iteraion-best 也可以是 global-best  solution

   我们可以固定使用一种方法, 也可以将其混合起来: 比如初始使用$s^{ib}$, 然后在一定次数的循环之后, 使用一次$s^{gb}$




4. PTS (Smoothing of the pheromone trails)
   $$
   \tau_{ij}^*(t) = \tau_{ij}(t) + \delta (\tau_{max}(t) - \tau_{ij}(t))
   $$
   其中,

   $\tau_{ij}^*$是修正后的信息素 , $\tau_{ij}$是修正前的信息素

   $\delta \in [0,1]$ | 当$\delta = 1 $ 即重新初始化路径的信息素到最大值; 当$\delta = 0$即关闭PTS

​        

​	一直开启PTS其实就相当于增大了tau_min - 所以不建议一直开启

​	当结果又很多次没有变好之后, 可以开启一下PTS, 以增加已经减到很小的路径信息素的值 |

​	毕竟就算$\rho=0.98$时, $\rho^{100} = 0.132 \ \ \rho^{200} = 0.017 \ \ \rho^{500} = 0.00004 $ | 循环次数增加, 信息素剩余量已经很小了

​	所以建议根据$\rho$来选择$\delta$和多少次循环用一次$\delta$ | 当$\rho=0.98$时, 建议200次循环内结果没变好, 启用一次PTS

​	

​	其实就是当算法收敛之后, 对目前的结果还不满意, 则在目前收敛的信息素状态下, 将他们放大一次, 路径上信

​	息素越小, 则放大的比例越大, 然后让算法再开始重新探索. 所以选择**多少次**结果没变好开启一次PTS很关键.




5. 各参数选择:

   $\rho \in [0.7, 0.99]$ | 随着$\rho$数值增加, 需要更多的iteration使得算法converge, 同时结果也会相对更好一点

   $p_{best} ≠ 1 $ | 很难说多少的$p_{best}$更好, 只能说使得$\tau_{min}$存在比不存在好 (使得蚂蚁更具探索性) 

   $\tau(1) = \tau_{max}$ 比 $\tau(1) = \tau_{min}$好

   $s^{ib}$比$s^{gb}$好 | 即单纯iteration-best比较好一点 | 但是实验也显示在大型搜索空间中, 混合使用两种方法使得算法能converge的更快 | 即用n次$s^{ib}$然后用一次$s^{gb}$, 如此重复, 效果更好 | 也可以前25次$s^{ib}$ 然后每50次混用$s^{ib}$和$s^{gb}$

   

6. FDC for TSP| fitness-distance corrlation | 一般与K-opt Search同时使用, 用来增加搜索的速度

   蚂蚁在选择下一个城市的时候, 把其他城市按离目前城市的距离从小到大排序, 将里目前城市最近的**N**个城市记为C1.

   查看C1是否在可行城市列表中存在, 将这些既在可行城市列表又离目前城市近的城市记为C2。

   若C2存在, 则按照概率从可行性列表中选一个城市走

   若C2不存在, 则在可行城市列表中, 选择离当前城市最近的城市当做下一个地点。

   

   然后, 在一只蚂蚁完成一次TSP循环之后, 跑一次k-opt search, 具体查看上方k-opt search的介绍

   


​    

   论文所用参数(供参考): |不是特别多的循环推荐用0.003这样很小的$\delta$ | 只要存在就很影响信息素更新

   $\beta = 2 \\ \alpha = 1 \\ m = n, where \ m \ is \ the \ number \ of \ ants \ and \ n \ is \ the \ number \ of \ nodes \\ \rho = 0.98 \\ p_{best} = 0.005 | \tau_{min} = \tau_{max}/2n \\ \delta = 0.5 \\ 10th \ s^{ib} \ with \ once \ s^{gb} \\ 3-opt$

   

   

​    

​    




​    

