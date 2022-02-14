import pandas as pd
from habanero import counts
import time
import numpy as np 
# Load information with all the dois
df = pd.read_csv('altmetric_info.tsv', sep='\t', index_col=[0])
# just grab the dois and drop any nans
dois = df['doi'].dropna()


citations = []
for i, doi in dois.iteritems():   
    print(i)  
    try: 
        c = counts.citation_count(doi = doi)
    except: 
        c = np.nan
    time.sleep(1)
    print(c)
    citations.append(c)

df['citations'] = citations

df.to_csv('./altmetric_info.tsv', sep='\t')
