# inspired by https://github.com/tmccarthy/ausvotes
# ross lazarus me fecit 21 march 2018
#
# march 23 Vote early, vote often
#   WA has wierd data in csv - chasing down is painful...
#   Aha. One division name has comment char "-" in it set to deal with the stupid 2nd row
#   of dashes - changed to skiprows=[1,] in read_csv - now seems to work
#   Flag possible transcription errors where primary vote was involved - too horrible to class as a meatsock error?
#
# march 22
#
# Added detection of preference strings with hamming distance = 1 or where a simple transpostion explains the differences.
# Limit to top 20 - nShow in code
# These are interesting as they may be sheeple making errors rather than not following HTV cards?
# EG for NT we see that the top string is related to #8 and #16 by a single discordant box or a transposition between neighboring boxes
# Could group these counts and call them #0 for sensitivity analysis.
# Top HTV patterns will increase by 10% or more if we do that
#
# march 21
#
# fields in data are
# ElectorateNm  VoteCollectionPointNm   VoteCollectionPointId   BatchNo PaperNo Preferences
# Preferences are a string of integers - so try simple converting into a string to see how
# many duplicates there are - turns out a lot
# first rows of Tasmanian data aec-senate-formalpreferences-20499-TAS.csv
#  ElectorateNm,VoteCollectionPointNm,VoteCollectionPointId,BatchNo,PaperNo,Preferences
#  Bass,Branxholm,1,1,1,",,,,,,,,,,,,,,,,,,,,,21,22,45,44,43,42,41,40,52,53,54,7,8,55,56,2,5,4,3,1,6,49,50,51,23,24....
#
# current output sample
"""
### NT Transposition of positions 2 and 3
 #0 = 6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=6208)
 #5 = 6,4,5,0,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=517)
### NT Hamming=1 difference at position 2
 #0 = 6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=6725)
 #8 = 6,4,7,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=346)
### NT Transposition of positions 1 and 2
 #0 = 6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=7071)
 #16 = 6,0,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=204)
### NT Hamming=1 difference at position 6
 #3 = 1,2,3,4,5,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=672)
 #4 = 1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=536)
### NT Transposition of positions 4 and 5
 #6 = 0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=501)
 #7 = 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=473)
### NT Transposition of positions 0 and 1
 #9 = 0,6,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=276)
 #16 = 6,0,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=204)
### NT Hamming=1 difference at position 0
 #11 = 7,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=255)
 #14 = 0,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 (n=220)
                                                     Count State
6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   6208    NT
0,3,6,2,5,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   6022    NT
0,3,5,1,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   1284    NT
1,2,3,4,5,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    672    NT
1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    536    NT
6,4,5,0,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    517    NT
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    501    NT
0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    473    NT
6,4,7,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    346    NT
0,6,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    276    NT
4,3,5,2,7,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    256    NT
7,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    255    NT
4,3,5,2,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    223    NT
0,3,5,2,6,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    222    NT
0,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    220    NT
5,3,4,2,7,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    214    NT
6,0,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    204    NT
7,6,5,4,3,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    195    NT
5,0,4,3,1,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    194    NT
6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    188    NT
### After amalgamating likely error categories:
                                                     Count State
6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   7275    NT
0,3,6,2,5,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   6022    NT
0,3,5,1,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   1284    NT
1,2,3,4,5,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   1208    NT
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    974    NT
0,6,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    480    NT
4,3,5,2,7,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    256    NT
7,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    475    NT
4,3,5,2,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    223    NT
0,3,5,2,6,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    222    NT
5,3,4,2,7,1,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    214    NT
7,6,5,4,3,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    195    NT
5,0,4,3,1,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    194    NT
6,5,4,3,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    188    NT 
"""

import os
import csv
import string
import pandas as pd


FDIR = '/home/ross/Downloads/aec-senate-formalpreferences-20499-'
  
pd.set_option('display.max_colwidth',256) # to prevent truncation
pd.set_option('display.width', 256)


nShow = 20 # for hamming/transposition put to stdout during run
inCSVs = ["NT.zip","TAS.zip","ACT.zip","WA.zip","QLD.zip","SA.zip","VIC.zip","NSW.zip"]
topTen = []
sumName = 'top%d_table.tab' % nShow
sumFiddledName = 'Fiddled_top%d_table.tab' % nShow
errName = 'plausible_errors.txt'

try:
    os.remove(sumName)
except:
    pass
try:
    os.remove(errName)
except:
    pass

   
def reportDistances(df,datname):
    """
    check for prefs with only 1 edit needed (? meatsock error)
    or where a transposition (also meatsock) will work
    
    Return fiddled data where simple errors are "fixed" among the top patterns by
    attributing the smaller count to the larger and deleting the smaller pattern
    
    Ballot paper did good service as a table cloth for this senate election as I recall
    so errors could be expected....
    
    Record indices of differences. If only one, hamming = 1. If two check for transposition between
    adjacent boxes
    
    todo: ? check that preference 1 does not change - assume that distracted voters get
    that right when they make some other less important error.
    NO vote changing transitions found in top 20 - that's good. 
    """
    dft = df.copy()
    report = []
    killMe = []
    for i,s in enumerate(list(dft.index.values)):
        ss = s.split(',')
        ns = dft.iloc[i][0]    # use that index 0 to remove pandas series wrapper
        for j in range(i,(dft.shape[0]-1)):
            s2 = dft.index.values[j]
            ns2 = dft.iloc[j][0] # count
            s2s = s2.split(',')
            diffs = [i for i,x in enumerate(ss) if (s2s[i] != x)]
            mergeUs = False
            if len(diffs) == 1:
               mergeUs = True
               report.append('### %s Hamming=1 difference at position %d\n #%d = %s (n=%d)\n #%d = %s (n=%d)' % (datname,diffs[0],i,s,ns,j,s2,ns2))
            if len(diffs) == 2: # may be transposition between neighboring boxes?
                p,q = diffs     # box zero based indices
                if (abs(p - q) == 1 and ss[p] == s2s[q] and ss[q] == s2s[p]): # matching neighbors
                    mergeUs = True
                    report.append('### %s Transposition of positions %d and %d\n #%d = %s (n=%d)\n #%d = %s (n=%d)' % (datname,p,q,i,s,ns,j,s2,ns2))
                    if (ss[p] == 1 or ss[q] == 1):
                        report.append('!!! %s ABOVE TRANSPOSITION likely a REAL DIFFERENCE - primary vote changed - NOT merged')
                        mergeUs = False
            if mergeUs: # hypothetical merge of commonest preference patterns where possible simian error
                ns += ns2 # update local count in case multiples
                dft.iloc[i][0] = ns # merge
                killMe.append(s2) # index to remove 
    if len(killMe) > 0:
        dft = dft.drop(killMe)
    return(report,dft)
        

for fnum,fn in enumerate(inCSVs):
    fpath = '%s%s' % (FDIR,fn)
    dat = pd.read_csv(fpath, quotechar='"',skiprows=[1,],compression='infer')
    datnames=fn.split('-')[-1] # last part
    datname = datnames.split('.zip')[0]
    sp = dat['Preferences'].copy()
    for i in range(len(sp)):
        ss = sp.iloc[i]
        try:
            s = ss.split(',')
        except:
            print('!!! not splittable bad data at row',i,'=',ss,' Ignored')
            s = ''
        if (len(s) > 1):
            for j in range(len(s)):
                if s[j] == "":
                    s[j] = 0
                elif s[j] == "/" or s[j] == '*':
                    # Tim McCarthy reported that AEC says solo tick or cross == 1
                    s[j] = 1
                else:
                    s[j] = int(s[j])
            try: # WA file has bogus data somewhere
                sp[i] = ','.join(['%d' % x for x in s])
            except:
                print('!!! cannot join bad data at row',i,'=',s)
        # a big string - how many are identical -> use value_counts for table
    dat['spref'] = sp
    sdat = dat.drop(columns=['Preferences'])
    vc = sdat['spref'].value_counts().to_frame()
    vc.columns = ["Count"]
    vchead = vc.head(n=nShow).copy()
    (rep,vcht) = reportDistances(vchead,datname)
    if len(rep) > 0:
        print('\n'.join(rep))
        f = open(errName,'a')
        f.write('\n'.join(rep))
        f.write('\n')
        f.close()
    else:
        print('No hamming distance = 1 or transposed pairs found\n')
    
    vchead['State'] = datname
    vchead.to_csv(sumName,sep='\t',index_label='Preferences',mode='a',header=(fnum==0))
    print(vchead)
    vcht['State'] = datname
    vcht.to_csv(sumFiddledName,sep='\t',index_label='Preferences',mode='a',header=(fnum==0))
    print('### After amalgamating likely error categories:')
    print(vcht)
