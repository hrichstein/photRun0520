# Creates two directories for each pointing, one for each filter
# Creates inner directories to house crclean fits
# Moves flc_fits files to new directories

import numpy as np
import os

upperDir = '/Volumes/Spare Data/Hannah_Data/'

def make_dir(targnames):

    names = np.loadtxt(targnames,dtype=str)

    f606w_dirs = [[] for xx in range(len(names))]
    f814w_dirs = [[] for xx in range(len(names))]

    for nn in range(len(names)):
        f814w_dirs[nn] = names[nn] + '_f814w'
        f606w_dirs[nn] = names[nn] + '_f606w'

    for dir606w in f606w_dirs:
        if not os.path.exists(os.path.join(".",dir606w)):
            os.makedirs(dir606w)
        if not os.path.exists(os.path.join(".",dir606w,"crClean")):
            os.makedirs(os.path.join(".",dir606w,"crClean"))

    for dir814w in f814w_dirs:
        if not os.path.exists(os.path.join(".",dir814w)):
            os.makedirs(dir814w)
        if not os.path.exists(os.path.join(".",dir814w,"crClean")):
            os.makedirs(os.path.join(".",dir814w,"crClean"))

    return None

def run_command(com):

    s0 = ''
    com = s0.join(com)
    res = os.system(com)

    return res

def move_files(targnames):

    names = np.loadtxt(targnames,dtype=str)

    # file_names = [[] for xx in range(len(names))]

    for nn in range(len(names)):
        file_names =  upperDir + names[nn] + '_flcs.txt'

        temp_dat = np.genfromtxt(file_names,dtype=str)

        temp_dir_814 = names[nn] + '_f814w'
        temp_dir_606 = names[nn] + '_f606w'

        for tt in range(len(temp_dat)):

            if temp_dat[tt,1] == 'F606W':
                jdan_name = temp_dat[tt,0] + ''

                com = ["mv flc_fits/", jdan_name, "_flc.fits ", temp_dir_606]
            elif temp_dat[tt,1] == 'F814W':
                jdan_name = temp_dat[tt,0] + ''

                com = ["mv flc_fits/", jdan_name, "_flc.fits ", temp_dir_814]

            run_command(com)

    return None




# End
