# header from
# ElectorateNm  VoteCollectionPointNm   VoteCollectionPointId   BatchNo PaperNo Preferences
# Preferences are a string of integers - so try one hot encoding to see what turns up.
"""
ElectorateNm,VoteCollectionPointNm,VoteCollectionPointId,BatchNo,PaperNo,Preferences
Bass,Branxholm,1,1,1,",,,,,,,,,,,,,,,,,,,,,21,22,45,44,43,42,41,40,52,53,54,7,8,55,56,2,5,4,3,1,6,49,50,51,23,24,,,25,26,27,28,9,10,48,47,46,11,12,29,30,13,14,31,32,33,34,15,16,17,18,19,20,3$

"""
import csv
import string
import numpy
import pandas as pd
import sklearn

TESTING = False
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

inCSVs = ["~/Downloads/test.csv",] # "~/Downloads/aec-senate-formalpreferences-20499-TAS.csv",]
if (not TESTING):
    inCSVs = ["~/Downloads/aec-senate-formalpreferences-20499-TAS.csv",]
for fpath in inCSVs:
    dat = pd.read_csv(fpath, quotechar='"',dtype={"ElectorateNm":object,"VoteCollectionPointNm":object,
    "VoteCollectionPointId":int,"BatchNo":int,"PaperNo":int,"Preferences":object})
    sp = dat['Preferences'].copy()
    sps = sp.copy()
    for i in range(len(sp)):
        s = sp[i].split(',').copy()
        for j in range(len(s)):
            if s[j] == "" or s[j] == "/" or s[j] == '*':
                s[j] = 0
            else:
                s[j] = int(s[j])
        sp[i] = s
        sps[i] = ','.join(['%d' % x for x in s])
    dat['pref'] = sp
    dat['spref'] = sps
    sdat = dat.drop(columns=['Preferences'])
    # print(sdat.head())
    vc = sdat['spref'].value_counts()
    print(vc)
    """
    for tasmania we get
    5,6,0,2,0,1,0,0,0,0,0,0,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0                                  
                               9824
0,1,2,0,0,0,0,5,0,0,0,6,3,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0                                  
                               2307
0,4,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,5,3,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0                                  
                               1490
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0                                  
                                687

    """
