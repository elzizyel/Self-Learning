<center><font size = 10>Imbalance Data</font></center>



# 1. 原因

​		对单纯的分类模型而言，因为模型的训练过程是让训练集上整体的偏差最小。所以如果训练集上负例特别多，而正例特别少，那么只要模型把所有样本都预测为负例，则整体上偏差就会很小，相当于牺牲了正例。但是在欺诈检测等等场景这事是不能被接受的。

​		所以最终评估模型的方法不应该是`Accuracy`而应该是`NE`/`F1`/`Recall`/`Precision`等指标



# 2. 解决方法

### 2.1 过采样 | OverSampling

- 方法

  - 对少数类样本进行随机镜像以增加少数类样本的数量

- 适用场景

  - 数据相对不是很充足

- 优点

  - 不丢失信息

- 缺点

  - 容易导致过拟合，因为没有给少数类增加任何新的信息

- 代码

  - ```python
    from imblearn.over_sampling import RandomOverSampler
    ros=RandomOverSampler(random_state=1024)
    X_resample, y_resample = ros.fit_sample(X_orig, y_orig)
    ```



### 2.2 欠采样 | UnderSampling

- 方法

  - 对多数类样本进行删减，以保持数据集的平衡

- 适用场景

  - 数据相对充足

- 优点

  - 模型训练速度变快

- 缺点

  - 丢失信息

- 代码

  - ```python
    from imblearn.under_sampling import RandomUnderSampler
    #通过设置RandomUnderSampler中的replacement=True参数, 可以实现自助法(boostrap)抽样
    #通过设置RandomUnderSampler中的ratio参数,可以设置数据采样比例
    rus=RandomUnderSampler(ratio=0.4,random_state=0,replacement=False) #采用随机欠采样（下采样）
    X_resample, y_resample = rus.fit_sample(X_orig, y_orig)
    ```



### 2.3 SMOTE 

- 方法

  - 对于少数类中的每一个样本，计算与其相邻的K个样本的欧氏距离(相当于KNN)
  - 根据样本不平衡比例设置一个采样倍率，记为N。
  - 对于每一个少数类样本，都从其K邻近样本点中随机选取一个样本点，将两者连线，新样本点为线中随机一点。重复该步骤N次。
    - 相当于$X_{new} = X_{orig} + rand(0,1)*(X_{KNN} - X_{orig})$

- 优点

  - 相当于过采样的一种改进迭代，在镜像少数类样本点时加入了一定的噪音

- 缺点

  - 存在一定盲目性，在做该算法时序确定K的值
  - 无法克服非平衡数据的数据分布问题。如果选取的少数类样本在少数类样本的边缘，则该少镜像+噪音产生的样本点可能会处在多数类样本与少数类样本中间或者直接在多数类样本内。导致模型无法很好的区分出正负例的边界，样本重叠
  - 仅适用于X均为连续型变量且无缺失值的情况(因为要计算欧式距离)

- 代码

  - ```python
    from imblearn.over_sampling import SMOTE
    smote = SMOTE(ratio='auto', random_state=1024, k_neighbors=5, kind='regular')
    X_resample, y_resample = smote.fit_sample(X_orig, y_orig)
    ```



### 2.4 Borderline-SMOTE

- 方法

  - 对于少数类中的每一个样本，计算与其相邻的K个样本的欧氏距离(相当于KNN)
  - 根据样本不平衡比例设置一个采样倍率，记为N。
  - 对于每一个少数类样本，都将其分为如下三类
    - Safe: 少数类样本KNN的样本点一半以上为少数类样本
    - Danger: 少数类样本KNN的样本点一半以上为多数类样本(视其为在少数类样本的边界)
    - Noise: 少数类样本KNN的样本点全为多数类样本 ，视为噪音
  - 仅对Danger点生成新样本
    - Borderline1
      - 选取与该Danger样本连线的KNN样本需要是少数类样本
    - Borderline2
      - 选取与该Danger样本连线的KNN样本可以是任何样本

- 优点:

  - 相比SMOTE，该方法更偏向于在少数类与多数类样本之间生成样本，即在少数类样本的边界生成样本，解决了SMOTE可能会在多数类样本点上(或附近)生成负样本的问题

- 代码

  - ```python
    from imblearn.over_sampling import SMOTE
    # kind = 'borderline1' / 'borderline2'
    # m_neighbors ~ 用于判断多少数量内的少数样本量呗判断为Danger样本
    bsmote = SMOTE(ratio='auto', random_state=1024, k_neighbors=5, m_neighbors=10, kind='borderline1')
    X_resample, y_resample = bsmote.fit_sample(X_orig, y_orig)
    ```



### 2.5 ADASYN 

- 方法

  - 记少数类样本数量为$X_n$, 多数类样本数量为$P_n$
  - 计算需要合成的样本数量: $G = (P_n - X_n)*\beta$, $\beta \in [0, 1]$。 当$\beta$为1时，则表示生成之后正负样本比例1:1
  - 对每一个少数类样本，用欧式距离计算KNN，这K个邻近样本内有$\Delta_n$个多数类样本，记多数类样本在K中的比例为$r = \Delta_n / K$
  - 对$r$进行标准化，$\hat{r_i} = r_i / \sum_{i=1}^{X_n}r_i$。即计算出这个样本的r比例在总体r比例中的占比
  - 计算每一个少数类样本需要合成的样本数量 $n_i = \hat{r_i} * G$
  - 对每一个少数类样本周围的K邻近样本中随机选择一个少数类样本，使用SMOTE方法产生样本，即连线再在先当中随机选一点
  - 重复上述方法直到满足该少数类样本需要生成的样本数量

- 优点

  - 在少数类样本周围多数类样本较多的地方，生成更多的少数类样本。与Borderline-SMOTE在边界生成样本点的思想非常接近

- 缺点

  - 与SMOTE一样，因为要计算欧式距离，所以只能对X均为连续型变量且非空的数据集使用

- 代码

  - ```python
    from imblearn.over_sampling import ADASYN
    ada = ADASYN(ratio='auto', random_state=1024, k_neighbors=5)
    X_resample, y_resample = bsmote.fit_sample(X_orig, y_orig)
    ```

