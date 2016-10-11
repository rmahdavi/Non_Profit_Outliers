import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn import svm

#Take form 990 extract from the IRS website in in a space-delimited, ASCII format and insert
#information into a dataframe 
#url = 'https://www.irs.gov/pub/irs-soi/15eofinextract990.dat.dat'
#df_form990extract = pd.read_csv(url, delim_whitespace = True)
#print "df_form990extract"
#print "Form 990 Extract Basic information below:" 
#print df_form990extract.info()
#print 'Functions available:' + ' ' + 'Feat' + '  '+' Zeroize'+ '  '+'abn_score'

#df_school = df_form990extract[df_form990extract.operateschoolsY70cd == 'Y']


sub = ['totrevenue > 1000000', 'totcntrbgfts > 500000']
#Takes the form 990 dataframe and list of query arguments in string format and queries the dataframe.
def subset(df,*args):
	for i in args:
		df = df.query(i)
	return df


def feat(df):
	EIN = df.EIN.values
	df_fr = pd.DataFrame(data = EIN, index = None, columns = ['EIN'])
	#Liabilities to Assets a measure of leverage
	df_fr['field1'] =  df.totliabend/df.totassetsend
	#Equity Ratio measure of the the portion of the total assets owned.
	#df_fr['field2'] = (capitalstktrstend+paidinsurplusend+retainedearnend)/totassetsend
	#Surplus Ratio Revenue minus Expenses divided by Revenue
	df_fr['field2'] = (df.totrevenue-df.totfuncexpns)/df.totrevenue
	#Deferred Expenses Ratio
	df_fr['field3'] = (df.prepaidexpnsend + df.othrassetsend)/df.totassetsend
	#Investment Return Ratio
	df_fr['field4'] = df.invstmntinc/df.totnetliabastend
	#Depreciation Rate as a portion of Fixed Assets before application of depreciation
	df_fr['field5'] = df.deprcatndepletn/(df.deprcatndepletn+df.lndbldgsequipend)
	#Deffered Revenue as a portion of Revenue
	df_fr['field6'] = df.deferedrevnuend/df.totrevenue
	#Compensation of officers
	df_fr['field7'] = df.compnsatncurrofcr/df.totassetsend
	df_fr['totrevenue'] = df.totrevenue
	df_fr['totcntrbgfts'] = df.totcntrbgfts
	#df_fr['field2'] =  (df.nonintcashend+df.svngstempinvend)/df.totassetsend
	#df_fr['field3'] = df.lndbldgsequipend/df.totassetsend
	#df_fr['field5'] = df.advrtpromo/df.totfuncexpns
	#df_fr['field6'] = df.compnsatncurrofcr/df.totassetsend
	#df_fr['field7'] = df.legalfees/df.totfuncexpns
	#df_fr['field8']= df.totrevenue/df.totfuncexpns
	return df_fr

#Converts all Nans and Infinities in the feature collums to zero.
#Note EIN (unique identifier) must be included as the first column in the Dataframe.
def zeroize(df):
	columns = df.columns
	for i in columns[1:]:
		df[i] = df[i].replace([np.inf, -np.inf], np.nan).fillna(0)
	return df

#Take in a list of EIN Numbers associated with normal foundations and creates a base to model on the behavior of these organizations
def Novelty_Detection(df,list):	
	df_novel = pd.DataFrame(data = None, index = list, columns = None)
	EIN = df.pop('EIN')
	Columns = df.columns
	X = df.values
	df = pd.DataFrame(data = Data, index = EIN, columns = Columns)
	df_novel = df_novel.join(df)
	X_novel = df_novel.values
	model = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)	
	dist_svm = model.fit(X_novel).decision_function(X)
	df['dist'] = dist_svm
	df = df.sort_values('dist')
	return df


# Insert Featurized DataFrame and computes Abnormality Scores useing Isolation Forests.  
def abn_score(df):	
	EIN = df.pop('EIN')
	X = df.values
	model = IsolationForest()
	abnormal_scores = model.fit(X).decision_function(X)
	df['EIN'] = EIN
	df['AS'] = abnormal_scores
	#df_AS = pd.DataFrame(data = [EIN], index = None, columns = ['EIN'])
	#df_AS['AS'] = abnormal_scores
	#df_AS = pd.concat([df_AS, df], axis = 1)
	df = df.sort_values('AS', ascending =True)
	return df

#plt.hist(series1, 100, range = [0,1.5], log = True)
#plt.show()
def main():
	pass


if __name__ == '__main__':
	main()

