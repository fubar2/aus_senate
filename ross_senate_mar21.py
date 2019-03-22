# inspired by https://github.com/tmccarthy/ausvotes
# fields in data are
# ElectorateNm  VoteCollectionPointNm   VoteCollectionPointId   BatchNo PaperNo Preferences
# Preferences are a string of integers - so try simple converting into a string to see how
# many duplicates there are - turns out a lot
# first rows of Tasmanian data aec-senate-formalpreferences-20499-TAS.csv
"""
ElectorateNm,VoteCollectionPointNm,VoteCollectionPointId,BatchNo,PaperNo,Preferences
Bass,Branxholm,1,1,1,",,,,,,,,,,,,,,,,,,,,,21,22,45,44,43,42,41,40,52,53,54,7,8,55,56,2,5,4,3,1,6,49,50,51,23,24....
"""
# processing gives
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
....

    """


import csv
import string
import zipfile
import numpy
import pandas as pd
import sklearn

FDIR = '/home/ross/Downloads/aec-senate-formalpreferences-20499-'

senateDtypes = {"ElectorateNm":object,"VoteCollectionPointNm":object,
    "VoteCollectionPointId":int,"BatchNo":int,"PaperNo":int,"Preferences":object}
    
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

inCSVs = ["ACT.zip","TAS.zip","NT.zip"]
for fn in inCSVs:
    fpath = '%s%s' % (FDIR,fn)
    zfile = zipfile.ZipFile(fpath)
    finfo = zfile.infolist()[0] # assume only one!
    ifile = zfile.open(finfo)
    dat = pd.read_csv(ifile, quotechar='"',dtype=senateDtypes,comment='-')
    datnames=fn.split('-')[-1] # last part
    datname = datnames.split('.zip')[0]
    print('State=',datname)
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
        sps[i] = ','.join(['%d' % x for x in s]) # a big string - how many are identical -> use value_counts for table
    dat['pref'] = sp
    dat['spref'] = sps
    sdat = dat.drop(columns=['Preferences'])
    vc = sdat['spref'].value_counts().to_frame()
    vc.columns = ["Count"]
    outfname = '%s_table.tab' % datname
    vc.to_csv(outfname,sep='\t',index_label='Preferences')

