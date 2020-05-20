import numpy as np
# from getJdan import getJdan
from f2mag import get_mags
from f2mag import f2mag_dirs
from flcFns import *

workDir = './'
upperDir = "/Volumes/Spare Data/Hannah_Data/"

filt_arr = ['F606W', 'F814W']
# filt_arr = ['F814W']
targname = 'HOROLOGIUM-I'

matchtol = 5.0
date = '1305'

for ff, filt in enumerate(filt_arr):

    # get_mags(targname,filt,date,workDir=workDir)
    wrapAll(targname,filt,date,workDir=workDir,matchtol=matchtol,iter=0)
