
**Very simple data driven approach** to parse out all *voting preference allocation patterns* in a
file of preference allocations for valid votes without even looking at HTV. Numbers in boxes
are treated as comma separated strings so commonest ones can be identified and counted.
These are tabulated and the most common ones are likely to be HTV or donkey votes.

*HTV* are at https://www.abc.net.au/news/federal-election-2016/guide/snt/htv/

*Raw data* are at https://results.aec.gov.au/20499/Website/SenateDownloadsMenu-20499-Csv.htm

*Inspired by* https://github.com/tmccarthy/ausvotes


23 March

WA data has a division name with a "-" in it and I'd chosen that as the comment character for
pd.read_csv. Replaced that with skiprows=[1,] to drop that stupid second header row of dashes.

todo: test if a transposition involves a first preference - that is not an ignorable error?
done: TURNS OUT they do not - none found in top 20 voting patterns in any state.

22 March

Added detection of preference strings with hamming distance = 1 or where a simple transpostion accounts for
differences between the most common strings taken pairwise.

Limit to top 20 - nShow constant in code

These are interesting as they may be sheeple making errors rather than not following HTV cards?

EG for NT we see that the top string is related to #5, #8 and #16 by a single discordant box or a transposition between neighboring boxes

Could group these counts and add their counts to the commonest one for a sensitivity analysis on human error - ballots can be
fearful data entry forms - looks like the top HTV patterns will increase by perhaps 10%

**The CLP HTV count could probably be >10% higher becoming (6208 + 517 + 346)
if #5 and #8 are accepted as #0 with a single plausible human error?**

~~~~
### Transposition of positions 2 and 3
 #0 = 6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #5 = 6,4,5,0,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
### Hamming=1 difference at position 2
 #0 = 6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #8 = 6,4,7,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
### Transposition of positions 1 and 2
 #0 = 6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #16 = 6,0,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
### Hamming=1 difference at position 6
 #3 = 1,2,3,4,5,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #4 = 1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
### Transposition of positions 4 and 5
 #6 = 0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #7 = 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
### Transposition of positions 0 and 1
 #9 = 0,6,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #16 = 6,0,4,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
### Hamming=1 difference at position 0
 #11 = 7,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
 #14 = 0,6,5,4,1,2,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
NT
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
7,3,6,2,5,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0    188    NT
~~~~

21 March

~~~~
ross@ross-UX31A:~/rossdev/aus_senate$ head *.tab
==> ACT_table.tab <==
Preferences     Count
3,0,6,0,5,1,4,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 16473
6,5,1,0,0,0,4,2,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 9317
0,2,5,0,6,0,4,1,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 2697
3,0,6,0,5,1,4,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 1544
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 1155
0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 670
0,5,1,0,0,6,4,2,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 443
6,5,1,0,0,0,3,2,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 364
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 358

==> NT_table.tab <==
Preferences     Count
6,4,0,5,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     6209
0,3,6,2,5,1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     6021
0,3,5,1,4,2,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     1284
1,2,3,4,5,6,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     678
1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     538
6,4,5,0,1,3,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     517
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     468
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     363
0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0     349

==> TAS_table.tab <==
Preferences     Count
5,6,0,2,0,1,0,0,0,0,0,0,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   9824
0,1,2,0,0,0,0,5,0,0,0,6,3,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   2307
0,4,1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,5,3,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   1490
0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   687
0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   606
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   461
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,8,9,10,11,12,0,0,0,0,0,0,0,1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0        244
1,2,3,4,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   213
5,6,0,0,2,1,0,0,0,0,0,0,0,0,0,3,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   138

~~~~
Tasmanian data used as a test give pretty promising results with preference string followed by count

Original above found about 14k which is about the sum of the first 4 shown

~~~~
TAS 13,744  339,159 4.05%
~~~~

Commonest NT pattern looks like the CLP ticket but the 6th looks like 517 people made a transcription error - the HTV does not show box C so some sheeple may have accidentally 
preferenced the Citizens Electroral Council instead of the Greens - or else really preferred not to vote at all for the greens.
Raises the question of whether counting a vote as "following" an HTV needs to take into account possible transcription errors - hard to get into voters' heads but
at least the data driven approach allows patterns like these to be exposed.

