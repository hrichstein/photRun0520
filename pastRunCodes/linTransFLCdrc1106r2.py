import numpy as np
from linear6d import *
from getJdan import *

dir = 'catRawMags1305/catDir/'
'''

transform.py

This code serves as the main interface for using the mpfit Python code (mpfit.py) to
determine the coefficients for a 6-parameter linear transformation (linear6d.py).
For the input, it takes 8 different 1D arrays:
- x and y positions of a list of sources to be transformed into another frame that
have already been matched to a corresponding list of sources in the other frame.

- x and y positions of the corresponding list in the intended frame

- weights for the sources (this is currently set to 1.0 for every source
to give equal weight

- x and y positions of all sources that are to be transformed into another frame. Once
the 6-param coefficients have been determined using the above matched sources, the
transformation is applied to this full list of sources and is saved out.


The first set of coordinates is the reference sources in your particular secondary dither. The second set of coordinates is the reference sources in the primary dither. And the third set is all sources in your secondary dither.
'''

RA, DEC, flags, c_star, mag1, mag2, mag3, mag4, xt1, yt1, xDRC_trans, yDRC_trans, xDRC_mat, yDRC_mat, magDRC, id_cat = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15

cat = np.genfromtxt(dir+'matchedFLCdrc1106.dat')

match_arr = np.zeros((len(cat),2))

match_arr[:,0] = cat[:,xDRC_trans]
match_arr[:,1] = cat[:,yDRC_trans]

master_arr = np.zeros((len(cat),2))

master_arr[:,0] = cat[:,xDRC_mat]
master_arr[:,1] = cat[:,yDRC_mat]

all_cat = np.genfromtxt(dir+'flcDRCpos1106_f606w.dat')

RA, DEC, flux, flags, c_star, mag1, mag2, mag3, mag4, ra1, dec1, ra2, dec2, ra3, dec3, ra4, dec4, xr1, yr1, xr2, yr2, xr3, yr3, xr4, yr4, xc1, yc1, xc2, yc2, xc3, yc3, xc4, yc4, xt1, yt1, xt2, yt2, xt3, yt3, xt4, yt4, xDRC, yDRC = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42

def linTrans(targname,filt,dir='catRawMags1305/catDir/'):
# matched_w_MagsPos2705.dat
    # match = np.loadtxt(dir+"matched_w_MagsPos2705r2.dat")
    # master = np.loadtxt(dir+"matched_w_MagsPos2705r2.dat")
    match = match_arr
    master= master_arr

    weights = np.zeros((len(match)))
    weights.fill(1.0)

    all = all_cat

    # all1000_idx = np.argsort(all[:,7])
    # #
    # all = all[all1000_idx]
    #
    # outname = jdanUse[0]+"_"+targname+"_"+filt+"_0206drcPSF.dat"

    outname = 'flcDRCmatch1106_f606wr2.dat'
    # new_match, new_all = test_linear(match[:,0], match[:,1], master[:,0], master[:,1], weights, weights, all[:,xt], all[:,yt])

    new_match, new_all = test_linear(match[:,0],match[:,1], master[:,0], master[:,1], weights, weights, all[:,xDRC],all[:,yDRC])

    np.savetxt(dir+outname, new_all, fmt="%1.6f")
    # np.savetxt(dir+'flcDRC0406newMatch.dat',new_match,fmt='%1.6f')


    return None

def addTranscols(targname,filt,dir='catRawMags1305/catDir/'):

    # jdanUse = getJdan(targname,filt)

    # for ff in range(len(jdanUse)):
    cat = np.genfromtxt(dir+'matched_w_MagsPos1106r2.dat')

    transCat = np.genfromtxt(dir + 'flcDRCmatch1106_f606wr2.dat')

    newCol = np.zeros((len(cat),2))

    newCol[:,0] = transCat[:,0]
    newCol[:,1] = transCat[:,1]

    cat = np.hstack((cat, newCol))

    header = 'RA DEC flux flags c_star mag1 mag2 mag3 mag4 ra1 dec1 ra2 dec2 ra3 dec3 ra4 dec4 xr1 yr1 xr2 yr2 xr3 yr3 xr4 yr4 xc1 yc1 xc2 yc2 xc3 yc3 xc4 yc4 xt1 yt1 xt2 yt2 xt3 yt3 xt4 yt4 xDRC yDRC'

    np.savetxt(dir+'flcDRCpos1106_f606wr2.dat', cat, header=header)

    return None

targname = 'HOROLOGIUM-I'
filt = 'F606W'

linTrans(targname,filt,dir='catRawMags1305/catDir/')
addTranscols(targname,filt,dir='catRawMags1305/catDir/')

# Iter      23    CHI-SQUARE =  239.5616411  DOF =  1862
#    P0 = -0.7688914295
#    P1 = 1.000172983
#    P2 = 0.0003970047803
#    P3 = -1.020091462
#    P4 = 0.0002689535807
#    P5 = 1.000337728
