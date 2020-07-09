import numpy as np
import os
from astropy.io import fits
import time

# from getJdan import getJdan
# from f2mag0707 import *
# from hst_func import *
# from linTrans import *
from f2mag0707 import f2mag_dirs
# from initialCorrMatch0707 import *
# from linTrans_1_0707 import *
# from pltMaking0707 import *
# from reMatchPull0707 import *
# from stdCuts0707 import *
# from getFLCdrcRefStars0707 import *
# from linFLC2drc0707 import *
# from getRefiter0707 import *
# from linFLC2drcIter0707 import *
from whichIter0707 import *
from getMatchedFLCdrc0707 import *

filt_arr = ['F606W', 'F814W']

targname_arr = ['HYDRA-II','PEGASUS-III','PHOENIX-II','RETICULUM-II','TRIANGULUM-II-EAST','TRIANGULUM-II-WEST','TUCANA-II-NE',
'TUCANA-II-NW','TUCANA-II-SE','TUCANA-II-SW','SAGITTARIUS-II']

# Got all of the FLC magnitudes calculated
for c1,targname in enumerate(targname_arr):
    seDir, magCatDir, catDir = f2mag_dirs(targname,date='1305',workDir='./')
    for c2,filt in enumerate(filt_arr):
        # get_mags(targname,filt,'1305',workDir='./')
        # wrapped(targname,filt)
        # outDiths(argname,filt,dir=catDir,suffix='_ref.dat',iter=1)
        # openFiles(targname,filt,dir=catDir,iter=1) # makes plots
        # wrapped_i(targname,filt,iter=1)
        # makeSTDcuts(catDir,filt,suffix='_aftLT.dat')
        # getRef(targname,filt,dir=catDir,matchtol=50)
        # linFLC2drc(targname,filt,dir=catDir)
        match_file = whichIter(targname,filt,dir=catDir)
        print(match_file)
        getMatch(targname,filt,match_file,dir=catDir,matchtol=5,stdTol=5)
