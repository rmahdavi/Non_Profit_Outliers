from sklearn.manifold import TSNE
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest
df = pd.read_csv('outlier.csv')
#Take unwanted columns for tranformations off
EIN = df.pop('EIN')
AS = df.pop('AS')
outlier = df.pop('Outlier') 
#Turn wanted observation and observations into numpy array
X = df.values
B = np.random.randint(51354,size=10000)
X_sample = X[B,:]
outlier_sample  = outlier[B]
#Fit the model multi demension space onto TSNE
t_sne = TSNE(perplexity=100, learning_rate=10, n_iter=6000)
transformation = t_sne.fit_transform(X_sample)
colors = outlier_sample.replace(dict(zip(outlier_sample.unique(),['b', 'r'])))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(transformation[:,0], transformation[:,1], color = colors)
#rng = np.random.RandomState(42)
#clf = IsolationForest(max_samples=100, random_state=rng)
#xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
#Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
#Z = Z.reshape(xx.shape)
#plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)