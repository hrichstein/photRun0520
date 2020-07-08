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
from stdCuts0707 import *

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
        makeSTDcuts(catDir,filt,suffix='_aftLT.dat')
