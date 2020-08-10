import numpy as np
import os
from astropy.io import fits

from getJdan import getJdan
from runPU_1008 import f2mag_dirs, runPhotUtils
from initialCorrMatch_pu import *
    # distCor, offCor, matchWJCs, pullMags, wrapped
from linTrans_1_pu import outDiths, makePlot, openFiles
from reMatchPull_pu import *
    # matchWJCs_i, pullMags_i, wrapped_i
from stdCuts_pu import makeSTDcuts

filt_arr = ['F606W','F814W']
targname_arr = ['SAGITTARIUS-II','HOROLOGIUM-I']

for c1,targname in enumerate(targname_arr):
    rand_tuple = f2mag_dirs(targname,date='10Aug',workDir='./')
    saveDir = rand_tuple[-1]

    for c2,filt in enumerate(filt_arr):
        jdan = getJdan(targname,filt)
        # runPhotUtils(targname,filt,jdan,saveDir=saveDir)
        wrapped(targname,filt,jdan,catDir=saveDir)
        outDiths(targname,filt,jdan,dir=saveDir,suffix='_ref.dat',iter=1)
        # openFiles(targname,filt,dir=saveDir,iter=1)
        # wrapped_i(targname,filt,iter=1,catDir=saveDir)
        # makeSTDcuts(saveDir,filt,suffix='_aftLT.dat')
