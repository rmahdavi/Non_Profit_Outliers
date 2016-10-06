import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

#Take form 990 extract from the IRS website in in a space-delimited, ASCII format and insert
#information into a dataframe 
url = 'https://www.irs.gov/pub/irs-soi/15eofinextract990.dat.dat'
df_form990extract = pd.read_csv(url, delim_whitespace = True)
print "df_form990extract"
print "Form 990 Extract Basic information below:" 
print df_form990extract.info()
print 'Functions available:' + ' ' + 'Feat' + '  '+' Zeroize'+ '  '+'abn_score'

#df_school = df_form990extract[df_form990extract.operateschoolsY70cd == 'Y']

#1. Total Assets to Liabilities
#totassetsend/totnetliabastend
#2. Total Cash to Assets
#nonintcashend+svngstempinvend/totassetsend
#3. Total Plant, Property, and Equipment to Assets
#lndbldgsequipend/totassetsend
#4. Invesmnet Income to investments
#invstmntinc/(invstgovtoblig+invstcorpstk+invstcorpbnd+totinvstsec+mrtgloans)
#5. Total Functional Expenses to total expenses
#totfuncexpns/totexpns
#6. Compensation of Officers to Total Assets
#(compofficers)/totassetsend
#7. Legal Fees as a percentage of total fees
#legalfees/totexpnspbks
#8. Tax penality as a portion of total taxes
#estpnlty/taxdue
#9. Capital Gain as a portion of the fair market value of total assets
#totexcapgnls/fairmrktvaleoy
#10. Total Revenue to Total Expenses
#totrcptperbks/totexpnspbks

def feat(df):
	EIN = df.EIN.values
	df_fr = pd.DataFrame(data = EIN, index = None, columns = ['EIN'])
	df_fr['field1'] =  df.totassetsend/df.totnetliabastend
	df_fr['field2'] =  (df.nonintcashend+df.svngstempinvend)/df.totassetsend
	df_fr['field3'] = df.lndbldgsequipend/df.totassetsend
	df_fr['field4'] = df.invstmntinc/(df.invstgovtoblig+df.invstcorpstk+df.invstcorpbnd+df.totinvstsec+df.mrtgloans)
	df_fr['field5'] = df.totfuncexpns/df.totexpns
	df_fr['field6'] = df.compofficers/df.totassetsend
	df_fr['field7'] = df.legalfees/df.totexpnspbks
	df_fr['field8'] = df.estpnlty/df.taxdue
	df_fr['field9'] = df.totexcapgnls/df.fairmrktvaleoy
	df_fr['field10']= df.totrcptperbks/df.totexpnspbks
	return df_fr

#Converts all Nans and Infinities in the feature collums to zero.
#Note EIN (unique identifier) must be included as the first column in the Dataframe.
def zeroize(df):
	columns = df.columns
	for i in columns[1:]:
		df_1[i] = df_1.field1.replace([np.inf, -np.inf], np.nan).replace([np.nan],0)
		
# Insert Featurized DataFrame and computes Abnormality Scores useing Isolation Forests.  
def abn_score(df):	
	EIN = df.pop('EIN')
	X = df.values
	model = IsolationForest()
	abnormal_scores = model.fit(X).decision_function(X)
	df_AS = pd.DataFrame(data = EIN, index = None, columns = ['EIN'])
	df_AS['AS'] = abnormal_scores
	return df_AS.info()

#plt.hist(series1, 100, range = [0,1.5], log = True)
#plt.show()
def main():
	feat()
	zeroize()
	abn_score()


if __name__ == '__main__':
	main()

