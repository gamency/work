
# coding: utf-8

# In[153]:

import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import pandas as pd
get_ipython().magic(u'matplotlib inline')


# In[152]:

# 准备训练数据：随机生成 包含两个特征的200个样本点
rng = np.random.RandomState(42)
X = 0.3 * rng.randn(100, 2) # 获得 100 x 2 维矩阵
# train test sample
X_train=np.r_[X+2, X-2] # 行合并这两个矩阵， np.c_是列合并


# In[155]:

clf =IsolationForest(n_estimators=100,max_samples=70,contamination=0.05 , random_state=rng) # 设定模型参数
clf.fit(X_train) # 训练


# In[169]:

# 预测,识别异常点
# 因为contamination=0.05， 即假设200个样本中有5%的比例是异常的（即10个）
y_pred_train = clf.predict(X_train) 
print pd.Series(y_pred_train).value_counts() 


# In[205]:

# 异常分数的分布
y_pred_proba = clf.decision_function(X_train)
h =plt.hist(y_pred_proba,bins=20, normed=True)
plt.show()


# In[172]:

# 生成5个孤立点进行预测
# 比较异常分数与阈值的大小，若低于阈值，则决策结果返回异常(-1)。
X_outliers = rng.uniform(low=-4, high=4, size=(5, 2))
print "阈值", clf.threshold_ # 若异常分数低于该阈值，则predict返回-1
print "预测异常分数", clf.decision_function(X_outliers) 
print "预测决策结果", clf.predict(X_outliers) 


# In[176]:

# 调整阈值，则决策结果也发生相应的变化
clf.threshold_=-0.1
print "阈值", clf.threshold_ # 若异常分数低于该阈值，则predict返回-1
print "预测异常分数", clf.decision_function(X_outliers) 
print "预测决策结果", clf.predict(X_outliers) 

