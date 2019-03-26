rationale = """Inspired by <a href="https://github.com/tmccarthy/ausvotes">https://github.com/tmccarthy/ausvotes</a><br>
ross lazarus me fecit 21 march 2018<br>
Code at <a href="https://github.com/fubar2/aus_senate">https://github.com/fubar2/aus_senate</a><br>
Comments and contributions welcomed there<br>
How to votes cards are at <a href="https://www.abc.net.au/news/federal-election-2016/guide/snt/htv/">https://www.abc.net.au/news/federal-election-2016/guide/snt/htv/</a>
"""
# This brutal and fugly code was quickly hacked without regard for aesthetics. So bite me. Or send code
# Requires about 5GB ram and 26 minutes to run over all the data on my ancient server.
# History:
#
# march 26
#  added percentage of all ballots to count tables
#
# march 25
# pdfs now work
#
# march 24
#   added index.html report summary of top counts before and after amalgamation of errors
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
# march 21 - started project
#
# fields in data are
# ElectorateNm  VoteCollectionPointNm   VoteCollectionPointId   BatchNo PaperNo Preferences
# Preferences are a string of integers - so try simple converting into a string to see how
# many duplicates there are - turns out a lot
# first rows of Tasmanian data aec-senate-formalpreferences-20499-TAS.csv
#  ElectorateNm,VoteCollectionPointNm,VoteCollectionPointId,BatchNo,PaperNo,Preferences
#  Bass,Branxholm,1,1,1,",,,,,,,,,,,,,,,,,,,,,21,22,45,44,43,42,41,40,52,53,54,7,8,55,56,2,5,4,3,1,6,49,50,51,23,24....
#

import os
import csv
import string
import pandas as pd
import weasyprint

QUICK = 0
FDIR = '/home/ross/Downloads/aec-senate-formalpreferences-20499-'
META = '2016 Australian senate preference data processed using code at https://github.com/fubar2/aus_senate'
STYL = """<style type="text/css">
            tr:nth-child(even) { background-color: lightblue; }
            tr:nth-child(odd) { background-color: lightyellow; }
        </style>"""
pd.set_option('display.max_colwidth',256) # to prevent truncation
pd.set_option('display.width', 256)
pd_props = [
('size', '50in 30in')] 
th_props = [
  ('font-size', '14px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7f7f9')
  ]

# Set CSS properties for td elements in dataframe
td_props = [
  ('font-size', '12px'),
  ('text-align', 'center'),
  ]

# prepare table styles for render call
 # {"selector":"@page","props":pd_props},

ourStyles = [
  {"selector":"th", "props":th_props},
  {"selector":"td", "props":td_props}
  ]


nShow = 21 # includes header
inCSVs = ["NSW.zip","VIC.zip","WA.zip","QLD.zip","SA.zip","ACT.zip","TAS.zip","NT.zip"]
if QUICK:
    inCSVs = ["NT.zip","ACT.zip"]
topTen = []
sumName = 'reports/top%d_tables.tab' % (nShow-1)
sumFiddledName = 'reports/amalgamated_top%d_tables.tab' % (nShow-1)
errName = 'reports/plausible_errors_%d.txt' % (nShow-1)
htmlName = 'reports/top_%d_%s.html'
outPDF = 'reports/common_ballots_senate_2016_top%d_%s.pdf'

for fn in [sumName,sumFiddledName,errName]:
    # these are appended to for each iteration
    try:
        os.remove(fn)
    except:
        pass
# precompute a very long list of box column labels
boxlabs = [chr(x+ord('A')) for x in range(26)]
for i in range(20):
    pre = boxlabs[i]
    boxlabs += [''.join([pre,chr(x+ord('A'))]) for x in range(26)]

def makeTable(df,state):
    """ split into letter headed boxes table
    """
    df2 = pd.DataFrame()
    prefs = [x.split(',') for x in list(df.index.values)]
    counts = list(df['Count'])
    props = list(df['Prop'])
    nr = df.shape[0]
    nc = len(prefs[0])
    sl = [state]*nr
    datdic = {'State':sl}
    bl = boxlabs[:nc]
    csums = []
    for i in range(nc): # for each column
        c = [int(prefs[x][i]) for x in range(nr)]
        csums.append(sum(c)) # if zero, useless..
        datdic[bl[i]] = c     
    datdic['Counts'] = counts
    datdic['Prop'] = props
    df2 = pd.DataFrame(datdic)
    newi = list(range(1,nr))
    df2 = df2.reindex(newi)
    h2 = df2.style.set_table_styles(ourStyles).render()   
    h = ''.join(h2)
    return (h)
    
    
   
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
    Several vote changing transitions found in top 20 in some states so they do happen
    """
    dft = df.copy()
    report = []
    killMe = []
    indices = list(dft.index.values)
    nr = dft.shape[0]
    for i,s in enumerate(indices):
        ss = s.split(',')
        ns = dft.loc[s,'Count']    
        for j in range(i,(nr-1)):
            s2 = indices[j]
            ns2 = dft.loc[s2,'Count'] 
            s2s = s2.split(',')
            diffs = [y for y,x in enumerate(ss) if (s2s[y] != x)]
            mergeUs = False
            if len(diffs) == 1:
               p = diffs[0]
               if ss[p] == '1' or s2s == '1':
                    report.append('!!! %s ABOVE single error likely a REAL DIFFERENCE - primary vote changed - NOT merged')
               else:
                    mergeUs = True
                    report.append('### %s Hamming=1 difference at position %d\n #%d = %s (n=%d)\n #%d = %s (n=%d)' % (datname,diffs[0],i,s,ns,j,s2,ns2))
            elif len(diffs) == 2: # may be transposition between neighboring boxes?
                p,q = diffs     # zero based indices -> box order values
                if (abs(p - q) == 1 and ss[p] == s2s[q] and ss[q] == s2s[p]): # matching neighbors
                    mergeUs = True
                    report.append('### %s Transposition of positions %d and %d\n #%d = %s (n=%d)\n #%d = %s (n=%d)' % (datname,p,q,i,s,ns,j,s2,ns2))
                    if (ss[p] == '1' or ss[q] == '1'):
                        report.append('!!! %s ABOVE TRANSPOSITION likely a REAL DIFFERENCE - primary vote changed - NOT merged')
                        mergeUs = False
                        
            if mergeUs: # hypothetical merge of commonest preference patterns where possible simian error
                ns += ns2 # update local count in case multiples
                dft.at[s,'Count'] = ns # merge
                killMe.append(s2) # index to remove 
    if len(killMe) > 0:
        dft = dft.drop(killMe)
    return(report,dft)
        


for fnum,fn in enumerate(inCSVs):
    # NSW pdf needs 60" vic/qld/wa 55" sa 35" a4 landscape the rest 
    sizedict = {'NSW':60,'VIC':45,'QLD':50,'WA':35,'SA':25,'NT':10,'ACT':10,'TAS':25}
    fpath = '%s%s' % (FDIR,fn)
    dat = pd.read_csv(fpath, quotechar='"',skiprows=[1,],compression='infer')
    datnames=fn.split('-')[-1] # last part
    datname = datnames.split('.zip')[0]
    htmlrep = '''<!DOCTYPE html>\n<html lang="en"><head><meta charset="utf-8">
    <meta info="%s">%s</head>
    <body><b>Top 20 preference choice patterns<br>before and after amalgamation of patterns
    differing only by one box's value or a simple transposition between neighboring boxes not involving the primary vote
    for %s:</b><br>\n''' % (META,STYL,datname)
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
    counts = list(vc.loc[:,'Count'])
    tot = sum(counts)
    freqs = ['%2.2f%%' % (100.0*x/tot) for x in counts]
    vc['Prop'] = freqs
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

    htmlrep += '<h2>%s</h2><br>\n' % ('Top %d counts' % (nShow-1))
    nr,nc = dat.shape
    htmlrep += '### File %s has %d rows and %d columns<br>' % (fpath,nr,nc)
    htvlink = 'https://www.abc.net.au/news/federal-election-2016/guide/s%s/htv/' % datname.lower()
    htmlrep += '<a href="%s" target="_blank">How to vote cards - click here</a><br>' % htvlink
    htmlrep += makeTable(vchead,datname)
    vchead.to_csv(sumName,sep='\t',index_label='Preferences',mode='a',header=(fnum==0))
    print(vchead)
    vcht['State'] = datname
    if (vcht.shape[0] != vchead.shape[0]):
        htmlrep += '<h2>Amalgamated counts after ignoring arguably "small" differences</h2>\n'
        htmlrep += makeTable(vcht,datname)
        vcht.to_csv(sumFiddledName,sep='\t',index_label='Preferences',mode='a',header=(fnum==0))
        print('### After amalgamating likely error categories:')
        print(vcht)
    else:
        htmlrep += '<h2>### No arguably "small" differences to amalgamate were found</h2>\n'
    htmlrep += '<footer>%s</footer></body></html>\n' % (rationale)
    rep = open(htmlName % ((nShow-1),datname),'w')
    rep.write(htmlrep)
    rep.close()
    # Convert the html file to a pdf file using weasyprint
    ss = [weasyprint.CSS(string='@page { size: %din 10in } ' % sizedict[datname]),
         weasyprint.CSS(string="tr:nth-child(even) { background-color: lightblue; }"),
         weasyprint.CSS(string= "tr:nth-child(odd) { background-color: lightyellow; }")]
    weasyprint.HTML(htmlName % ((nShow-1),datname)).write_pdf(outPDF % ((nShow-1),datname),stylesheets=ss)
