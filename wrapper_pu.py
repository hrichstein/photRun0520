import numpy as np
import os
from astropy.io import fits

from getDRCfiltRef_pu import *
    # getRefDRCFilt
from drcFiltLinTrans_pu import *
    # linFiltTransDRC
from matchDRCfilt_pu import *
    # matchFiltDRC

from getJdan import getJdan
from runPU_1008 import f2mag_dirs, runPhotUtils
from initialCorrMatch_pu import *
    # distCor, offCor, matchWJCs, pullMags, wrapped
from linTrans_1_pu import outDiths, makePlot, openFiles
from reMatchPull_pu import *
    # matchWJCs_i, pullMags_i, wrapped_i
from stdCuts_pu import makeSTDcuts
from drcFLCref_pu import *
    # getRef
from linFLC2drc_pu import *
    # linFLC2drc
from whichIter_pu import whichIter, doIterMatch, getMatch
from getZPT_pu import *
    # getZPT, applyZPT, doZPT
from plotZPTdiff_pu import plotZPTdiff
from getRefFilt_pu import *
    # getRefFilt
from linTransFiltFLC_pu import *
from matchFiltFLC_pu import *
    # matchFilt
from makeCMD_pu import makeCMD

filt_arr = ['F606W','F814W']
# filt_arr = ['F606W']
# targname_arr = ['SAGITTARIUS-II','HOROLOGIUM-I']

targname_arr = ['HOROLOGIUM-I']

for c1,targname in enumerate(targname_arr):
    rand_tuple = f2mag_dirs(targname,date='10Aug',workDir='./')
    saveDir = rand_tuple[-1]

    # getRefDRCFilt(targname,dir=saveDir,matchtol=3)
    # linFiltTransDRC(targname,dir=saveDir)
    # matchFiltDRC(targname,dir=saveDir,matchtol=3)

    # for c2,filt in enumerate(filt_arr):
    #     jdan = getJdan(targname,filt)
        # runPhotUtils(targname,filt,jdan,saveDir=saveDir)
        # wrapped(targname,filt,jdan,catDir=saveDir)
        # outDiths(targname,filt,jdan,dir=saveDir,suffix='_ref.dat',iter=1)
        # openFiles(targname,filt,jdan,dir=saveDir,iter=1)
        # wrapped_i(targname,filt,jdan,iter=1,catDir=saveDir)
        # makeSTDcuts(saveDir,filt,suffix='_aftLT.dat')
        # getRef(targname,filt,dir=saveDir,matchtol=50)
        # linFLC2drc(targname,filt,dir=saveDir)
        # match_file = whichIter(targname,filt,dir=saveDir)
        # print(match_file)
        # getMatch(targname,filt,match_file,dir=saveDir,matchtol=2.5,stdTol=5)
        # doIterMatch(targname,filt,dir=saveDir,matchtol=2.5,stdTol=5)
        # doZPT(targname,filt,dir=saveDir,sigTol=2.5,stdTol=0.05)
        # plotZPTdiff(targname,filt,dir=saveDir,sigTol=2.5,stdTol=0.05)
    # getRefFilt(targname,matchtol=3,dir=saveDir)
    # linFiltTrans(targname,dir=saveDir)
    # matchFilt(targname,dir=saveDir,matchtol=3)
    makeCMD(targname,dir=saveDir)
