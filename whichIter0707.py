import numpy as np
import os
from astropy.io import fits

from getRefiter0707 import *
from linFLC2drcIter0707 import *

from f2mag0707 import f2mag_dirs

def whichIter(targname,filt,dir='./'):

    iter = int(1)
    kI = True

    nS_list = []
    mOff_list = []
    it_list = []

    while kI:

        numStars, meanOffset = getRef_i(targname,filt,dir=dir,matchtol=10,stdTol=2.5,iter=iter)

        nS_list = np.append(nS_list,[numStars])
        mOff_list = np.append(mOff_list,[meanOffset])
        it_list = np.append(it_list,[iter])

        if iter>=int(2):
            if np.logical_and((nS_list[-1] >= nS_list[-2]),(mOff_list[-1] <= mOff_list[-2])) :
                kI = False
                takeRun = iter
                # out = 'Case 1'

            elif np.logical_and((nS_list[-1] >= nS_list[-2]),(mOff_list[-1] >= mOff_list[-2])) :
                kI = False
                takeRun = iter-1
                # out = 'Case 2'

            elif np.logical_and((nS_list[-1] <= nS_list[-2]),(mOff_list[-1] >= mOff_list[-2])) :
                kI = False
                takeRun = iter-1
                # out = 'Case 3'

        linFLC2drc_i(targname,filt,dir=dir,iter=iter)
        iter += 1

    if takeRun == 1:
        file_str = dir+targname+"_"+filt+"_drcTrans.dat"
    else:
        iterStr = str(takeRun-1)
        file_str = dir+targname+"_"+filt+"_drcTrans"+iterStr+".dat"

    # return file_str, nS_list, mOff_list, it_list, out
    return file_str

# targname = 'HYDRA-II'
# filt = 'F606W'
#
# seDir, magCatDir, catDir = f2mag_dirs(targname,date='1305',workDir='./')
# test,nS,mO,it,out = whichIter(targname,filt,dir=catDir)

# print("String",test)
# print("Number of Stars",nS)
# print("Mean Offset",mO)
# print("Iter List",it)
# print(out)



#
