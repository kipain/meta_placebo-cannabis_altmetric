from urllib.request import urlopen
from urllib.error import HTTPError
import json
import pandas as pd
import numpy as np
import time

# Load information with all the dois
df = pd.read_csv('./DOI_Cannabis.csv', sep=',', header=None)
# just grab the dois and drop any nans
dois = df[0].dropna()

# Loop through each doi
altmetinfo = {}
for i, doi in dois.iteritems():   
    # DOI should look like this: 10.1016/j.jpain.2007.12.010 following bit of code just cleans up any exceptions
    if 'proxy.kib' in doi: 
        doi = doi.split('.se/')[1]
    elif 'https://doi:' in doi: 
        doi = doi.split('doi:')[1]
    elif 'ingen doi' in doi: 
        pass
    elif 'doi' in doi: 
        doi = doi.split('.org/')[1]

    print('Looking up: ' + doi)
    # Make url to grab
    url = 'https://api.altmetric.com/v1/doi/' + doi
    try:
        # Query the altmeric DOI, grab a json.
        # If doing this a lot (>10,000, should add an API key)
        r = urlopen(url)
        r = r.read()
        altmetinfo[i] = json.loads(r.decode("utf-8"))
        print('Entry found at altmetric')
    except HTTPError: 
        # If there is an error, add a nan instead (not necessary really as it is dropped later)
        altmetinfo[i] = np.nan
        print('Not indexed by altmetric')
    # Dont make altmetric mad. They say once a second, but when not using an API key once per 2 seconds is probably safer. 
    time.sleep(2)

# make to a dataframe
altdf = pd.DataFrame(altmetinfo).transpose()
# Drop those with no entries found
# altdf.dropna(how='all', inplace=True)
# Save
altdf.to_csv('altmetric_info.tsv', sep='\t')


