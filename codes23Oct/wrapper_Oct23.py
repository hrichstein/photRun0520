""" Hopefully a cleaner, more straightforward wrapper """

import numpy as np

from runPhotUtilsDRC import f2mag_dirs, runPhotUtils


# IMPORTANT VARIABLES FOR THIS PROCESS
work_dir = '../'  # this goes to photRun0520
drcDir = '/Volumes/Spare Data/Hannah_Data/origDRCs/'
targFile = work_dir + 'targnamesDirections2.txt'
dateDef = '23Oct'
drcInfoFile = '/Volumes/Spare Data/Hannah_Data/' + "drcTargInfo_new.dat"
suffix_ = '_pu.dat'
radius_ = int(4)

########

targname_arr = np.genfromtxt(targFile,dtype='str')

# Run this once, then comment out. May need to cut drcInfoFile
# into smaller pieces to avoid memory overload.
runPhotUtils(drcInfoFile,radius=radius_,suffix=suffix_)

# for c1,targname in enumerate(targname_arr):
#     save_dir = f2mag_dirs(targname,date=dateDef,workDir=work_dir)
#
