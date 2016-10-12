from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn import preprocessing
df = pd.read_csv('outlier.csv')
#Take unwanted columns for tranformations off
EIN = df.pop('EIN')
AS = df.pop('AS')
outlier = df.pop('Outlier') 
#Turn wanted observation and observations into numpy array
X = df.values
X_scaled = preprocessing.scale(X)
#B = np.random.randint(51354,size=20000)
#Fit the model multi demension space onto TSNE
transformation = PCA(whiten = True).fit_transform(X_scaled)
colors = outlier.replace(dict(zip(outlier.unique(),['b', 'r'])))
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(transformation[:,0], transformation[:,1], color = colors)
#rng = np.random.RandomState(42)
#clf = IsolationForest(max_samples=100, random_state=rng)
#xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
#Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
#Z = Z.reshape(xx.shape)
#plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)