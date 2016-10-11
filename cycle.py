import Data_Set as DS 
import pandas as pd

url = 'https://www.irs.gov/pub/irs-soi/15eofinextract990.dat.dat'
df_form990extract = pd.read_csv(url, delim_whitespace = True)
df = DS.feat(df_form990extract)
df = df.query('totrevenue > 1000000')
df = df.query('totcntrbgfts > 500000')
df.drop(['totrevenue', 'totcntrbgfts'], axis=1, inplace=True)
df = DS.zeroize(df)
df_AS = DS.abn_score(df)




