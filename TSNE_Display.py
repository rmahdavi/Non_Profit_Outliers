import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.manifold import TSNE
import seaborn as sns


#Selects a sample size to use for the tsne display.  TSNE is computionaly intensive so its recommend to take a sample.
def sample(ssize):
	'''
    INPUT: Sample size of the population
    OUTPUT: List of sample by index
    '''
	samplelist = np.random.randint(51354,size=ssize)
	return samplelist

#Performs the TSNE calculation, reducing the demensionality for two demensional display.
def tsne_calc(df,samplelist,metrics):

	'''
    INPUT: Dataframe including outlier model results, list respresenting sample selection that will be computed, list of factors that demensions will be reduced.
    OUTPUT: 2 by sample size array indicating axis position for tsne display
    '''
	df_1 = pd.DataFrame()
	for i in metrics:
		df_1[i] = df[i]
	X = df.values
	X_scaled = preprocessing.scale(X)
	X_sample = X_scaled[samplelist,:]
	t_sne = TSNE(perplexity=30, learning_rate=1000	, n_iter=1000)
	transformation = t_sne.fit_transform(X_sample)
	return transformation

#Displays the results of the TSNE display
def display(transformation,identifier,samplelist):
	'''
    INPUT: TSNE Transformed data, series indiciating what is and isn't an outlier, list respresenting sample selection
    OUTPUT: 2 by sample size array indicating axis position for tsne display
    '''
	sns.set(style="white", color_codes=True)
	identifier_sample = identifier[samplelist]
	colors = identifier_sample.replace(dict(zip(identifier_sample.unique(),['b', 'r'])))
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(transformation[:,0], transformation[:,1], color = colors, s = 3 )

#Takes in the modeled results with the featurized data and computes a display indicating positional relationship between nonprofits in a two demensional display
def main():
	filepath = 'Data/results.csv'
	df = pd.read_csv(filepath)
	outlier_IF = df.pop('outlier_IF')
	outlier_SVM = df.pop('outlier_SVM')
	metrics = ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'field8']
	samplelist = sample(10000)
	transformation = tsne_calc(df, samplelist, metrics)
	display(transformation, outlier_IF, samplelist)
	plt.show()


if __name__ == '__main__':
	main()











