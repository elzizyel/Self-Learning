- Scalar | a single numeric feature
- Vector | list of scalars
- Spaces | a vector space



[TOC]



# 1. Numeric Features



## 1.1 General Knowledge

  1. Check whether the magnitude matters. 

      - Important for automatiaclly acccrued numbers such as COUNTs.
 	2.  Smooth function such like 3x+1 | Check do they span several orders of manitude.
      - *Normalize* features if the methods uses the **Euclidean distance** such as k-means/ RBF kernel......
      - *Normalize* features to make the output stays on an expected scale
      - Smooth function such like 3x+1 of input features are sensitive to the scale of the input
	3.  Logical Function such like *Tree Model* | Not sensitive to input feature scale
     - The only exception is if the scale of the input grows over time
     - Such like the feature will grow outside of the range that the tree was trained on
     - For that case, we might need to rescale the inputs periodically *OR* bin-counting methods
	4.  The distribution of numeric features | Some methods care the distribution of input features
     - LR asumes that errors are distributed like Gaussian. 
     - Use power transform like log-transform for above point no longer holds.





## 1.2 Dealing with Counts



#### 1.2.1 Binarization

<img src="/Users/elziz/Self-Learning/Machine Learning/Feature Engineering/FeatExp/Pics for intro/Deal_Counts_1.png" alt="Histogram of listen counts in a player of Millon Song Dataset" style="zoom:50%;"/>

​	Take listening song as an example, users have different listening habits. Some might put their facorite songs on infinite loop, while others might savor them only on special occasions. For a song recommendation system, **we can binarize the count and clip all counts greater 1 to 1**.

​	So we consider if the user listened to a song at least once, then we count it as the user liking the song.

​                                **Summarize: choose a threshold and binarize the COUNTs feature**



#### 1.2.2 Quantization or Binning

​	In Figure 2-3. we can see that raw counts span several orders of manitude. In model like LR, a large count in one element of the data vector would outweigh the similarity in all other elements.

There are two way to fix this problem

1. Fixed-width binning
   - Each bin contains a specific numeric range
   - 0-12 | 12-17 |18-24| 25-34 …… | Customize the bin width
   - 0-9 | 10-99 | 100-999 | 1000-9999 etc | This bin widths grow exponentially
   - Log-transformation COUNTs
2. Quantile binning
   - If there are large gaps in the counts, it may be many empty bins with no data for fixed-width binning
   - Can use 0.25 quantile, 0.5 quantile, 0.75 quantile as threshold

<img src="/Users/elziz/Self-Learning/Machine Learning/Feature Engineering/FeatExp/Pics for intro/Deal_Counts_1.png" alt="Histogram of listen counts in a player of Millon Song Dataset" style="zoom:50%;" />





## 1.3 Power-Transformation

<img src="/Users/elziz/Self-Learning/Machine-Learning/Feature Engineering/Pics for intro/Log_trans.png" alt="drawing" width="500"/>

1. Make variance constant
2. Other Power-Transformation are all variance-stabilizing transformations
3. Box-Cox Transformation are also  $$y^{(\lambda)} = \left\{\frac{\frac{y^{\lambda} - 1}{\lambda}，\lambda≠0}{log(y), \lambda = 0} \right\}$$
4. Some of above transformation can only used by positive features, so if we want to use negative features with these methods, we can transfer negative features into Euclidean distance to the min of the feature. Transfer this feature to positive, then do the vairance constancy transformation.





## 1.4 Feature Scaling or Normalization

​	Some feature may increase without bound such like COUNTs. Models that are smooth function of the input, such as linear regression, logistic regression, or anything that involves a matrix, are affected by teh scale of the input. Tree-based models care less about that. If model is sensitive to the scale of input features, feature scaling may help.

#### 1.4.1 Min-Max Scaling

​	Use the scaled of the Euclidean Distance to scale the feature into [0,1]

$$x' = \frac{x - min(x)}{max(x)-min(x)}$$

<img src="/Users/elziz/Self-Learning/Machine-Learning/Feature Engineering/Pics for intro/min-max.png" alt="drawing" width="500"/>



#### 1.4.2 Standardization

​	Scaled feature has a mean of 0 and variance of 1. If the original feature has a Gaussian distribution, then the scale feature does too.

$$x' = \frac{x - \bar{x}}{\sigma_{x}}$$

<img src="/Users/elziz/Self-Learning/Machine-Learning/Feature Engineering/Pics for intro/standardize.png" alt="drawing" width="500"/>

### 

#### 1.4.3 L2 Normalization

$$x' = \frac{x}{||x||_2}$$

$$||x||_2 = \sqrt{x_1^2 + x_2^2 + ... + x_m^2}$$

<img src="/Users/elziz/Self-Learning/Machine-Learning/Feature Engineering/Pics for intro/l2-norm.png" alt="drawing" width="500"/>





# 2. Categorical Features

## 2.1 Encoding Categorical Variables

#### 2.1.1 One-Hot Encoding

​	Create new k variables to represent this one categorical variable. And this categorical variable have k category.

		- Pros: 

1. Redundant, allows for multiple valid models for the same problem.  
2. Each feature clearly corresponds to a cateogry, missing data can be encoded as all-zeros vector

|               | e1   | e2   | e3   |
| ------------- | ---- | ---- | ---- |
| San Francisco | 1    | 0    | 0    |
| New York      | 0    | 1    | 0    |
| Seattle       | 0    | 0    | 1    |



#### 2.1.2 Dummy Coding

​	Create new k-1 variables to represent this one categorical variable. And this categorical variable have k different type.

- Cons:

1. Cannot easily handle missing data

|               | e1   | e2   |
| ------------- | ---- | ---- |
| San Francisco | 1    | 0    |
| New York      | 0    | 1    |
| Seattle       | 0    | 0    |



#### 2.1.3 Effect Coding

 	If you have several categorical variables in a model, it often doesn't make much difference between dummy coding and effect coding. But if there are **two categorical variables have an interaction**, then effect coding may provide some benefits.

|               | e1   | e2   |
| ------------- | ---- | ---- |
| San Francisco | 1    | 0    |
| New York      | 0    | 1    |
| Seattle       | -1   | -1   |



## 2.2 Dealing with Large Categorical Variables

#### 2.2.1 Feature Hashing

​	The goal of Feature Hashing is reduce the dimension of a N-dimension feature into M-dimension feature(N > M), and try it best do not lose info.

- Pros:

1. Easy to implement
2. Makes model training cheaper
3. Easily adaptable to new categories
4. Easily handles rare categories
5. Feasible for online learning

- Cons

1. Only suitable for linear or kernelized models
2. Hashed feature not interpretable
3. Mixed reports of accuracy



#### 2.2.2 Bin-Counting

- Pros:

1. Smallest computational burden at training time
2. Enables tree-based models
3. Relatively easy to adapt to new categories
4. Handles rare categories with back-off or count-min sketch
5. Interpretable

- Cons:

1. Requires historical data
2. Delayed updates required, not completely suitable for online learning
3. Higher potential for leakage





