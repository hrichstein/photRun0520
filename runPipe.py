import numpy as np
# from getJdan import getJdan
from f2mag import get_mags
from f2mag import f2mag_dirs
from flcFns import *
from pMatch import *
from pRefStars import *
from linTrans import *

workDir = './'
upperDir = "/Volumes/Spare Data/Hannah_Data/"

filt_arr = ['F606W', 'F814W']
# filt_arr = ['F814W']
targname = 'HOROLOGIUM-I'

matchtol = 5.0
pixtol = 2
date = '1305'
catDir = workDir+'catRawMags'+date+'/catDir/'

iter = 1
# for ff, filt in enumerate(filt_arr):
# #     # get_mags(targname,filt,date,workDir=workDir)
    # wrapAll(targname,filt,date,workDir=workDir,matchtol=matchtol,iter=iter,\
    # stdCut=2.5)
# pMatch(targname,iter,catDir,matchtol=pixtol)

for ff, filt in enumerate(filt_arr):
    # pRefStars(targname,filt,catDir,magHi=24.5,magLo=21,\
    #     stdTol=0.1,posTol=3)
    linTrans(targname,filt,iter,catDir)
