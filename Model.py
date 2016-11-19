import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn import svm


#Create a featurized DataFrame from raw form 990 extracted data DataFrame.
def feat(df,*args):
	'''
    INPUT: Form 990 extract DataFrame
    OUTPUT: Featurized DataFrame
    '''
	EIN = df.EIN.values
	df_fr = pd.DataFrame(data = EIN, index = None, columns = ['EIN'])
	#Executive Compensation
	df_fr['field1'] = df.compnsatncurrofcr/df.totassetsend
	#Leverage
	df_fr['field2'] = df.totliabend/df.totassetsend
	#Solvency
	df_fr['field3'] = (df.totrevenue-df.totfuncexpns+df.deprcatndepletn)/df.totliabend
	#Deferred Expenses Ratio
	df_fr['field4'] = (df.prepaidexpnsend + df.othrassetsend)/df.totassetsend	
	#Deferred Revenue Ratio
	df_fr['field5'] = df.deferedrevnuend/df.totrevenue
	#Depreciation Rate as a portion of Fixed Assets before application of depreciation
	df_fr['field6'] = df.deprcatndepletn/(df.deprcatndepletn+df.lndbldgsequipend)
	#Surplus Margin
	df_fr['field7'] = (df.totrevenue-df.totfuncexpns)/df.totrevenue
	#Fundraising Efficiency
	df_fr['field8'] = df.netincfndrsng/df.lessdirfndrsng
	#Dummy variables to keep as indentifier for future uses
	for category in args:
		df_fr[category] = df[category]
	return df_fr

#Subset on the data on givin paramaters
def subset(df,*args):
	'''
    INPUT: Dataframe
    OUTPUT: Queries on the DataFrame
    '''
	for q in args:
		df = df.query(q)
	return df	

#Converts all Nans and Infinities in DataFrame to zero
def clean(df):
	'''
    INPUT: Dataframe
    OUTPUT: Dataframe
    '''
	columns = df.columns
	for i in columns[1:]:
		df[i] = df[i].replace([np.inf, -np.inf], np.nan).fillna(0)
	return df

# Detects outliers from a population of non profit organizations
def abn_score(df, metrics):	
	'''
    INPUT: Dataframe, Metrics to use for outlier detection
    OUTPUT: Dataframe
    '''
	df_1 = pd.DataFrame()
	for i in metrics:
		df_1[i] = df[i]
	X = df_1.values
	model = IsolationForest(contamination = .01)
	fit_model = model.fit(X)
	abnormal_scores = fit_model.decision_function(X)
	predict = fit_model.predict(X)
	return abnormal_scores, predict

#Takes features of a small sample of non profit organizations 
#and detects outliers that behave abnormally from the sample
def Novelty_Detection(df,df_novel,metrics):
	
	'''
    INPUT: Clean featurized DataFrame, Dataframe of Novel Unique Identifiers, metrics to use for outlier detection
    OUTPUT: Series of distance from the svm hyperplane, Series of classified outlier vs. non-outlier
    '''
	EIN_metrics = ['EIN'] + metrics
	df_1 = pd.DataFrame()
	for i in EIN_metrics:
		df_1[i] = df[i]
	df_novel = df_novel.merge(df_1, on ='EIN', how = 'left')
	df_novel_clean = df_novel.drop_duplicates('EIN').dropna().reindex()
	del df_1['EIN']
	X = df_1.values
	del df_novel_clean['EIN']
	X_novel = df_novel_clean.values
	model = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)	
	fitted_model = model.fit(X_novel)
	dist_svm = fitted_model.decision_function(X)
	predict = fitted_model.predict(X)
	return dist_svm, predict



#Obtains IRS Form 990 Data from the IRS website.  Obtain only organizations above 1,000,000 in total revenue and 500,000 in contributions.  
#Featurizes the data and applies both a novelty detection model and abnormality detection model.
def main():
	url = 'https://www.irs.gov/pub/irs-soi/15eofinextract990.dat.dat'
	df_form990extract = pd.read_csv(url, delim_whitespace = True)
	df_novel = pd.read_csv('Novel_clean.csv')
	df_novel.columns = ['EIN']
	metrics = ['field1', 'field2', 'field3', 'field4', 'field5', 'field6', 'field7', 'field8']
	df = feat(df_form990extract,'totrevenue','totcntrbgfts')
	df = subset(df,'totrevenue>1000000', 'totcntrbgfts>500000' )
	df = clean(df)
	df['AS'], df['outlier_IF'] = abn_score(df,metrics)
	df['ND'], df['outlier_SVM'] = Novelty_Detection(df,df_novel,metrics)
	return df
	

if __name__ == '__main__':
	main()

