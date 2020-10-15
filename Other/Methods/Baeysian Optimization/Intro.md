
<center><font size = 10>Bayesian Optimization</font></center>
## 1. Intro

​		某些模型训练一次时间非常久，使用GridSearch或者RandomSearch就会很耗时。使用BO就可以尝试使用最少的步骤找出全局的最优参数。

​		假设模型为$f$ ，那么其运作原理为: 结合先验信念，更新以前取出的样本，得到更好的近似后验。



## 2. Surrogate Model(GPs)

​		BO使用的比较流行的替代模型是GPs(高斯过程)，它定义了一个先验函数，使用它去合并了目标函数的先验信念。

​		GPs的后验评估成本较低(高斯分布在条件作用下封闭)，可用于搜索在空间中使得采样会进步的点。结合bayes，它可以通过先验分布加上新的样本点，得出$f$ 的后验分布。

​		即，随机选一堆$X$ ，然后对他们在$f$ 中的映射$y$ ；因为GPs能从先验的$p(f|X)$ 得到后验的$p(f|X,y)$ ，那么相应的，我们再随机选一个/堆$X_*$， 我们可以由$p(f_*|X_*,X,y) = N(f_*|\mu_*,\sum_*)$ ， 得到对于$f$ 的后验分布, 为均值为$\mu_*$ 方差为$\sum_*$ 的高斯分布。



## 3. Acquisition Functions

​		AC里面比较流行的是使用maximum probability of improvement、expected improvement\ upper confidence bound.

​		AC的作用是找到Surrogate Model里面的$X_*$ 。它在exploitation和exploration之间有一个trade-off。Exploitation表示选出的X可能是在surrogate model里面结果好的，Exploration表示选出的X是探索性高的。		

​		对于目标函数$f$ ，可以从$x_t = argmax_xu(x|D_{1:t-1})$ 这个点采样，其中u为Acquisition Function、$D_{1:t-1} = {(x_1,y_1), ..., (x_{t-1}, y_{t-1})}$是从$f$ 中取出的t-1个样本。

​		

## 4. Baeysian Optimization

在调参的过程中，$x_t$ 为新的可用参数，$y_t$ 为训练处模型的结果值。与GridSearch相比，BO在尝试下一组超参数时, 会参考之前的评估结果, 可以省去很多时间.

贝叶斯优化的流程:

1. 根据GPs和AC ~ $x_t = argmax_xu(x|D_{1:t-1})$ 找到下一步最好的采样点$x_t$

2. 从目标函数$f$ 中 通过$y_t = f(x_t) + \epsilon_t$ 得到可能的噪音样本
3. 将选出的样本和值放入$D_{1:t} = {D_{1:t-1},(x_t,y_t)}$ ，然后更新GP
4. 重复以上步骤