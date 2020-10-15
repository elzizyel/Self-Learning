<center><font size = 10>LightGBM</font></center>
## 1. 基础介绍

### 1.1 Leaf-wise (Best-first)的决策树生长策略

​	大部分决策树的学习算法通过level-wise 策略生长树, 如下图

![](./img/1.1-1.jpg)

​	但是LightGBM是通过leaf-wise的策略来生长树的。它会选择具有最大`delta loss`的叶节点来生长。相对Level-wise算法，leaf-wise可以减少更多的损失。

​	但是当sample size较小的时候，leaf-wise是有可能造成过拟合的。所以可以通过控制一系列参数来避免过拟合。如下图即为leaf-wise:

![](./img/1.1-2.jpg)



### 1.2 Categorical Vars的最优分割

​	在一般的ML之中，我们通常将categorical vars转变为one-hot encoding。然而对于树形结构这其实不是个很好的解决方案。因为对于一个基数较大的类别特征，树形会生长的非常不平衡，且需要很深的深度才能达到较好的准确率。

​	最好的解决方法是将特征类别划分为两个子集，对于有k种类别的categorical vars，共有$2^{k-1} - 1$种可能的划分，通过算法，寻找最优划分大约需要$k * log(k)$

​	其基本思想是根据训练目标的相关性对类别进行重排序。即根据累加值(sum_gradient / sum_hessian)重新对类别特征的直方图进行排序，然后再排好序的直方图中寻找最好的分割点。



## 2. 参数介绍

### 2.1 核心参数

- `objective` | default = `regression`, options = `regression`, `fair`, `binary`, `multiclass`, `xentropy`,…..
  - regression application
    - `regression_l2` , alias = `mean_squred_error`, `mse`
    - `regression_l1` , alias = `mean_absolute_error` , `mae`
  - binary - log loss
  - multiclass
    - `multiclass` , softmax函数, 应设置`num_class`
    - `multiclassova` , One-vs-All 二分类目标函数, 应设置`num_class`
- `bossting` | default = `gbdt` , optins = `gbdt` , `rf` , `dart` , `goss` 
  - `gbdt` , 传统梯度提升决策树
  - `rf` , 随机森林
- `train` | default = `""`
  - 训练数据集, LightGBM将使用这个数据集进行模型训练
- `valid` | default = `""`
  - 测试/验证用数据，LightGBM将使用这个数据集进行模型验证
  - 支持多验证数据集，以`,` 分割
- `num_boost_round` | default = `100` ， alias = `num_trees` , `num_iterations`
  - boosting的迭代次数 | 树形结构的树数量
  - 在内部，LightGBM对于`multiclass`问题设置`num_class * num_boost_round`棵树
- `learning_rate` | default = `0.1`
- `num_leaves` | default = `31`
  - 一棵树上叶子数



### 2.2 控制模型学习过程的参数

- `max_depth` | default = `-1`
  - 限制树模型的最大深度，可以用来处理过拟合
  - 限制了深度，树仍然可以通过leaf-wise生长
  - `-1` 意味着没有限制
- `min_data_in_leaf` | default = `20`
  - 一片叶子上数据的最小数量， 可以用来处理过拟合
- `min_sum_hessian_in_leaf` | default = `1e-3`
  - 一片椅子上最小hessian和，可以用来处理过拟合
- `feature_fraction` | default = `1.0`
  - 如果该参数小于`1.0`， 则LightGBM会在每次迭代中随机选择部分特征。例如若设置为`0.8` ，则在每棵树训练之前选择80%的特征
  - 可以用来加速训练
  - 可以用来处理过拟合
- `bagging_fraction` | default = `1.0`
  - 如果该参数小于`1.0` , 则LightGBM会在每次迭代中，不进行重采样的情况下随机选择部分数据
  - 可以用来加速训练
  - 可以用来处理过拟合
- `bagging_freq` | default = `0`
  - bagging的频率，`0`意味着禁用bagging。 `k`意味着每`k`次迭代执行bagging
- `early_stopping_round` | default = `0`
  - 如果模型在一个验证集中如果在`early_stopping_round`次循环中没有提升，则停止模型训练
- `lambda_l1` | default = `0`
  - L1正则
- `lambda_l2` | default = `0`
  - L2正则



### 2.3 IO 参数

- `ignore_column` | default = `""`
  - 在训练中忽略一些指定的列
  - 用数字做索引, e.g. `ignore_column = 0, 1, 2` 则column_index = 0, 1, 2 会被忽略
- `categorical_feature` | default = `""`
  - 指定分类特征
  - 用数字做索引, e.g. `categorical_feature = 0, 1, 2` 则column_index = 0, 1, 2 为分类特征
  - 为列名添加前缀`name:` e.g. `categorical_feature = name: c1, c2, c3` 意味着 c1, c2, c3是分类特征
  - 只支持 `int` type
  - 负值将被视为`NaN`



### 2.4 目标参数

- `is_unbalance` |  default = `false`
  - 用于`binary` 分类
  - 如果训练数据不平衡 设置为`true`



### 2.5 度量参数

- `metric` | default = {`l2` for regression}, {`binary_logloss` for binary classification}, …...
  - `l1` | alias = `mae` , `mean_absolute_error`
  - `l2` | alias = `mse` , `mean_squared_error`
  - `l1_root` | alias = `rmse` , `root_mean_squred_error`
  - `auc`
  - `binary_logloss`
- `metric_freq` | default = `1`
  - metric指标输出频率



## 3. 参数优化

### 3.1. 针对Leaf-Wise树的参数优化

1. `num_leaves` , 这个参数用来控制每一颗树上叶子的数量。我们可以将其设置为`num_leaves <= 2^(max_depth)` 
2. `min_data_in_leaf` , 这个参数用来控制每片叶子上的最小数据量，是用来处理模型过拟合非常重要的一个参数。它的值一般取决于训练样本的数量和`num_leaves`。将其设置的较大可以避免生成一个过深的树，但是有可能会导致欠拟合。实际应用中，对于大数据集，设置其为几百或者几千就足够了
3. `max_depth`， 这个参数用于控制树的最大深度， 可以用来处理过拟合问题



### 3.2. 更快的训练速度

1. 通过`baggin_fraction` 和 `baggin_freq` 参数来使用bagging方法
2. 通过`feature_fraction` 来进行特征的自抽样
3. 使用较小的`max_bin` | 个人感觉建议使用默认`255`
4. 使用并行学习



### 3.3. 更高的准确率

1. 使用较大的`max_bin` | 个人建议使用默认`255`
2. 使用较小的`learning_rate` 和 较大的 `num_iterations`
3. 使用较大的`num_leaves`



### 3.3 处理过拟合

1. 使用较小的`max_bin` | 个人建议使用默认`255`
2. 使用较小的`num_leaves`
3. 使用`min_data_in_leaf` 和 `min_sum_hessian_in_leaf`
4. 设置`baggin_fraction` 和 `bagging_freq`
5. 设置 `feature_fraction`
6. 使用`lambda_l1`, `lambda_l2`来使用正则



## 4. 其他/特性

### 4.1 LGB如何处理NA

​	It ignore the missing values when computing the split(二叉树的直方图的分割), then allocating all the data with missing valeues to whichever side of the split reduces the loss more.



### 4.2 LGB如何处理unbalanced data

​	在训练模型的时候对正/负样本设置权重，使得他们的数量*权重之后相等



### 4.3 LGB如何处理categorical vars

​	在树形结构中其实用one-hot encoding是相对不科学的，因为会生长出非常不平衡的树，然后要长的很深才能达到一个比较好的准确度。

​	事实上，最好的解决方法其实是将categorical vars分裂到两个子集里面去，然后因此我们有$2^{k-1}-1$种可能的分割方法。然后通过计算直方图的`sum_gradient / sum_hessian`我们可以得到最优的分割值，然后categorical vars就跟numerical features没有区别了。